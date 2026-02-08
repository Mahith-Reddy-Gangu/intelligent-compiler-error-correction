# Generated from SimpleC.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,13,50,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,5,2,27,8,2,10,
        2,12,2,30,9,2,1,3,1,3,1,3,3,3,35,8,3,1,4,1,4,1,4,1,4,1,5,1,5,1,5,
        1,5,1,5,1,6,1,6,1,6,1,6,1,6,0,0,7,0,2,4,6,8,10,12,0,0,45,0,14,1,
        0,0,0,2,17,1,0,0,0,4,28,1,0,0,0,6,34,1,0,0,0,8,36,1,0,0,0,10,40,
        1,0,0,0,12,45,1,0,0,0,14,15,3,2,1,0,15,16,5,0,0,1,16,1,1,0,0,0,17,
        18,5,7,0,0,18,19,5,9,0,0,19,20,5,1,0,0,20,21,5,2,0,0,21,22,5,3,0,
        0,22,23,3,4,2,0,23,24,5,4,0,0,24,3,1,0,0,0,25,27,3,6,3,0,26,25,1,
        0,0,0,27,30,1,0,0,0,28,26,1,0,0,0,28,29,1,0,0,0,29,5,1,0,0,0,30,
        28,1,0,0,0,31,35,3,8,4,0,32,35,3,10,5,0,33,35,3,12,6,0,34,31,1,0,
        0,0,34,32,1,0,0,0,34,33,1,0,0,0,35,7,1,0,0,0,36,37,5,7,0,0,37,38,
        5,10,0,0,38,39,5,5,0,0,39,9,1,0,0,0,40,41,5,10,0,0,41,42,5,6,0,0,
        42,43,5,11,0,0,43,44,5,5,0,0,44,11,1,0,0,0,45,46,5,8,0,0,46,47,5,
        11,0,0,47,48,5,5,0,0,48,13,1,0,0,0,2,28,34
    ]

class SimpleCParser ( Parser ):

    grammarFileName = "SimpleC.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'{'", "'}'", "';'", "'='", 
                     "'int'", "'return'", "'main'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "INT", "RETURN", 
                      "MAIN", "IDENTIFIER", "INTEGER", "WS", "COMMENT" ]

    RULE_program = 0
    RULE_mainFunction = 1
    RULE_statementList = 2
    RULE_statement = 3
    RULE_variableDeclaration = 4
    RULE_assignment = 5
    RULE_returnStatement = 6

    ruleNames =  [ "program", "mainFunction", "statementList", "statement", 
                   "variableDeclaration", "assignment", "returnStatement" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    INT=7
    RETURN=8
    MAIN=9
    IDENTIFIER=10
    INTEGER=11
    WS=12
    COMMENT=13

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def mainFunction(self):
            return self.getTypedRuleContext(SimpleCParser.MainFunctionContext,0)


        def EOF(self):
            return self.getToken(SimpleCParser.EOF, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = SimpleCParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self.mainFunction()
            self.state = 15
            self.match(SimpleCParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MainFunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(SimpleCParser.INT, 0)

        def MAIN(self):
            return self.getToken(SimpleCParser.MAIN, 0)

        def statementList(self):
            return self.getTypedRuleContext(SimpleCParser.StatementListContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_mainFunction

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMainFunction" ):
                listener.enterMainFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMainFunction" ):
                listener.exitMainFunction(self)




    def mainFunction(self):

        localctx = SimpleCParser.MainFunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_mainFunction)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self.match(SimpleCParser.INT)
            self.state = 18
            self.match(SimpleCParser.MAIN)
            self.state = 19
            self.match(SimpleCParser.T__0)
            self.state = 20
            self.match(SimpleCParser.T__1)
            self.state = 21
            self.match(SimpleCParser.T__2)
            self.state = 22
            self.statementList()
            self.state = 23
            self.match(SimpleCParser.T__3)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.StatementContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.StatementContext,i)


        def getRuleIndex(self):
            return SimpleCParser.RULE_statementList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatementList" ):
                listener.enterStatementList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatementList" ):
                listener.exitStatementList(self)




    def statementList(self):

        localctx = SimpleCParser.StatementListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_statementList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 28
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1408) != 0):
                self.state = 25
                self.statement()
                self.state = 30
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variableDeclaration(self):
            return self.getTypedRuleContext(SimpleCParser.VariableDeclarationContext,0)


        def assignment(self):
            return self.getTypedRuleContext(SimpleCParser.AssignmentContext,0)


        def returnStatement(self):
            return self.getTypedRuleContext(SimpleCParser.ReturnStatementContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)




    def statement(self):

        localctx = SimpleCParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_statement)
        try:
            self.state = 34
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7]:
                self.enterOuterAlt(localctx, 1)
                self.state = 31
                self.variableDeclaration()
                pass
            elif token in [10]:
                self.enterOuterAlt(localctx, 2)
                self.state = 32
                self.assignment()
                pass
            elif token in [8]:
                self.enterOuterAlt(localctx, 3)
                self.state = 33
                self.returnStatement()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(SimpleCParser.INT, 0)

        def IDENTIFIER(self):
            return self.getToken(SimpleCParser.IDENTIFIER, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_variableDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariableDeclaration" ):
                listener.enterVariableDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariableDeclaration" ):
                listener.exitVariableDeclaration(self)




    def variableDeclaration(self):

        localctx = SimpleCParser.VariableDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_variableDeclaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self.match(SimpleCParser.INT)
            self.state = 37
            self.match(SimpleCParser.IDENTIFIER)
            self.state = 38
            self.match(SimpleCParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(SimpleCParser.IDENTIFIER, 0)

        def INTEGER(self):
            return self.getToken(SimpleCParser.INTEGER, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)




    def assignment(self):

        localctx = SimpleCParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40
            self.match(SimpleCParser.IDENTIFIER)
            self.state = 41
            self.match(SimpleCParser.T__5)
            self.state = 42
            self.match(SimpleCParser.INTEGER)
            self.state = 43
            self.match(SimpleCParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(SimpleCParser.RETURN, 0)

        def INTEGER(self):
            return self.getToken(SimpleCParser.INTEGER, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_returnStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStatement" ):
                listener.enterReturnStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStatement" ):
                listener.exitReturnStatement(self)




    def returnStatement(self):

        localctx = SimpleCParser.ReturnStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_returnStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self.match(SimpleCParser.RETURN)
            self.state = 46
            self.match(SimpleCParser.INTEGER)
            self.state = 47
            self.match(SimpleCParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





