# Generated from grammar/SimpleC.g4 by ANTLR 4.13.2
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
        4,1,51,331,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,1,0,4,0,76,8,0,11,0,12,0,77,1,
        0,1,0,1,1,1,1,1,1,1,1,3,1,86,8,1,1,1,1,1,1,1,1,2,1,2,1,2,5,2,94,
        8,2,10,2,12,2,97,9,2,1,3,1,3,1,3,3,3,102,8,3,1,4,1,4,5,4,106,8,4,
        10,4,12,4,109,9,4,1,4,1,4,1,5,1,5,3,5,115,8,5,1,6,1,6,1,6,1,7,1,
        7,1,7,1,8,1,8,1,8,5,8,126,8,8,10,8,12,8,129,9,8,1,9,1,9,3,9,133,
        8,9,1,9,1,9,3,9,137,8,9,1,10,1,10,3,10,141,8,10,1,10,4,10,144,8,
        10,11,10,12,10,145,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,
        3,11,157,8,11,1,12,1,12,1,13,3,13,162,8,13,1,13,1,13,1,14,1,14,1,
        14,1,14,1,14,1,14,1,14,3,14,173,8,14,1,15,1,15,1,15,1,15,1,15,1,
        15,1,16,1,16,1,16,3,16,184,8,16,1,16,1,16,3,16,188,8,16,1,16,1,16,
        3,16,192,8,16,1,16,1,16,1,16,1,17,1,17,3,17,199,8,17,1,18,1,18,3,
        18,203,8,18,1,18,1,18,1,19,1,19,1,19,1,20,1,20,1,20,1,21,1,21,1,
        21,5,21,216,8,21,10,21,12,21,219,9,21,1,22,1,22,1,22,1,22,1,22,3,
        22,226,8,22,1,23,1,23,1,24,1,24,1,24,1,24,1,24,1,24,3,24,236,8,24,
        1,25,1,25,1,25,5,25,241,8,25,10,25,12,25,244,9,25,1,26,1,26,1,26,
        5,26,249,8,26,10,26,12,26,252,9,26,1,27,1,27,1,27,5,27,257,8,27,
        10,27,12,27,260,9,27,1,28,1,28,1,28,5,28,265,8,28,10,28,12,28,268,
        9,28,1,29,1,29,1,29,5,29,273,8,29,10,29,12,29,276,9,29,1,30,1,30,
        1,30,5,30,281,8,30,10,30,12,30,284,9,30,1,31,1,31,1,31,3,31,289,
        8,31,1,32,1,32,5,32,293,8,32,10,32,12,32,296,9,32,1,33,1,33,1,33,
        1,33,1,33,1,33,3,33,304,8,33,1,33,1,33,1,33,3,33,309,8,33,1,34,1,
        34,1,34,5,34,314,8,34,10,34,12,34,317,9,34,1,35,1,35,1,35,1,35,1,
        35,1,35,1,35,1,35,3,35,327,8,35,1,36,1,36,1,36,0,0,37,0,2,4,6,8,
        10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,
        54,56,58,60,62,64,66,68,70,72,0,7,2,0,14,18,33,33,1,0,19,20,2,0,
        21,22,30,31,1,0,25,26,1,0,27,29,3,0,12,13,25,26,32,32,1,0,1,4,339,
        0,75,1,0,0,0,2,81,1,0,0,0,4,90,1,0,0,0,6,98,1,0,0,0,8,103,1,0,0,
        0,10,114,1,0,0,0,12,116,1,0,0,0,14,119,1,0,0,0,16,122,1,0,0,0,18,
        130,1,0,0,0,20,143,1,0,0,0,22,156,1,0,0,0,24,158,1,0,0,0,26,161,
        1,0,0,0,28,165,1,0,0,0,30,174,1,0,0,0,32,180,1,0,0,0,34,198,1,0,
        0,0,36,200,1,0,0,0,38,206,1,0,0,0,40,209,1,0,0,0,42,212,1,0,0,0,
        44,225,1,0,0,0,46,227,1,0,0,0,48,229,1,0,0,0,50,237,1,0,0,0,52,245,
        1,0,0,0,54,253,1,0,0,0,56,261,1,0,0,0,58,269,1,0,0,0,60,277,1,0,
        0,0,62,288,1,0,0,0,64,290,1,0,0,0,66,308,1,0,0,0,68,310,1,0,0,0,
        70,326,1,0,0,0,72,328,1,0,0,0,74,76,3,2,1,0,75,74,1,0,0,0,76,77,
        1,0,0,0,77,75,1,0,0,0,77,78,1,0,0,0,78,79,1,0,0,0,79,80,5,0,0,1,
        80,1,1,0,0,0,81,82,3,72,36,0,82,83,5,44,0,0,83,85,5,38,0,0,84,86,
        3,4,2,0,85,84,1,0,0,0,85,86,1,0,0,0,86,87,1,0,0,0,87,88,5,39,0,0,
        88,89,3,8,4,0,89,3,1,0,0,0,90,95,3,6,3,0,91,92,5,36,0,0,92,94,3,
        6,3,0,93,91,1,0,0,0,94,97,1,0,0,0,95,93,1,0,0,0,95,96,1,0,0,0,96,
        5,1,0,0,0,97,95,1,0,0,0,98,99,3,72,36,0,99,101,5,44,0,0,100,102,
        3,20,10,0,101,100,1,0,0,0,101,102,1,0,0,0,102,7,1,0,0,0,103,107,
        5,40,0,0,104,106,3,10,5,0,105,104,1,0,0,0,106,109,1,0,0,0,107,105,
        1,0,0,0,107,108,1,0,0,0,108,110,1,0,0,0,109,107,1,0,0,0,110,111,
        5,41,0,0,111,9,1,0,0,0,112,115,3,12,6,0,113,115,3,22,11,0,114,112,
        1,0,0,0,114,113,1,0,0,0,115,11,1,0,0,0,116,117,3,14,7,0,117,118,
        5,37,0,0,118,13,1,0,0,0,119,120,3,72,36,0,120,121,3,16,8,0,121,15,
        1,0,0,0,122,127,3,18,9,0,123,124,5,36,0,0,124,126,3,18,9,0,125,123,
        1,0,0,0,126,129,1,0,0,0,127,125,1,0,0,0,127,128,1,0,0,0,128,17,1,
        0,0,0,129,127,1,0,0,0,130,132,5,44,0,0,131,133,3,20,10,0,132,131,
        1,0,0,0,132,133,1,0,0,0,133,136,1,0,0,0,134,135,5,33,0,0,135,137,
        3,42,21,0,136,134,1,0,0,0,136,137,1,0,0,0,137,19,1,0,0,0,138,140,
        5,42,0,0,139,141,3,42,21,0,140,139,1,0,0,0,140,141,1,0,0,0,141,142,
        1,0,0,0,142,144,5,43,0,0,143,138,1,0,0,0,144,145,1,0,0,0,145,143,
        1,0,0,0,145,146,1,0,0,0,146,21,1,0,0,0,147,157,3,24,12,0,148,157,
        3,26,13,0,149,157,3,28,14,0,150,157,3,30,15,0,151,157,3,32,16,0,
        152,157,3,36,18,0,153,157,3,38,19,0,154,157,3,40,20,0,155,157,3,
        8,4,0,156,147,1,0,0,0,156,148,1,0,0,0,156,149,1,0,0,0,156,150,1,
        0,0,0,156,151,1,0,0,0,156,152,1,0,0,0,156,153,1,0,0,0,156,154,1,
        0,0,0,156,155,1,0,0,0,157,23,1,0,0,0,158,159,5,37,0,0,159,25,1,0,
        0,0,160,162,3,42,21,0,161,160,1,0,0,0,161,162,1,0,0,0,162,163,1,
        0,0,0,163,164,5,37,0,0,164,27,1,0,0,0,165,166,5,6,0,0,166,167,5,
        38,0,0,167,168,3,42,21,0,168,169,5,39,0,0,169,172,3,22,11,0,170,
        171,5,7,0,0,171,173,3,22,11,0,172,170,1,0,0,0,172,173,1,0,0,0,173,
        29,1,0,0,0,174,175,5,8,0,0,175,176,5,38,0,0,176,177,3,42,21,0,177,
        178,5,39,0,0,178,179,3,22,11,0,179,31,1,0,0,0,180,181,5,9,0,0,181,
        183,5,38,0,0,182,184,3,34,17,0,183,182,1,0,0,0,183,184,1,0,0,0,184,
        185,1,0,0,0,185,187,5,37,0,0,186,188,3,42,21,0,187,186,1,0,0,0,187,
        188,1,0,0,0,188,189,1,0,0,0,189,191,5,37,0,0,190,192,3,42,21,0,191,
        190,1,0,0,0,191,192,1,0,0,0,192,193,1,0,0,0,193,194,5,39,0,0,194,
        195,3,22,11,0,195,33,1,0,0,0,196,199,3,14,7,0,197,199,3,42,21,0,
        198,196,1,0,0,0,198,197,1,0,0,0,199,35,1,0,0,0,200,202,5,5,0,0,201,
        203,3,42,21,0,202,201,1,0,0,0,202,203,1,0,0,0,203,204,1,0,0,0,204,
        205,5,37,0,0,205,37,1,0,0,0,206,207,5,10,0,0,207,208,5,37,0,0,208,
        39,1,0,0,0,209,210,5,11,0,0,210,211,5,37,0,0,211,41,1,0,0,0,212,
        217,3,44,22,0,213,214,5,36,0,0,214,216,3,44,22,0,215,213,1,0,0,0,
        216,219,1,0,0,0,217,215,1,0,0,0,217,218,1,0,0,0,218,43,1,0,0,0,219,
        217,1,0,0,0,220,226,3,48,24,0,221,222,3,62,31,0,222,223,3,46,23,
        0,223,224,3,44,22,0,224,226,1,0,0,0,225,220,1,0,0,0,225,221,1,0,
        0,0,226,45,1,0,0,0,227,228,7,0,0,0,228,47,1,0,0,0,229,235,3,50,25,
        0,230,231,5,34,0,0,231,232,3,42,21,0,232,233,5,35,0,0,233,234,3,
        48,24,0,234,236,1,0,0,0,235,230,1,0,0,0,235,236,1,0,0,0,236,49,1,
        0,0,0,237,242,3,52,26,0,238,239,5,24,0,0,239,241,3,52,26,0,240,238,
        1,0,0,0,241,244,1,0,0,0,242,240,1,0,0,0,242,243,1,0,0,0,243,51,1,
        0,0,0,244,242,1,0,0,0,245,250,3,54,27,0,246,247,5,23,0,0,247,249,
        3,54,27,0,248,246,1,0,0,0,249,252,1,0,0,0,250,248,1,0,0,0,250,251,
        1,0,0,0,251,53,1,0,0,0,252,250,1,0,0,0,253,258,3,56,28,0,254,255,
        7,1,0,0,255,257,3,56,28,0,256,254,1,0,0,0,257,260,1,0,0,0,258,256,
        1,0,0,0,258,259,1,0,0,0,259,55,1,0,0,0,260,258,1,0,0,0,261,266,3,
        58,29,0,262,263,7,2,0,0,263,265,3,58,29,0,264,262,1,0,0,0,265,268,
        1,0,0,0,266,264,1,0,0,0,266,267,1,0,0,0,267,57,1,0,0,0,268,266,1,
        0,0,0,269,274,3,60,30,0,270,271,7,3,0,0,271,273,3,60,30,0,272,270,
        1,0,0,0,273,276,1,0,0,0,274,272,1,0,0,0,274,275,1,0,0,0,275,59,1,
        0,0,0,276,274,1,0,0,0,277,282,3,62,31,0,278,279,7,4,0,0,279,281,
        3,62,31,0,280,278,1,0,0,0,281,284,1,0,0,0,282,280,1,0,0,0,282,283,
        1,0,0,0,283,61,1,0,0,0,284,282,1,0,0,0,285,289,3,64,32,0,286,287,
        7,5,0,0,287,289,3,62,31,0,288,285,1,0,0,0,288,286,1,0,0,0,289,63,
        1,0,0,0,290,294,3,70,35,0,291,293,3,66,33,0,292,291,1,0,0,0,293,
        296,1,0,0,0,294,292,1,0,0,0,294,295,1,0,0,0,295,65,1,0,0,0,296,294,
        1,0,0,0,297,298,5,42,0,0,298,299,3,42,21,0,299,300,5,43,0,0,300,
        309,1,0,0,0,301,303,5,38,0,0,302,304,3,68,34,0,303,302,1,0,0,0,303,
        304,1,0,0,0,304,305,1,0,0,0,305,309,5,39,0,0,306,309,5,12,0,0,307,
        309,5,13,0,0,308,297,1,0,0,0,308,301,1,0,0,0,308,306,1,0,0,0,308,
        307,1,0,0,0,309,67,1,0,0,0,310,315,3,44,22,0,311,312,5,36,0,0,312,
        314,3,44,22,0,313,311,1,0,0,0,314,317,1,0,0,0,315,313,1,0,0,0,315,
        316,1,0,0,0,316,69,1,0,0,0,317,315,1,0,0,0,318,327,5,44,0,0,319,
        327,5,45,0,0,320,327,5,46,0,0,321,327,5,47,0,0,322,323,5,38,0,0,
        323,324,3,42,21,0,324,325,5,39,0,0,325,327,1,0,0,0,326,318,1,0,0,
        0,326,319,1,0,0,0,326,320,1,0,0,0,326,321,1,0,0,0,326,322,1,0,0,
        0,327,71,1,0,0,0,328,329,7,6,0,0,329,73,1,0,0,0,34,77,85,95,101,
        107,114,127,132,136,140,145,156,161,172,183,187,191,198,202,217,
        225,235,242,250,258,266,274,282,288,294,303,308,315,326
    ]

class SimpleCParser ( Parser ):

    grammarFileName = "SimpleC.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'int'", "'float'", "'char'", "'void'", 
                     "'return'", "'if'", "'else'", "'while'", "'for'", "'break'", 
                     "'continue'", "'++'", "'--'", "'+='", "'-='", "'*='", 
                     "'/='", "'%='", "'=='", "'!='", "'<='", "'>='", "'&&'", 
                     "'||'", "'+'", "'-'", "'*'", "'/'", "'%'", "'<'", "'>'", 
                     "'!'", "'='", "'?'", "':'", "','", "';'", "'('", "')'", 
                     "'{'", "'}'", "'['", "']'" ]

    symbolicNames = [ "<INVALID>", "INT", "FLOAT", "CHAR", "VOID", "RETURN", 
                      "IF", "ELSE", "WHILE", "FOR", "BREAK", "CONTINUE", 
                      "INC", "DEC", "ADD_ASSIGN", "SUB_ASSIGN", "MUL_ASSIGN", 
                      "DIV_ASSIGN", "MOD_ASSIGN", "EQ", "NEQ", "LTE", "GTE", 
                      "AND", "OR", "PLUS", "MINUS", "MUL", "DIV", "MOD", 
                      "LT", "GT", "NOT", "ASSIGN", "QUESTION", "COLON", 
                      "COMMA", "SEMI", "LPAREN", "RPAREN", "LBRACE", "RBRACE", 
                      "LBRACK", "RBRACK", "IDENTIFIER", "INTEGER", "FLOAT_LITERAL", 
                      "CHAR_LITERAL", "WS", "LINE_COMMENT", "BLOCK_COMMENT", 
                      "ERROR_CHAR" ]

    RULE_program = 0
    RULE_functionDef = 1
    RULE_paramList = 2
    RULE_param = 3
    RULE_block = 4
    RULE_blockItem = 5
    RULE_declaration = 6
    RULE_declarationNoSemi = 7
    RULE_initDeclaratorList = 8
    RULE_initDeclarator = 9
    RULE_arraySuffix = 10
    RULE_statement = 11
    RULE_emptyStatement = 12
    RULE_exprStatement = 13
    RULE_ifStatement = 14
    RULE_whileStatement = 15
    RULE_forStatement = 16
    RULE_forInit = 17
    RULE_returnStatement = 18
    RULE_breakStatement = 19
    RULE_continueStatement = 20
    RULE_expression = 21
    RULE_assignmentExpression = 22
    RULE_assignmentOperator = 23
    RULE_conditionalExpression = 24
    RULE_logicalOrExpression = 25
    RULE_logicalAndExpression = 26
    RULE_equalityExpression = 27
    RULE_relationalExpression = 28
    RULE_additiveExpression = 29
    RULE_multiplicativeExpression = 30
    RULE_unaryExpression = 31
    RULE_postfixExpression = 32
    RULE_postfixPart = 33
    RULE_argumentList = 34
    RULE_primaryExpression = 35
    RULE_typeSpecifier = 36

    ruleNames =  [ "program", "functionDef", "paramList", "param", "block", 
                   "blockItem", "declaration", "declarationNoSemi", "initDeclaratorList", 
                   "initDeclarator", "arraySuffix", "statement", "emptyStatement", 
                   "exprStatement", "ifStatement", "whileStatement", "forStatement", 
                   "forInit", "returnStatement", "breakStatement", "continueStatement", 
                   "expression", "assignmentExpression", "assignmentOperator", 
                   "conditionalExpression", "logicalOrExpression", "logicalAndExpression", 
                   "equalityExpression", "relationalExpression", "additiveExpression", 
                   "multiplicativeExpression", "unaryExpression", "postfixExpression", 
                   "postfixPart", "argumentList", "primaryExpression", "typeSpecifier" ]

    EOF = Token.EOF
    INT=1
    FLOAT=2
    CHAR=3
    VOID=4
    RETURN=5
    IF=6
    ELSE=7
    WHILE=8
    FOR=9
    BREAK=10
    CONTINUE=11
    INC=12
    DEC=13
    ADD_ASSIGN=14
    SUB_ASSIGN=15
    MUL_ASSIGN=16
    DIV_ASSIGN=17
    MOD_ASSIGN=18
    EQ=19
    NEQ=20
    LTE=21
    GTE=22
    AND=23
    OR=24
    PLUS=25
    MINUS=26
    MUL=27
    DIV=28
    MOD=29
    LT=30
    GT=31
    NOT=32
    ASSIGN=33
    QUESTION=34
    COLON=35
    COMMA=36
    SEMI=37
    LPAREN=38
    RPAREN=39
    LBRACE=40
    RBRACE=41
    LBRACK=42
    RBRACK=43
    IDENTIFIER=44
    INTEGER=45
    FLOAT_LITERAL=46
    CHAR_LITERAL=47
    WS=48
    LINE_COMMENT=49
    BLOCK_COMMENT=50
    ERROR_CHAR=51

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

        def EOF(self):
            return self.getToken(SimpleCParser.EOF, 0)

        def functionDef(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.FunctionDefContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.FunctionDefContext,i)


        def getRuleIndex(self):
            return SimpleCParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = SimpleCParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 74
                self.functionDef()
                self.state = 77 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 30) != 0)):
                    break

            self.state = 79
            self.match(SimpleCParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeSpecifier(self):
            return self.getTypedRuleContext(SimpleCParser.TypeSpecifierContext,0)


        def IDENTIFIER(self):
            return self.getToken(SimpleCParser.IDENTIFIER, 0)

        def LPAREN(self):
            return self.getToken(SimpleCParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(SimpleCParser.RPAREN, 0)

        def block(self):
            return self.getTypedRuleContext(SimpleCParser.BlockContext,0)


        def paramList(self):
            return self.getTypedRuleContext(SimpleCParser.ParamListContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_functionDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionDef" ):
                listener.enterFunctionDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionDef" ):
                listener.exitFunctionDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionDef" ):
                return visitor.visitFunctionDef(self)
            else:
                return visitor.visitChildren(self)




    def functionDef(self):

        localctx = SimpleCParser.FunctionDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_functionDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.typeSpecifier()
            self.state = 82
            self.match(SimpleCParser.IDENTIFIER)
            self.state = 83
            self.match(SimpleCParser.LPAREN)
            self.state = 85
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 30) != 0):
                self.state = 84
                self.paramList()


            self.state = 87
            self.match(SimpleCParser.RPAREN)
            self.state = 88
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.ParamContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.ParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.COMMA)
            else:
                return self.getToken(SimpleCParser.COMMA, i)

        def getRuleIndex(self):
            return SimpleCParser.RULE_paramList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamList" ):
                listener.enterParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamList" ):
                listener.exitParamList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamList" ):
                return visitor.visitParamList(self)
            else:
                return visitor.visitChildren(self)




    def paramList(self):

        localctx = SimpleCParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self.param()
            self.state = 95
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==36:
                self.state = 91
                self.match(SimpleCParser.COMMA)
                self.state = 92
                self.param()
                self.state = 97
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeSpecifier(self):
            return self.getTypedRuleContext(SimpleCParser.TypeSpecifierContext,0)


        def IDENTIFIER(self):
            return self.getToken(SimpleCParser.IDENTIFIER, 0)

        def arraySuffix(self):
            return self.getTypedRuleContext(SimpleCParser.ArraySuffixContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_param

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam" ):
                listener.enterParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam" ):
                listener.exitParam(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = SimpleCParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 98
            self.typeSpecifier()
            self.state = 99
            self.match(SimpleCParser.IDENTIFIER)
            self.state = 101
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==42:
                self.state = 100
                self.arraySuffix()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(SimpleCParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(SimpleCParser.RBRACE, 0)

        def blockItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.BlockItemContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.BlockItemContext,i)


        def getRuleIndex(self):
            return SimpleCParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = SimpleCParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 103
            self.match(SimpleCParser.LBRACE)
            self.state = 107
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 265399014801278) != 0):
                self.state = 104
                self.blockItem()
                self.state = 109
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 110
            self.match(SimpleCParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declaration(self):
            return self.getTypedRuleContext(SimpleCParser.DeclarationContext,0)


        def statement(self):
            return self.getTypedRuleContext(SimpleCParser.StatementContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_blockItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlockItem" ):
                listener.enterBlockItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlockItem" ):
                listener.exitBlockItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlockItem" ):
                return visitor.visitBlockItem(self)
            else:
                return visitor.visitChildren(self)




    def blockItem(self):

        localctx = SimpleCParser.BlockItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_blockItem)
        try:
            self.state = 114
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 112
                self.declaration()
                pass
            elif token in [5, 6, 8, 9, 10, 11, 12, 13, 25, 26, 32, 37, 38, 40, 44, 45, 46, 47]:
                self.enterOuterAlt(localctx, 2)
                self.state = 113
                self.statement()
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


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declarationNoSemi(self):
            return self.getTypedRuleContext(SimpleCParser.DeclarationNoSemiContext,0)


        def SEMI(self):
            return self.getToken(SimpleCParser.SEMI, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaration" ):
                return visitor.visitDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def declaration(self):

        localctx = SimpleCParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_declaration)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            self.declarationNoSemi()
            self.state = 117
            self.match(SimpleCParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationNoSemiContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def typeSpecifier(self):
            return self.getTypedRuleContext(SimpleCParser.TypeSpecifierContext,0)


        def initDeclaratorList(self):
            return self.getTypedRuleContext(SimpleCParser.InitDeclaratorListContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_declarationNoSemi

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclarationNoSemi" ):
                listener.enterDeclarationNoSemi(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclarationNoSemi" ):
                listener.exitDeclarationNoSemi(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclarationNoSemi" ):
                return visitor.visitDeclarationNoSemi(self)
            else:
                return visitor.visitChildren(self)




    def declarationNoSemi(self):

        localctx = SimpleCParser.DeclarationNoSemiContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_declarationNoSemi)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            self.typeSpecifier()
            self.state = 120
            self.initDeclaratorList()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InitDeclaratorListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def initDeclarator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.InitDeclaratorContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.InitDeclaratorContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.COMMA)
            else:
                return self.getToken(SimpleCParser.COMMA, i)

        def getRuleIndex(self):
            return SimpleCParser.RULE_initDeclaratorList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInitDeclaratorList" ):
                listener.enterInitDeclaratorList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInitDeclaratorList" ):
                listener.exitInitDeclaratorList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInitDeclaratorList" ):
                return visitor.visitInitDeclaratorList(self)
            else:
                return visitor.visitChildren(self)




    def initDeclaratorList(self):

        localctx = SimpleCParser.InitDeclaratorListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_initDeclaratorList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 122
            self.initDeclarator()
            self.state = 127
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==36:
                self.state = 123
                self.match(SimpleCParser.COMMA)
                self.state = 124
                self.initDeclarator()
                self.state = 129
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class InitDeclaratorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(SimpleCParser.IDENTIFIER, 0)

        def arraySuffix(self):
            return self.getTypedRuleContext(SimpleCParser.ArraySuffixContext,0)


        def ASSIGN(self):
            return self.getToken(SimpleCParser.ASSIGN, 0)

        def expression(self):
            return self.getTypedRuleContext(SimpleCParser.ExpressionContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_initDeclarator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInitDeclarator" ):
                listener.enterInitDeclarator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInitDeclarator" ):
                listener.exitInitDeclarator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInitDeclarator" ):
                return visitor.visitInitDeclarator(self)
            else:
                return visitor.visitChildren(self)




    def initDeclarator(self):

        localctx = SimpleCParser.InitDeclaratorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_initDeclarator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 130
            self.match(SimpleCParser.IDENTIFIER)
            self.state = 132
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==42:
                self.state = 131
                self.arraySuffix()


            self.state = 136
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==33:
                self.state = 134
                self.match(SimpleCParser.ASSIGN)
                self.state = 135
                self.expression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArraySuffixContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACK(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.LBRACK)
            else:
                return self.getToken(SimpleCParser.LBRACK, i)

        def RBRACK(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.RBRACK)
            else:
                return self.getToken(SimpleCParser.RBRACK, i)

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.ExpressionContext,i)


        def getRuleIndex(self):
            return SimpleCParser.RULE_arraySuffix

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArraySuffix" ):
                listener.enterArraySuffix(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArraySuffix" ):
                listener.exitArraySuffix(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArraySuffix" ):
                return visitor.visitArraySuffix(self)
            else:
                return visitor.visitChildren(self)




    def arraySuffix(self):

        localctx = SimpleCParser.ArraySuffixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_arraySuffix)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 138
                self.match(SimpleCParser.LBRACK)
                self.state = 140
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 264162064216064) != 0):
                    self.state = 139
                    self.expression()


                self.state = 142
                self.match(SimpleCParser.RBRACK)
                self.state = 145 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==42):
                    break

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

        def emptyStatement(self):
            return self.getTypedRuleContext(SimpleCParser.EmptyStatementContext,0)


        def exprStatement(self):
            return self.getTypedRuleContext(SimpleCParser.ExprStatementContext,0)


        def ifStatement(self):
            return self.getTypedRuleContext(SimpleCParser.IfStatementContext,0)


        def whileStatement(self):
            return self.getTypedRuleContext(SimpleCParser.WhileStatementContext,0)


        def forStatement(self):
            return self.getTypedRuleContext(SimpleCParser.ForStatementContext,0)


        def returnStatement(self):
            return self.getTypedRuleContext(SimpleCParser.ReturnStatementContext,0)


        def breakStatement(self):
            return self.getTypedRuleContext(SimpleCParser.BreakStatementContext,0)


        def continueStatement(self):
            return self.getTypedRuleContext(SimpleCParser.ContinueStatementContext,0)


        def block(self):
            return self.getTypedRuleContext(SimpleCParser.BlockContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = SimpleCParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_statement)
        try:
            self.state = 156
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 147
                self.emptyStatement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 148
                self.exprStatement()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 149
                self.ifStatement()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 150
                self.whileStatement()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 151
                self.forStatement()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 152
                self.returnStatement()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 153
                self.breakStatement()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 154
                self.continueStatement()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 155
                self.block()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EmptyStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SEMI(self):
            return self.getToken(SimpleCParser.SEMI, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_emptyStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEmptyStatement" ):
                listener.enterEmptyStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEmptyStatement" ):
                listener.exitEmptyStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEmptyStatement" ):
                return visitor.visitEmptyStatement(self)
            else:
                return visitor.visitChildren(self)




    def emptyStatement(self):

        localctx = SimpleCParser.EmptyStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_emptyStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 158
            self.match(SimpleCParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SEMI(self):
            return self.getToken(SimpleCParser.SEMI, 0)

        def expression(self):
            return self.getTypedRuleContext(SimpleCParser.ExpressionContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_exprStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprStatement" ):
                listener.enterExprStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprStatement" ):
                listener.exitExprStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprStatement" ):
                return visitor.visitExprStatement(self)
            else:
                return visitor.visitChildren(self)




    def exprStatement(self):

        localctx = SimpleCParser.ExprStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_exprStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 161
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 264162064216064) != 0):
                self.state = 160
                self.expression()


            self.state = 163
            self.match(SimpleCParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(SimpleCParser.IF, 0)

        def LPAREN(self):
            return self.getToken(SimpleCParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(SimpleCParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(SimpleCParser.RPAREN, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.StatementContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.StatementContext,i)


        def ELSE(self):
            return self.getToken(SimpleCParser.ELSE, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_ifStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStatement" ):
                listener.enterIfStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStatement" ):
                listener.exitIfStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStatement" ):
                return visitor.visitIfStatement(self)
            else:
                return visitor.visitChildren(self)




    def ifStatement(self):

        localctx = SimpleCParser.IfStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 165
            self.match(SimpleCParser.IF)
            self.state = 166
            self.match(SimpleCParser.LPAREN)
            self.state = 167
            self.expression()
            self.state = 168
            self.match(SimpleCParser.RPAREN)
            self.state = 169
            self.statement()
            self.state = 172
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.state = 170
                self.match(SimpleCParser.ELSE)
                self.state = 171
                self.statement()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(SimpleCParser.WHILE, 0)

        def LPAREN(self):
            return self.getToken(SimpleCParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(SimpleCParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(SimpleCParser.RPAREN, 0)

        def statement(self):
            return self.getTypedRuleContext(SimpleCParser.StatementContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_whileStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhileStatement" ):
                listener.enterWhileStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhileStatement" ):
                listener.exitWhileStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStatement" ):
                return visitor.visitWhileStatement(self)
            else:
                return visitor.visitChildren(self)




    def whileStatement(self):

        localctx = SimpleCParser.WhileStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_whileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 174
            self.match(SimpleCParser.WHILE)
            self.state = 175
            self.match(SimpleCParser.LPAREN)
            self.state = 176
            self.expression()
            self.state = 177
            self.match(SimpleCParser.RPAREN)
            self.state = 178
            self.statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(SimpleCParser.FOR, 0)

        def LPAREN(self):
            return self.getToken(SimpleCParser.LPAREN, 0)

        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.SEMI)
            else:
                return self.getToken(SimpleCParser.SEMI, i)

        def RPAREN(self):
            return self.getToken(SimpleCParser.RPAREN, 0)

        def statement(self):
            return self.getTypedRuleContext(SimpleCParser.StatementContext,0)


        def forInit(self):
            return self.getTypedRuleContext(SimpleCParser.ForInitContext,0)


        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.ExpressionContext,i)


        def getRuleIndex(self):
            return SimpleCParser.RULE_forStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStatement" ):
                listener.enterForStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStatement" ):
                listener.exitForStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStatement" ):
                return visitor.visitForStatement(self)
            else:
                return visitor.visitChildren(self)




    def forStatement(self):

        localctx = SimpleCParser.ForStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_forStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 180
            self.match(SimpleCParser.FOR)
            self.state = 181
            self.match(SimpleCParser.LPAREN)
            self.state = 183
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 264162064216094) != 0):
                self.state = 182
                self.forInit()


            self.state = 185
            self.match(SimpleCParser.SEMI)
            self.state = 187
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 264162064216064) != 0):
                self.state = 186
                self.expression()


            self.state = 189
            self.match(SimpleCParser.SEMI)
            self.state = 191
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 264162064216064) != 0):
                self.state = 190
                self.expression()


            self.state = 193
            self.match(SimpleCParser.RPAREN)
            self.state = 194
            self.statement()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForInitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declarationNoSemi(self):
            return self.getTypedRuleContext(SimpleCParser.DeclarationNoSemiContext,0)


        def expression(self):
            return self.getTypedRuleContext(SimpleCParser.ExpressionContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_forInit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForInit" ):
                listener.enterForInit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForInit" ):
                listener.exitForInit(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForInit" ):
                return visitor.visitForInit(self)
            else:
                return visitor.visitChildren(self)




    def forInit(self):

        localctx = SimpleCParser.ForInitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_forInit)
        try:
            self.state = 198
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 196
                self.declarationNoSemi()
                pass
            elif token in [12, 13, 25, 26, 32, 38, 44, 45, 46, 47]:
                self.enterOuterAlt(localctx, 2)
                self.state = 197
                self.expression()
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


    class ReturnStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(SimpleCParser.RETURN, 0)

        def SEMI(self):
            return self.getToken(SimpleCParser.SEMI, 0)

        def expression(self):
            return self.getTypedRuleContext(SimpleCParser.ExpressionContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_returnStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStatement" ):
                listener.enterReturnStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStatement" ):
                listener.exitReturnStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStatement" ):
                return visitor.visitReturnStatement(self)
            else:
                return visitor.visitChildren(self)




    def returnStatement(self):

        localctx = SimpleCParser.ReturnStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_returnStatement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
            self.match(SimpleCParser.RETURN)
            self.state = 202
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 264162064216064) != 0):
                self.state = 201
                self.expression()


            self.state = 204
            self.match(SimpleCParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BreakStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BREAK(self):
            return self.getToken(SimpleCParser.BREAK, 0)

        def SEMI(self):
            return self.getToken(SimpleCParser.SEMI, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_breakStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreakStatement" ):
                listener.enterBreakStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreakStatement" ):
                listener.exitBreakStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreakStatement" ):
                return visitor.visitBreakStatement(self)
            else:
                return visitor.visitChildren(self)




    def breakStatement(self):

        localctx = SimpleCParser.BreakStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_breakStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 206
            self.match(SimpleCParser.BREAK)
            self.state = 207
            self.match(SimpleCParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContinueStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CONTINUE(self):
            return self.getToken(SimpleCParser.CONTINUE, 0)

        def SEMI(self):
            return self.getToken(SimpleCParser.SEMI, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_continueStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContinueStatement" ):
                listener.enterContinueStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContinueStatement" ):
                listener.exitContinueStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinueStatement" ):
                return visitor.visitContinueStatement(self)
            else:
                return visitor.visitChildren(self)




    def continueStatement(self):

        localctx = SimpleCParser.ContinueStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_continueStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 209
            self.match(SimpleCParser.CONTINUE)
            self.state = 210
            self.match(SimpleCParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignmentExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.AssignmentExpressionContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.AssignmentExpressionContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.COMMA)
            else:
                return self.getToken(SimpleCParser.COMMA, i)

        def getRuleIndex(self):
            return SimpleCParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = SimpleCParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_expression)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 212
            self.assignmentExpression()
            self.state = 217
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,19,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 213
                    self.match(SimpleCParser.COMMA)
                    self.state = 214
                    self.assignmentExpression() 
                self.state = 219
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,19,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def conditionalExpression(self):
            return self.getTypedRuleContext(SimpleCParser.ConditionalExpressionContext,0)


        def unaryExpression(self):
            return self.getTypedRuleContext(SimpleCParser.UnaryExpressionContext,0)


        def assignmentOperator(self):
            return self.getTypedRuleContext(SimpleCParser.AssignmentOperatorContext,0)


        def assignmentExpression(self):
            return self.getTypedRuleContext(SimpleCParser.AssignmentExpressionContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_assignmentExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignmentExpression" ):
                listener.enterAssignmentExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignmentExpression" ):
                listener.exitAssignmentExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignmentExpression" ):
                return visitor.visitAssignmentExpression(self)
            else:
                return visitor.visitChildren(self)




    def assignmentExpression(self):

        localctx = SimpleCParser.AssignmentExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_assignmentExpression)
        try:
            self.state = 225
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 220
                self.conditionalExpression()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 221
                self.unaryExpression()
                self.state = 222
                self.assignmentOperator()
                self.state = 223
                self.assignmentExpression()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ASSIGN(self):
            return self.getToken(SimpleCParser.ASSIGN, 0)

        def ADD_ASSIGN(self):
            return self.getToken(SimpleCParser.ADD_ASSIGN, 0)

        def SUB_ASSIGN(self):
            return self.getToken(SimpleCParser.SUB_ASSIGN, 0)

        def MUL_ASSIGN(self):
            return self.getToken(SimpleCParser.MUL_ASSIGN, 0)

        def DIV_ASSIGN(self):
            return self.getToken(SimpleCParser.DIV_ASSIGN, 0)

        def MOD_ASSIGN(self):
            return self.getToken(SimpleCParser.MOD_ASSIGN, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_assignmentOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignmentOperator" ):
                listener.enterAssignmentOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignmentOperator" ):
                listener.exitAssignmentOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignmentOperator" ):
                return visitor.visitAssignmentOperator(self)
            else:
                return visitor.visitChildren(self)




    def assignmentOperator(self):

        localctx = SimpleCParser.AssignmentOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_assignmentOperator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 227
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8590442496) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionalExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalOrExpression(self):
            return self.getTypedRuleContext(SimpleCParser.LogicalOrExpressionContext,0)


        def QUESTION(self):
            return self.getToken(SimpleCParser.QUESTION, 0)

        def expression(self):
            return self.getTypedRuleContext(SimpleCParser.ExpressionContext,0)


        def COLON(self):
            return self.getToken(SimpleCParser.COLON, 0)

        def conditionalExpression(self):
            return self.getTypedRuleContext(SimpleCParser.ConditionalExpressionContext,0)


        def getRuleIndex(self):
            return SimpleCParser.RULE_conditionalExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConditionalExpression" ):
                listener.enterConditionalExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConditionalExpression" ):
                listener.exitConditionalExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConditionalExpression" ):
                return visitor.visitConditionalExpression(self)
            else:
                return visitor.visitChildren(self)




    def conditionalExpression(self):

        localctx = SimpleCParser.ConditionalExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_conditionalExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 229
            self.logicalOrExpression()
            self.state = 235
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==34:
                self.state = 230
                self.match(SimpleCParser.QUESTION)
                self.state = 231
                self.expression()
                self.state = 232
                self.match(SimpleCParser.COLON)
                self.state = 233
                self.conditionalExpression()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalOrExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalAndExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.LogicalAndExpressionContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.LogicalAndExpressionContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.OR)
            else:
                return self.getToken(SimpleCParser.OR, i)

        def getRuleIndex(self):
            return SimpleCParser.RULE_logicalOrExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicalOrExpression" ):
                listener.enterLogicalOrExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicalOrExpression" ):
                listener.exitLogicalOrExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalOrExpression" ):
                return visitor.visitLogicalOrExpression(self)
            else:
                return visitor.visitChildren(self)




    def logicalOrExpression(self):

        localctx = SimpleCParser.LogicalOrExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_logicalOrExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 237
            self.logicalAndExpression()
            self.state = 242
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==24:
                self.state = 238
                self.match(SimpleCParser.OR)
                self.state = 239
                self.logicalAndExpression()
                self.state = 244
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalAndExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def equalityExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.EqualityExpressionContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.EqualityExpressionContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.AND)
            else:
                return self.getToken(SimpleCParser.AND, i)

        def getRuleIndex(self):
            return SimpleCParser.RULE_logicalAndExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicalAndExpression" ):
                listener.enterLogicalAndExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicalAndExpression" ):
                listener.exitLogicalAndExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalAndExpression" ):
                return visitor.visitLogicalAndExpression(self)
            else:
                return visitor.visitChildren(self)




    def logicalAndExpression(self):

        localctx = SimpleCParser.LogicalAndExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_logicalAndExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 245
            self.equalityExpression()
            self.state = 250
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==23:
                self.state = 246
                self.match(SimpleCParser.AND)
                self.state = 247
                self.equalityExpression()
                self.state = 252
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EqualityExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relationalExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.RelationalExpressionContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.RelationalExpressionContext,i)


        def EQ(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.EQ)
            else:
                return self.getToken(SimpleCParser.EQ, i)

        def NEQ(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.NEQ)
            else:
                return self.getToken(SimpleCParser.NEQ, i)

        def getRuleIndex(self):
            return SimpleCParser.RULE_equalityExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEqualityExpression" ):
                listener.enterEqualityExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEqualityExpression" ):
                listener.exitEqualityExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEqualityExpression" ):
                return visitor.visitEqualityExpression(self)
            else:
                return visitor.visitChildren(self)




    def equalityExpression(self):

        localctx = SimpleCParser.EqualityExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_equalityExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 253
            self.relationalExpression()
            self.state = 258
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==19 or _la==20:
                self.state = 254
                _la = self._input.LA(1)
                if not(_la==19 or _la==20):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 255
                self.relationalExpression()
                self.state = 260
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationalExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def additiveExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.AdditiveExpressionContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.AdditiveExpressionContext,i)


        def LT(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.LT)
            else:
                return self.getToken(SimpleCParser.LT, i)

        def LTE(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.LTE)
            else:
                return self.getToken(SimpleCParser.LTE, i)

        def GT(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.GT)
            else:
                return self.getToken(SimpleCParser.GT, i)

        def GTE(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.GTE)
            else:
                return self.getToken(SimpleCParser.GTE, i)

        def getRuleIndex(self):
            return SimpleCParser.RULE_relationalExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationalExpression" ):
                listener.enterRelationalExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationalExpression" ):
                listener.exitRelationalExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationalExpression" ):
                return visitor.visitRelationalExpression(self)
            else:
                return visitor.visitChildren(self)




    def relationalExpression(self):

        localctx = SimpleCParser.RelationalExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_relationalExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 261
            self.additiveExpression()
            self.state = 266
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 3227516928) != 0):
                self.state = 262
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3227516928) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 263
                self.additiveExpression()
                self.state = 268
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multiplicativeExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.MultiplicativeExpressionContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.MultiplicativeExpressionContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.PLUS)
            else:
                return self.getToken(SimpleCParser.PLUS, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.MINUS)
            else:
                return self.getToken(SimpleCParser.MINUS, i)

        def getRuleIndex(self):
            return SimpleCParser.RULE_additiveExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveExpression" ):
                listener.enterAdditiveExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveExpression" ):
                listener.exitAdditiveExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveExpression" ):
                return visitor.visitAdditiveExpression(self)
            else:
                return visitor.visitChildren(self)




    def additiveExpression(self):

        localctx = SimpleCParser.AdditiveExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_additiveExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 269
            self.multiplicativeExpression()
            self.state = 274
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==25 or _la==26:
                self.state = 270
                _la = self._input.LA(1)
                if not(_la==25 or _la==26):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 271
                self.multiplicativeExpression()
                self.state = 276
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicativeExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unaryExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.UnaryExpressionContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.UnaryExpressionContext,i)


        def MUL(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.MUL)
            else:
                return self.getToken(SimpleCParser.MUL, i)

        def DIV(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.DIV)
            else:
                return self.getToken(SimpleCParser.DIV, i)

        def MOD(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.MOD)
            else:
                return self.getToken(SimpleCParser.MOD, i)

        def getRuleIndex(self):
            return SimpleCParser.RULE_multiplicativeExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeExpression" ):
                listener.enterMultiplicativeExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeExpression" ):
                listener.exitMultiplicativeExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeExpression" ):
                return visitor.visitMultiplicativeExpression(self)
            else:
                return visitor.visitChildren(self)




    def multiplicativeExpression(self):

        localctx = SimpleCParser.MultiplicativeExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_multiplicativeExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 277
            self.unaryExpression()
            self.state = 282
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 939524096) != 0):
                self.state = 278
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 939524096) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 279
                self.unaryExpression()
                self.state = 284
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def postfixExpression(self):
            return self.getTypedRuleContext(SimpleCParser.PostfixExpressionContext,0)


        def unaryExpression(self):
            return self.getTypedRuleContext(SimpleCParser.UnaryExpressionContext,0)


        def INC(self):
            return self.getToken(SimpleCParser.INC, 0)

        def DEC(self):
            return self.getToken(SimpleCParser.DEC, 0)

        def PLUS(self):
            return self.getToken(SimpleCParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(SimpleCParser.MINUS, 0)

        def NOT(self):
            return self.getToken(SimpleCParser.NOT, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_unaryExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryExpression" ):
                listener.enterUnaryExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryExpression" ):
                listener.exitUnaryExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryExpression" ):
                return visitor.visitUnaryExpression(self)
            else:
                return visitor.visitChildren(self)




    def unaryExpression(self):

        localctx = SimpleCParser.UnaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_unaryExpression)
        self._la = 0 # Token type
        try:
            self.state = 288
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [38, 44, 45, 46, 47]:
                self.enterOuterAlt(localctx, 1)
                self.state = 285
                self.postfixExpression()
                pass
            elif token in [12, 13, 25, 26, 32]:
                self.enterOuterAlt(localctx, 2)
                self.state = 286
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4395642880) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 287
                self.unaryExpression()
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


    class PostfixExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primaryExpression(self):
            return self.getTypedRuleContext(SimpleCParser.PrimaryExpressionContext,0)


        def postfixPart(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.PostfixPartContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.PostfixPartContext,i)


        def getRuleIndex(self):
            return SimpleCParser.RULE_postfixExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPostfixExpression" ):
                listener.enterPostfixExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPostfixExpression" ):
                listener.exitPostfixExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostfixExpression" ):
                return visitor.visitPostfixExpression(self)
            else:
                return visitor.visitChildren(self)




    def postfixExpression(self):

        localctx = SimpleCParser.PostfixExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_postfixExpression)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 290
            self.primaryExpression()
            self.state = 294
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 4672924430336) != 0):
                self.state = 291
                self.postfixPart()
                self.state = 296
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PostfixPartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACK(self):
            return self.getToken(SimpleCParser.LBRACK, 0)

        def expression(self):
            return self.getTypedRuleContext(SimpleCParser.ExpressionContext,0)


        def RBRACK(self):
            return self.getToken(SimpleCParser.RBRACK, 0)

        def LPAREN(self):
            return self.getToken(SimpleCParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(SimpleCParser.RPAREN, 0)

        def argumentList(self):
            return self.getTypedRuleContext(SimpleCParser.ArgumentListContext,0)


        def INC(self):
            return self.getToken(SimpleCParser.INC, 0)

        def DEC(self):
            return self.getToken(SimpleCParser.DEC, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_postfixPart

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPostfixPart" ):
                listener.enterPostfixPart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPostfixPart" ):
                listener.exitPostfixPart(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostfixPart" ):
                return visitor.visitPostfixPart(self)
            else:
                return visitor.visitChildren(self)




    def postfixPart(self):

        localctx = SimpleCParser.PostfixPartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_postfixPart)
        self._la = 0 # Token type
        try:
            self.state = 308
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [42]:
                self.enterOuterAlt(localctx, 1)
                self.state = 297
                self.match(SimpleCParser.LBRACK)
                self.state = 298
                self.expression()
                self.state = 299
                self.match(SimpleCParser.RBRACK)
                pass
            elif token in [38]:
                self.enterOuterAlt(localctx, 2)
                self.state = 301
                self.match(SimpleCParser.LPAREN)
                self.state = 303
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 264162064216064) != 0):
                    self.state = 302
                    self.argumentList()


                self.state = 305
                self.match(SimpleCParser.RPAREN)
                pass
            elif token in [12]:
                self.enterOuterAlt(localctx, 3)
                self.state = 306
                self.match(SimpleCParser.INC)
                pass
            elif token in [13]:
                self.enterOuterAlt(localctx, 4)
                self.state = 307
                self.match(SimpleCParser.DEC)
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


    class ArgumentListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignmentExpression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SimpleCParser.AssignmentExpressionContext)
            else:
                return self.getTypedRuleContext(SimpleCParser.AssignmentExpressionContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(SimpleCParser.COMMA)
            else:
                return self.getToken(SimpleCParser.COMMA, i)

        def getRuleIndex(self):
            return SimpleCParser.RULE_argumentList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgumentList" ):
                listener.enterArgumentList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgumentList" ):
                listener.exitArgumentList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgumentList" ):
                return visitor.visitArgumentList(self)
            else:
                return visitor.visitChildren(self)




    def argumentList(self):

        localctx = SimpleCParser.ArgumentListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_argumentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 310
            self.assignmentExpression()
            self.state = 315
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==36:
                self.state = 311
                self.match(SimpleCParser.COMMA)
                self.state = 312
                self.assignmentExpression()
                self.state = 317
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFIER(self):
            return self.getToken(SimpleCParser.IDENTIFIER, 0)

        def INTEGER(self):
            return self.getToken(SimpleCParser.INTEGER, 0)

        def FLOAT_LITERAL(self):
            return self.getToken(SimpleCParser.FLOAT_LITERAL, 0)

        def CHAR_LITERAL(self):
            return self.getToken(SimpleCParser.CHAR_LITERAL, 0)

        def LPAREN(self):
            return self.getToken(SimpleCParser.LPAREN, 0)

        def expression(self):
            return self.getTypedRuleContext(SimpleCParser.ExpressionContext,0)


        def RPAREN(self):
            return self.getToken(SimpleCParser.RPAREN, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_primaryExpression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimaryExpression" ):
                listener.enterPrimaryExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimaryExpression" ):
                listener.exitPrimaryExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimaryExpression" ):
                return visitor.visitPrimaryExpression(self)
            else:
                return visitor.visitChildren(self)




    def primaryExpression(self):

        localctx = SimpleCParser.PrimaryExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_primaryExpression)
        try:
            self.state = 326
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [44]:
                self.enterOuterAlt(localctx, 1)
                self.state = 318
                self.match(SimpleCParser.IDENTIFIER)
                pass
            elif token in [45]:
                self.enterOuterAlt(localctx, 2)
                self.state = 319
                self.match(SimpleCParser.INTEGER)
                pass
            elif token in [46]:
                self.enterOuterAlt(localctx, 3)
                self.state = 320
                self.match(SimpleCParser.FLOAT_LITERAL)
                pass
            elif token in [47]:
                self.enterOuterAlt(localctx, 4)
                self.state = 321
                self.match(SimpleCParser.CHAR_LITERAL)
                pass
            elif token in [38]:
                self.enterOuterAlt(localctx, 5)
                self.state = 322
                self.match(SimpleCParser.LPAREN)
                self.state = 323
                self.expression()
                self.state = 324
                self.match(SimpleCParser.RPAREN)
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


    class TypeSpecifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(SimpleCParser.INT, 0)

        def FLOAT(self):
            return self.getToken(SimpleCParser.FLOAT, 0)

        def CHAR(self):
            return self.getToken(SimpleCParser.CHAR, 0)

        def VOID(self):
            return self.getToken(SimpleCParser.VOID, 0)

        def getRuleIndex(self):
            return SimpleCParser.RULE_typeSpecifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTypeSpecifier" ):
                listener.enterTypeSpecifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTypeSpecifier" ):
                listener.exitTypeSpecifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTypeSpecifier" ):
                return visitor.visitTypeSpecifier(self)
            else:
                return visitor.visitChildren(self)




    def typeSpecifier(self):

        localctx = SimpleCParser.TypeSpecifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_typeSpecifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 328
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 30) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





