from typing import Dict, Any

from generated.SimpleCVisitor import SimpleCVisitor
from generated.SimpleCParser import SimpleCParser


class SymbolTableBuilder(SimpleCVisitor):
    """
    Builds a simple flat symbol table:
      name -> {"kind": "var"|"param"|"func", "type": <type>, "line": <line>}
    Note: flat table is fine for deterministic typo correction (conservative).
    """

    def __init__(self):
        super().__init__()
        self.symbols: Dict[str, Dict[str, Any]] = {}

    def _type_text(self, type_ctx) -> str:
        return type_ctx.getText() if type_ctx else "?"

    def _add_symbol(self, name: str, kind: str, typ: str, line: int):
        if name and name not in self.symbols:
            self.symbols[name] = {"kind": kind, "type": typ, "line": line}

    # -------------------------
    # Functions / Params
    # -------------------------
    def visitFunctionDef(self, ctx: SimpleCParser.FunctionDefContext):
        ret_type = self._type_text(ctx.typeSpecifier())

        fn_ident = ctx.IDENTIFIER()
        if fn_ident is not None:
            name = fn_ident.getText()
            line = fn_ident.symbol.line if hasattr(fn_ident, "symbol") else -1
            self._add_symbol(name, "func", ret_type, line)

        return self.visitChildren(ctx)

    def visitParam(self, ctx: SimpleCParser.ParamContext):
        typ = self._type_text(ctx.typeSpecifier())
        ident = ctx.IDENTIFIER()
        if ident is not None:
            name = ident.getText()
            line = ident.symbol.line if hasattr(ident, "symbol") else -1
            self._add_symbol(name, "param", typ, line)

        return self.visitChildren(ctx)

    # -------------------------
    # Declarations (normal)
    # -------------------------
    def visitDeclaration(self, ctx: SimpleCParser.DeclarationContext):
        """
        declaration : typeSpecifier initDeclaratorList SEMI
                   | declarationNoSemi SEMI        (if you rewired grammar this way)
        We handle both safely by probing what exists.
        """
        # Case 1: direct typeSpecifier/initDeclaratorList
        type_ctx = getattr(ctx, "typeSpecifier", None)
        list_ctx = getattr(ctx, "initDeclaratorList", None)

        if callable(type_ctx) and callable(list_ctx):
            typ = self._type_text(ctx.typeSpecifier())
            lst = ctx.initDeclaratorList()
            if lst is None:
                return self.visitChildren(ctx)
            for init_ctx in lst.initDeclarator():
                ident = init_ctx.IDENTIFIER()
                if ident is None:
                    continue
                name = ident.getText()
                line = ident.symbol.line if hasattr(ident, "symbol") else -1
                self._add_symbol(name, "var", typ, line)
            return self.visitChildren(ctx)

        # Case 2: wrapped declarationNoSemi
        dn = None
        try:
            dn = ctx.declarationNoSemi()
        except Exception:
            dn = None

        if dn is not None:
            return self.visit(dn)

        return self.visitChildren(ctx)

    def visitDeclarationNoSemi(self, ctx: SimpleCParser.DeclarationNoSemiContext):
        """
        declarationNoSemi : typeSpecifier initDeclaratorList ;
        Used inside forInit.
        """
        typ = self._type_text(ctx.typeSpecifier())
        lst = ctx.initDeclaratorList()
        if lst is None:
            return self.visitChildren(ctx)

        for init_ctx in lst.initDeclarator():
            ident = init_ctx.IDENTIFIER()
            if ident is None:
                continue
            name = ident.getText()
            line = ident.symbol.line if hasattr(ident, "symbol") else -1
            self._add_symbol(name, "var", typ, line)

        return self.visitChildren(ctx)

    def get_symbols(self) -> Dict[str, Dict[str, Any]]:
        return dict(self.symbols)