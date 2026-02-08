from antlr4 import ParseTreeWalker

from SimpleCListener import SimpleCListener
from .symbol_table import SymbolTable


class DeclarationAnalysisListener(SimpleCListener):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []

    def enterVariableDeclaration(self, ctx):
        name = ctx.IDENTIFIER().getText()
        self.symbol_table.declare(name, ctx.start.line)

    def enterAssignment(self, ctx):
        name = ctx.IDENTIFIER().getText()
        if not self.symbol_table.is_declared(name):
            self.errors.append(
                f"Line {ctx.start.line}: assignment to undeclared variable '{name}'"
            )


def analyze_parse_tree(tree):
    walker = ParseTreeWalker()
    listener = DeclarationAnalysisListener()
    walker.walk(listener, tree)

    return {
        "symbol_table": listener.symbol_table,
        "errors": listener.errors,
    }
