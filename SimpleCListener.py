# Generated from SimpleC.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SimpleCParser import SimpleCParser
else:
    from SimpleCParser import SimpleCParser

# This class defines a complete listener for a parse tree produced by SimpleCParser.
class SimpleCListener(ParseTreeListener):

    # Enter a parse tree produced by SimpleCParser#program.
    def enterProgram(self, ctx:SimpleCParser.ProgramContext):
        pass

    # Exit a parse tree produced by SimpleCParser#program.
    def exitProgram(self, ctx:SimpleCParser.ProgramContext):
        pass


    # Enter a parse tree produced by SimpleCParser#mainFunction.
    def enterMainFunction(self, ctx:SimpleCParser.MainFunctionContext):
        pass

    # Exit a parse tree produced by SimpleCParser#mainFunction.
    def exitMainFunction(self, ctx:SimpleCParser.MainFunctionContext):
        pass


    # Enter a parse tree produced by SimpleCParser#statementList.
    def enterStatementList(self, ctx:SimpleCParser.StatementListContext):
        pass

    # Exit a parse tree produced by SimpleCParser#statementList.
    def exitStatementList(self, ctx:SimpleCParser.StatementListContext):
        pass


    # Enter a parse tree produced by SimpleCParser#statement.
    def enterStatement(self, ctx:SimpleCParser.StatementContext):
        pass

    # Exit a parse tree produced by SimpleCParser#statement.
    def exitStatement(self, ctx:SimpleCParser.StatementContext):
        pass


    # Enter a parse tree produced by SimpleCParser#variableDeclaration.
    def enterVariableDeclaration(self, ctx:SimpleCParser.VariableDeclarationContext):
        pass

    # Exit a parse tree produced by SimpleCParser#variableDeclaration.
    def exitVariableDeclaration(self, ctx:SimpleCParser.VariableDeclarationContext):
        pass


    # Enter a parse tree produced by SimpleCParser#assignment.
    def enterAssignment(self, ctx:SimpleCParser.AssignmentContext):
        pass

    # Exit a parse tree produced by SimpleCParser#assignment.
    def exitAssignment(self, ctx:SimpleCParser.AssignmentContext):
        pass


    # Enter a parse tree produced by SimpleCParser#returnStatement.
    def enterReturnStatement(self, ctx:SimpleCParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by SimpleCParser#returnStatement.
    def exitReturnStatement(self, ctx:SimpleCParser.ReturnStatementContext):
        pass



del SimpleCParser