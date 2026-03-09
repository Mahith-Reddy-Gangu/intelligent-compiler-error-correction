# compiler/semantic_checker.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from antlr4.tree.Tree import TerminalNodeImpl

try:
    from generated.SimpleCParser import SimpleCParser
except Exception as e:
    raise ImportError(
        "generated SimpleCParser not found. Run ANTLR generation into 'generated/' first."
    ) from e

_VISITOR_BASE = None
try:
    from generated.SimpleCVisitor import SimpleCVisitor as _V  # type: ignore
    _VISITOR_BASE = _V
except Exception:
    try:
        from generated.SimpleCParserVisitor import SimpleCParserVisitor as _V  # type: ignore
        _VISITOR_BASE = _V
    except Exception as e:
        raise ImportError(
            "generated visitor not found. Generate with ANTLR '-visitor'. "
            "Expected generated/SimpleCVisitor.py or generated/SimpleCParserVisitor.py"
        ) from e


@dataclass
class _DeclInfo:
    name: str
    ctype: str          # for vars/params: "int"/"float"/"char"/"void"; for funcs: "func"
    line: int
    col: int
    used: bool = False


@dataclass
class _FuncSig:
    name: str
    ret_type: str
    param_types: List[str]
    line: int
    col: int


def _tok_line_col(node: Any) -> Tuple[int, int]:
    try:
        sym = node.getSymbol()
        if sym is not None:
            return int(sym.line), int(sym.column)
    except Exception:
        pass
    try:
        st = getattr(node, "start", None)
        if st is not None:
            return int(st.line), int(st.column)
    except Exception:
        pass
    return (0, 0)


def _is_identifier_terminal(node: TerminalNodeImpl) -> bool:
    try:
        sym = node.getSymbol()
        if sym is None:
            return False
        return sym.type == SimpleCParser.IDENTIFIER
    except Exception:
        return False


def _infer_literal_type_from_token_type(tok_type: int) -> Optional[str]:
    if tok_type == SimpleCParser.INTEGER:
        return "int"
    if tok_type == SimpleCParser.FLOAT_LITERAL:
        return "float"
    if tok_type == SimpleCParser.CHAR_LITERAL:
        return "char"
    return None


class SemanticChecker(_VISITOR_BASE):
    """
    Semantic checks aligned to your current grammar.

    Emits issues (dict):
      - undeclared
      - redeclared
      - use_before_declare (best-effort, same-line conservative)
      - unused
      - type_mismatch
      - return_type_mismatch
      - call_arity_mismatch
      - call_type_mismatch
      - break_outside_loop
      - continue_outside_loop
    """

    def __init__(self):
        super().__init__()
        self._issues: List[Dict[str, Any]] = []

        # scope stack: each scope is name -> _DeclInfo
        self._scopes: List[Dict[str, _DeclInfo]] = []
        self._decl_pos: Dict[Tuple[int, str], Tuple[int, int]] = {}

        # function signatures (global)
        self._funcs: Dict[str, _FuncSig] = {}

        # current function return type
        self._current_func_ret: Optional[str] = None

        # loop depth for break/continue validation
        self._loop_depth: int = 0

    # -----------------------------
    # Public API
    # -----------------------------
    def get_issues(self) -> List[Dict[str, Any]]:
        return list(self._issues)

    # -----------------------------
    # Helpers
    # -----------------------------
    def _push_scope(self) -> None:
        self._scopes.append({})

    def _pop_scope(self) -> Dict[str, _DeclInfo]:
        return self._scopes.pop()

    def _cur_scope(self) -> Dict[str, _DeclInfo]:
        if not self._scopes:
            self._push_scope()
        return self._scopes[-1]

    def _lookup(self, name: str) -> Optional[_DeclInfo]:
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        return None

    def _lookup_in_current(self, name: str) -> Optional[_DeclInfo]:
        return self._cur_scope().get(name)

    def _add_issue(self, kind: str, name: str, line: int, col: int, msg: str) -> None:
        self._issues.append({"kind": kind, "name": name, "line": line, "col": col, "msg": msg})

    def _emit_unused_for_scope(self, scope: Dict[str, _DeclInfo]) -> None:
        for name, info in scope.items():
            if info.ctype == "func":
                continue
            if not info.used:
                self._add_issue("unused", name, info.line, info.col, f"Variable '{name}' declared but never used")

    # -----------------------------
    # Types (simple ranks)
    # -----------------------------
    def _type_rank(self, t: str) -> int:
        # promotion: char -> int -> float
        if t == "char":
            return 0
        if t == "int":
            return 1
        if t == "float":
            return 2
        if t == "void":
            return -100
        return -1

    def _can_assign(self, lhs: str, rhs: str) -> bool:
        # Conservative: allow same type, or widening (char->int, int->float, char->float)
        # Disallow narrowing (float->int, int->char, float->char)
        return self._type_rank(rhs) <= self._type_rank(lhs)

    def _promote(self, a: str, b: str) -> str:
        return a if self._type_rank(a) >= self._type_rank(b) else b

    # -----------------------------
    # Expression type inference + call detection
    # -----------------------------
    def _infer_expr_type(self, ctx: Any) -> Optional[str]:
        if ctx is None:
            return None

        # Terminal
        if isinstance(ctx, TerminalNodeImpl):
            try:
                sym = ctx.getSymbol()
                if sym is None:
                    return None
                if sym.type == SimpleCParser.IDENTIFIER:
                    d = self._lookup(ctx.getText())
                    return d.ctype if d else None
                return _infer_literal_type_from_token_type(sym.type)
            except Exception:
                return None

        cls = ctx.__class__.__name__

        # primaryExpression: IDENTIFIER | literal | (expression)
        if cls == "PrimaryExpressionContext":
            try:
                ident = ctx.IDENTIFIER()
                if ident is not None:
                    d = self._lookup(ident.getText())
                    return d.ctype if d else None
            except Exception:
                pass
            try:
                # literals
                for tok_attr, tname in [("INTEGER", "int"), ("FLOAT_LITERAL", "float"), ("CHAR_LITERAL", "char")]:
                    fn = getattr(ctx, tok_attr, None)
                    if callable(fn) and fn() is not None:
                        return tname
            except Exception:
                pass
            try:
                inner = ctx.expression()
                if inner is not None:
                    return self._infer_expr_type(inner)
            except Exception:
                pass

        # postfixExpression: primaryExpression postfixPart*
        # If it includes a call "(...)" we treat type as function return type (if known).
        if cls == "PostfixExpressionContext":
            # detect f(...) calls: primary IDENTIFIER + postfixPart with LPAREN
            try:
                prim = ctx.primaryExpression()
                fname = None
                try:
                    ident = prim.IDENTIFIER()
                    if ident is not None:
                        fname = ident.getText()
                except Exception:
                    fname = None

                if fname:
                    # scan postfixPart for a call
                    parts = []
                    try:
                        parts = list(ctx.postfixPart())
                    except Exception:
                        parts = []

                    for p in parts:
                        if p.__class__.__name__ == "PostfixPartContext":
                            # p has LPAREN? RPAREN?
                            if getattr(p, "LPAREN", None) is not None:
                                # not reliable; fall back to text check
                                pass
                        txt = p.getText()
                        if txt.startswith("(") and txt.endswith(")"):
                            sig = self._funcs.get(fname)
                            if sig:
                                return sig.ret_type
                            return None
            except Exception:
                pass

            # array index / post inc/dec: type stays base type
            try:
                return self._infer_expr_type(ctx.primaryExpression())
            except Exception:
                return None

        # unaryExpression: postfixExpression | (op) unaryExpression
        if cls == "UnaryExpressionContext":
            try:
                return self._infer_expr_type(ctx.getChild(ctx.getChildCount() - 1))
            except Exception:
                return None

        # multiplicative / additive: promote
        if cls in {"MultiplicativeExpressionContext", "AdditiveExpressionContext"}:
            try:
                t = self._infer_expr_type(ctx.getChild(0))
                if t is None:
                    return None
                i = 2
                while i < ctx.getChildCount():
                    rhs = self._infer_expr_type(ctx.getChild(i))
                    if rhs is not None:
                        t = self._promote(t, rhs)
                    i += 2
                return t
            except Exception:
                return None

        # relational/equality/logical always produce int
        if cls in {"RelationalExpressionContext", "EqualityExpressionContext", "LogicalAndExpressionContext", "LogicalOrExpressionContext"}:
            return "int"

        # conditional: promote arms
        if cls == "ConditionalExpressionContext":
            try:
                if ctx.getChildCount() == 1:
                    return self._infer_expr_type(ctx.getChild(0))
                t1 = self._infer_expr_type(ctx.getChild(2))
                t2 = self._infer_expr_type(ctx.getChild(4))
                if t1 and t2:
                    return self._promote(t1, t2)
                return t1 or t2
            except Exception:
                return None

        # assignmentExpression: LHS type
        if cls == "AssignmentExpressionContext":
            try:
                if ctx.getChildCount() == 1:
                    return self._infer_expr_type(ctx.getChild(0))
                lhs_t = self._infer_expr_type(ctx.getChild(0))
                return lhs_t
            except Exception:
                return None

        # expression: comma operator => type of last
        if cls == "ExpressionContext":
            try:
                if ctx.getChildCount() == 1:
                    return self._infer_expr_type(ctx.getChild(0))
                return self._infer_expr_type(ctx.getChild(ctx.getChildCount() - 1))
            except Exception:
                return None

        # fallback: walk children
        try:
            for i in range(ctx.getChildCount()):
                t = self._infer_expr_type(ctx.getChild(i))
                if t is not None:
                    return t
        except Exception:
            pass

        return None

    # -----------------------------
    # Visitors
    # -----------------------------
    def visitProgram(self, ctx: SimpleCParser.ProgramContext):
        self._push_scope()
        out = self.visitChildren(ctx)
        self._emit_unused_for_scope(self._cur_scope())
        self._pop_scope()
        return out

    def visitFunctionDef(self, ctx: SimpleCParser.FunctionDefContext):
        # ret type + name
        try:
            rtype = ctx.typeSpecifier().getText()
        except Exception:
            rtype = None

        fname_node = None
        fname = None
        try:
            fname_node = ctx.IDENTIFIER()
            if fname_node is not None:
                fname = fname_node.getText()
        except Exception:
            fname = None

        if fname and rtype:
            line, col = _tok_line_col(fname_node)
            # function signature
            if fname in self._funcs:
                self._add_issue("redeclared", fname, line, col, f"Redeclaration of function '{fname}'")
            else:
                param_types: List[str] = []
                try:
                    pl = ctx.paramList()
                    if pl is not None:
                        for p in pl.param():
                            try:
                                param_types.append(p.typeSpecifier().getText())
                            except Exception:
                                param_types.append("?")
                except Exception:
                    pass
                self._funcs[fname] = _FuncSig(fname, rtype, param_types, line, col)

            # also store function name in global scope for undeclared checks
            if self._lookup_in_current(fname) is not None:
                self._add_issue("redeclared", fname, line, col, f"Redeclaration of '{fname}' in the same scope")
            else:
                self._cur_scope()[fname] = _DeclInfo(name=fname, ctype="func", line=line, col=col, used=True)

        prev_ret = self._current_func_ret
        self._current_func_ret = rtype

        # function scope
        self._push_scope()

        # params in function scope
        try:
            pl = ctx.paramList()
            if pl is not None:
                self.visit(pl)
        except Exception:
            pass

        # body
        out = self.visit(ctx.block())

        self._emit_unused_for_scope(self._cur_scope())
        self._pop_scope()

        self._current_func_ret = prev_ret
        return out

    def visitParam(self, ctx: SimpleCParser.ParamContext):
        try:
            name_node = ctx.IDENTIFIER()
            name = name_node.getText()
            ctype = ctx.typeSpecifier().getText()
            line, col = _tok_line_col(name_node)
        except Exception:
            return self.visitChildren(ctx)

        if self._lookup_in_current(name) is not None:
            self._add_issue("redeclared", name, line, col, f"Redeclaration of '{name}' in the same scope")
            return None

        depth = len(self._scopes) - 1
        self._cur_scope()[name] = _DeclInfo(name=name, ctype=ctype, line=line, col=col, used=False)
        self._decl_pos[(depth, name)] = (line, col)
        return None

    def visitBlock(self, ctx: SimpleCParser.BlockContext):
        self._push_scope()
        out = self.visitChildren(ctx)
        self._emit_unused_for_scope(self._cur_scope())
        self._pop_scope()
        return out

    def visitDeclaration(self, ctx: SimpleCParser.DeclarationContext):
        # declaration : declarationNoSemi SEMI ;
        try:
            dn = ctx.declarationNoSemi()
        except Exception:
            dn = None

        if dn is not None:
            return self.visit(dn)

        return None
    def visitDeclarationNoSemi(self, ctx: SimpleCParser.DeclarationNoSemiContext):
        # declarationNoSemi : typeSpecifier initDeclaratorList ;
        try:
            ctype = ctx.typeSpecifier().getText()
        except Exception:
            return None

        lst = None
        try:
            lst = ctx.initDeclaratorList()
        except Exception:
            lst = None

        if lst is None:
            return None

        for init_ctx in lst.initDeclarator():
            self._handle_init_declarator(init_ctx, ctype)

        return None

    def _handle_init_declarator(self, ctx: SimpleCParser.InitDeclaratorContext, ctype: str) -> None:
        ident = None
        try:
            ident = ctx.IDENTIFIER()
        except Exception:
            ident = None
        if ident is None:
            return

        name = ident.getText()
        line, col = _tok_line_col(ident)

        if self._lookup_in_current(name) is not None:
            self._add_issue("redeclared", name, line, col, f"Redeclaration of '{name}' in the same scope")
            return

        depth = len(self._scopes) - 1
        self._cur_scope()[name] = _DeclInfo(name=name, ctype=ctype, line=line, col=col, used=False)
        self._decl_pos[(depth, name)] = (line, col)

        # initializer type check
        try:
            expr = ctx.expression()
        except Exception:
            expr = None

        if expr is not None:
            rhs_t = self._infer_expr_type(expr)
            if rhs_t is not None and not self._can_assign(ctype, rhs_t):
                self._add_issue("type_mismatch", name, line, col, f"Cannot assign '{rhs_t}' to '{ctype}' for variable '{name}'")

    def visitReturnStatement(self, ctx: SimpleCParser.ReturnStatementContext):
        if self._current_func_ret is None:
            return self.visitChildren(ctx)

        expr = None
        try:
            expr = ctx.expression()
        except Exception:
            expr = None

        line, col = _tok_line_col(ctx)

        if self._current_func_ret == "void":
            if expr is not None:
                self._add_issue("return_type_mismatch", "", line, col, "Void function should not return a value")
            return self.visitChildren(ctx)

        if expr is None:
            self._add_issue(
                "return_type_mismatch",
                "",
                line,
                col,
                f"Non-void function should return a value of type '{self._current_func_ret}'",
            )
            return self.visitChildren(ctx)

        t = self._infer_expr_type(expr)
        if t is not None and not self._can_assign(self._current_func_ret, t):
            self._add_issue(
                "return_type_mismatch",
                "",
                line,
                col,
                f"Return type '{t}' not compatible with function return type '{self._current_func_ret}'",
            )

        return self.visitChildren(ctx)

    def visitWhileStatement(self, ctx: SimpleCParser.WhileStatementContext):
        self._loop_depth += 1
        out = self.visitChildren(ctx)
        self._loop_depth -= 1
        return out

    def visitForStatement(self, ctx: SimpleCParser.ForStatementContext):
        # forStatement : FOR LPAREN forInit? SEMI expression? SEMI expression? RPAREN statement ;

        # Enter loop context (for break/continue validation)
        self._loop_depth += 1

        # The for-loop introduces its own scope in C when init contains a declaration.
        # We will ALWAYS push a scope here; it's safe and matches typical C behavior.
        self._push_scope()

        # Visit init first so declared vars (e.g., int i=0) exist for cond/update/body
        try:
            fi = ctx.forInit()
            if fi is not None:
                self.visit(fi)
        except Exception:
            pass

        # Visit condition expression (optional)
        try:
            # expression() appears 0..2 times here: cond and update
            exprs = list(ctx.expression())
            if len(exprs) >= 1 and exprs[0] is not None:
                self.visit(exprs[0])
            if len(exprs) >= 2 and exprs[1] is not None:
                self.visit(exprs[1])
        except Exception:
            pass

        # Visit the loop body statement
        out = None
        try:
            st = ctx.statement()
            out = self.visit(st) if st is not None else self.visitChildren(ctx)
        except Exception:
            out = self.visitChildren(ctx)

        # End loop scope
        self._emit_unused_for_scope(self._cur_scope())
        self._pop_scope()

        # Exit loop context
        self._loop_depth -= 1
        return out

    def visitBreakStatement(self, ctx: SimpleCParser.BreakStatementContext):
        if self._loop_depth <= 0:
            line, col = _tok_line_col(ctx)
            self._add_issue("break_outside_loop", "", line, col, "break used outside of a loop")
        return self.visitChildren(ctx)

    def visitContinueStatement(self, ctx: SimpleCParser.ContinueStatementContext):
        if self._loop_depth <= 0:
            line, col = _tok_line_col(ctx)
            self._add_issue("continue_outside_loop", "", line, col, "continue used outside of a loop")
        return self.visitChildren(ctx)

    def visitAssignStmt(self, ctx):
        # your grammar doesn't have AssignStmtContext anymore; ignore if present in older generated code
        return self.visitChildren(ctx)

    def visitTerminal(self, node: TerminalNodeImpl):
        if not _is_identifier_terminal(node):
            return None

        parent = getattr(node, "parentCtx", None)
        if parent is not None:
            pname = parent.__class__.__name__
            # don't count declaration identifiers
            if pname in {"InitDeclaratorContext", "ParamContext", "FunctionDefContext"}:
                return None

        name = node.getText()
        line, col = _tok_line_col(node)

        decl = self._lookup(name)
        if decl is None:
            self._add_issue("undeclared", name, line, col, f"Use of undeclared identifier '{name}'")
            return None

        # use-before-declare (same-line heuristic)
        depth = len(self._scopes) - 1
        if (depth, name) in self._decl_pos:
            dline, dcol = self._decl_pos[(depth, name)]
            if line == dline and col < dcol:
                self._add_issue("use_before_declare", name, line, col, f"Identifier '{name}' used before its declaration in the same scope")

        if decl.ctype != "func":
            decl.used = True

        return None

    # -----------------------------
    # Function call validation
    # -----------------------------
    def visitPostfixExpression(self, ctx: SimpleCParser.PostfixExpressionContext):
        # Detect f(...) and validate args
        try:
            prim = ctx.primaryExpression()
        except Exception:
            prim = None

        fname = None
        try:
            if prim is not None and prim.IDENTIFIER() is not None:
                fname = prim.IDENTIFIER().getText()
        except Exception:
            fname = None

        if not fname:
            return self.visitChildren(ctx)

        # find a call postfixPart: '(' argumentList? ')'
        call_parts = []
        try:
            call_parts = list(ctx.postfixPart())
        except Exception:
            call_parts = []

        for p in call_parts:
            txt = p.getText()
            if txt.startswith("(") and txt.endswith(")"):
                sig = self._funcs.get(fname)
                if sig is None:
                    # if it's not a known function, treat as undeclared use of identifier (already handled by visitTerminal)
                    continue

                # count argument expressions
                arg_types: List[Optional[str]] = []
                try:
                    al = p.argumentList()
                except Exception:
                    al = None

                if al is not None:
                    try:
                        # argumentList: assignmentExpression (COMMA assignmentExpression)*
                        for ae in al.assignmentExpression():
                            arg_types.append(self._infer_expr_type(ae))
                    except Exception:
                        pass

                # arity check
                if len(arg_types) != len(sig.param_types):
                    line, col = _tok_line_col(prim.IDENTIFIER())
                    self._add_issue(
                        "call_arity_mismatch",
                        fname,
                        line,
                        col,
                        f"Function '{fname}' expects {len(sig.param_types)} argument(s) but got {len(arg_types)}",
                    )
                else:
                    # type check
                    for i, (got, expected) in enumerate(zip(arg_types, sig.param_types), start=1):
                        if got is None:
                            continue
                        if not self._can_assign(expected, got):
                            line, col = _tok_line_col(prim.IDENTIFIER())
                            self._add_issue(
                                "call_type_mismatch",
                                fname,
                                line,
                                col,
                                f"Argument {i} of '{fname}' expects '{expected}' but got '{got}'",
                            )

        return self.visitChildren(ctx)