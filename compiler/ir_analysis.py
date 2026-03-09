from __future__ import annotations

from antlr4 import ParseTreeWalker

from generated.SimpleCListener import SimpleCListener
from .symbol_table import SymbolTable


def _get_identifier_text(ctx) -> str:
    """
    Safely extract IDENTIFIER token text from a context.
    If your grammar uses a different token name, add it here.
    """
    # Most grammars: IDENTIFIER()
    if hasattr(ctx, "IDENTIFIER") and ctx.IDENTIFIER() is not None:
        return ctx.IDENTIFIER().getText()

    # Common alternative token name: ID()
    if hasattr(ctx, "ID") and ctx.ID() is not None:
        return ctx.ID().getText()

    # Fallback: try getText() but that might include more than just the id
    return ctx.getText()


class DeclarationAnalysisListener(SimpleCListener):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []

    def enterVariableDeclaration(self, ctx):
        name = _get_identifier_text(ctx)
        ok = self.symbol_table.declare(name, ctx.start.line)
        if not ok:
            prev = self.symbol_table.declared_line(name)
            self.errors.append(
                f"Line {ctx.start.line}: redeclaration of variable '{name}' (previous at line {prev})"
            )

    def enterAssignment(self, ctx):
        name = _get_identifier_text(ctx)
        if not self.symbol_table.is_declared(name):
            self.errors.append(
                f"Line {ctx.start.line}: assignment to undeclared variable '{name}'"
            )


def analyze_parse_tree(tree):
    walker = ParseTreeWalker()
    listener = DeclarationAnalysisListener()
    walker.walk(listener, tree)

    # return a printable dict for convenience
    return {
        "symbol_table": listener.symbol_table.to_dict(),
        "errors": listener.errors,
    }