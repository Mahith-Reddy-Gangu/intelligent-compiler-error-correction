from typing import Dict, Any, List, Tuple, Optional

from generated.SimpleCVisitor import SimpleCVisitor
from generated.SimpleCParser import SimpleCParser


def _pos_gt(a_line: int, a_col: int, b_line: int, b_col: int) -> bool:
    """Return True if (a_line,a_col) > (b_line,b_col)."""
    if a_line != b_line:
        return a_line > b_line
    return a_col > b_col


class _DeclCollector(SimpleCVisitor):
    """
    Pass 1: Build a scope tree and collect declarations.

    Scopes:
      - One scope per functionDef
      - One scope per block { ... }

    Stores:
      parent[scope_id] -> parent scope_id or None
      decls[scope_id][name] -> (line, col, decl_kind)
      redecls -> list of issues
      declared_sites -> set of (name,line,col) to ignore as "uses"
    """

    def __init__(self):
        super().__init__()
        self._next_scope_id = 1

        self.parent: Dict[int, Optional[int]] = {}
        self.decls: Dict[int, Dict[str, Tuple[int, int, str]]] = {}
        self.declared_sites: set[Tuple[str, int, int]] = set()

        self.redecls: List[Dict[str, Any]] = []

        self._scope_stack: List[int] = []

    def _new_scope(self) -> int:
        sid = self._next_scope_id
        self._next_scope_id += 1
        self.decls[sid] = {}
        return sid

    def _enter_scope(self):
        sid = self._new_scope()
        parent = self._scope_stack[-1] if self._scope_stack else None
        self.parent[sid] = parent
        self._scope_stack.append(sid)

    def _exit_scope(self):
        if self._scope_stack:
            self._scope_stack.pop()

    def _cur_scope(self) -> Optional[int]:
        return self._scope_stack[-1] if self._scope_stack else None

    def _declare_here(self, name: str, line: int, col: int, kind: str):
        sid = self._cur_scope()
        if sid is None:
            return

        # Mark declaration site so checker won't treat it as a "use"
        self.declared_sites.add((name, line, col))

        if name in self.decls[sid]:
            prev_line, prev_col, prev_kind = self.decls[sid][name]
            self.redecls.append(
                {
                    "kind": "redecl",
                    "name": name,
                    "line": line,
                    "col": col,
                    "prev_line": prev_line,
                    "prev_col": prev_col,
                    "scope": sid,
                    "decl_kind": kind,
                }
            )
            return

        self.decls[sid][name] = (line, col, kind)

    # ---- scope nodes ----

    def visitFunctionDef(self, ctx: SimpleCParser.FunctionDefContext):
        self._enter_scope()

        fn_ident = ctx.IDENTIFIER()
        if fn_ident is not None and hasattr(fn_ident, "symbol"):
            self._declare_here(
                fn_ident.getText(),
                fn_ident.symbol.line,
                fn_ident.symbol.column,
                kind="func",
            )

        self.visitChildren(ctx)

        self._exit_scope()
        return None

    def visitBlock(self, ctx: SimpleCParser.BlockContext):
        self._enter_scope()
        self.visitChildren(ctx)
        self._exit_scope()
        return None

    # ---- declaration nodes ----

    def visitParam(self, ctx: SimpleCParser.ParamContext):
        ident = ctx.IDENTIFIER()
        if ident is not None and hasattr(ident, "symbol"):
            self._declare_here(
                ident.getText(),
                ident.symbol.line,
                ident.symbol.column,
                kind="param",
            )
        return self.visitChildren(ctx)

    def visitInitDeclarator(self, ctx: SimpleCParser.InitDeclaratorContext):
        ident = ctx.IDENTIFIER()
        if ident is not None and hasattr(ident, "symbol"):
            self._declare_here(
                ident.getText(),
                ident.symbol.line,
                ident.symbol.column,
                kind="var",
            )
        return self.visitChildren(ctx)


class UndeclaredIdentifierChecker(SimpleCVisitor):
    """
    Pass 2: Detect identifier uses with scope awareness.

    Issues:
      - undeclared
      - use_before_declare
      - redecl
      - unused (warning)

    NOTE: We only consider variables/params for unused warnings (not functions).
    """

    def __init__(self, symbols: Dict[str, Dict[str, Any]], require_decl_before_use: bool = True):
        super().__init__()
        self.symbols = symbols or {}
        self.require_decl_before_use = require_decl_before_use

        self._parent: Dict[int, Optional[int]] = {}
        self._decls: Dict[int, Dict[str, Tuple[int, int, str]]] = {}
        self._declared_sites: set[Tuple[str, int, int]] = set()

        self.issues: List[Dict[str, Any]] = []

        # scope stack for pass2
        self._scope_stack: List[int] = []
        self._next_scope_id = 1

        # Track (scope_id, name) that were actually used
        self._used: set[Tuple[int, str]] = set()

    def _collect(self, tree):
        collector = _DeclCollector()
        collector.visit(tree)

        self._parent = collector.parent
        self._decls = collector.decls
        self._declared_sites = collector.declared_sites

        for it in collector.redecls:
            self.issues.append(dict(it))

    def _enter_scope(self):
        sid = self._next_scope_id
        self._next_scope_id += 1
        self._scope_stack.append(sid)

    def _exit_scope(self):
        if self._scope_stack:
            self._scope_stack.pop()

    def _cur_scope(self) -> Optional[int]:
        return self._scope_stack[-1] if self._scope_stack else None

    def _lookup_visible(self, name: str, cur_scope: Optional[int]) -> Optional[Tuple[int, int, int, str]]:
        sid = cur_scope
        while sid is not None:
            d = self._decls.get(sid, {})
            if name in d:
                dl, dc, kind = d[name]
                return sid, dl, dc, kind
            sid = self._parent.get(sid)
        return None

    def _emit_unused_warnings(self):
        """
        After traversal: any var/param declared but never used in that same scope -> warning.
        """
        for sid, declmap in self._decls.items():
            for name, (dl, dc, kind) in declmap.items():
                if kind not in ("var", "param"):
                    continue
                if (sid, name) not in self._used:
                    self.issues.append(
                        {
                            "kind": "unused",
                            "name": name,
                            "line": dl,
                            "col": dc,
                        }
                    )

    def visit(self, tree):
        # pass1
        self._collect(tree)
        # pass2
        out = super().visit(tree)
        # finalize warnings
        self._emit_unused_warnings()
        return out

    # ---- scope nodes (must match pass1 order) ----

    def visitFunctionDef(self, ctx: SimpleCParser.FunctionDefContext):
        self._enter_scope()
        self.visitChildren(ctx)
        self._exit_scope()
        return None

    def visitBlock(self, ctx: SimpleCParser.BlockContext):
        self._enter_scope()
        self.visitChildren(ctx)
        self._exit_scope()
        return None

    # ---- use sites ----

    def visitPrimaryExpression(self, ctx: SimpleCParser.PrimaryExpressionContext):
        ident = ctx.IDENTIFIER()
        if ident is None or not hasattr(ident, "symbol"):
            return self.visitChildren(ctx)

        name = ident.getText()
        line = ident.symbol.line
        col = ident.symbol.column

        if (name, line, col) in self._declared_sites:
            return self.visitChildren(ctx)

        cur_scope = self._cur_scope()
        found = self._lookup_visible(name, cur_scope)

        if found is None:
            self.issues.append({"kind": "undeclared", "name": name, "line": line, "col": col})
            return self.visitChildren(ctx)

        found_scope, decl_line, decl_col, decl_kind = found

        # mark used if it's a var/param
        if decl_kind in ("var", "param"):
            self._used.add((found_scope, name))

        if self.require_decl_before_use:
            if cur_scope is not None and found_scope == cur_scope:
                if _pos_gt(decl_line, decl_col, line, col):
                    self.issues.append(
                        {
                            "kind": "use_before_declare",
                            "name": name,
                            "line": line,
                            "col": col,
                            "decl_line": decl_line,
                            "decl_col": decl_col,
                        }
                    )

        return self.visitChildren(ctx)

    def get_issues(self) -> List[Dict[str, Any]]:
        seen = set()
        out: List[Dict[str, Any]] = []
        for it in self.issues:
            key = (it.get("kind"), it.get("name"), it.get("line"), it.get("col"))
            if key in seen:
                continue
            seen.add(key)
            out.append(it)
        return out