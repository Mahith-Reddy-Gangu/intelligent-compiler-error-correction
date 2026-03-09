grammar SimpleC;

/* =========================
   PARSER RULES
   ========================= */

program
    : functionDef+ EOF
    ;

// ---- Functions ----
// Supports: int foo(int a, float b) { ... }
functionDef
    : typeSpecifier IDENTIFIER LPAREN paramList? RPAREN block
    ;

paramList
    : param (COMMA param)*
    ;

param
    : typeSpecifier IDENTIFIER arraySuffix?
    ;

// ---- Blocks with mixed declarations/statements (C99 style) ----
block
    : LBRACE blockItem* RBRACE
    ;

blockItem
    : declaration
    | statement
    ;

// ---- Declarations ----
declaration
    : declarationNoSemi SEMI
    ;

// IMPORTANT: same as declaration, but WITHOUT the trailing ';'
// Needed for: for (int i=0; ... ; ...)
declarationNoSemi
    : typeSpecifier initDeclaratorList
    ;

initDeclaratorList
    : initDeclarator (COMMA initDeclarator)*
    ;

initDeclarator
    : IDENTIFIER arraySuffix? (ASSIGN expression)?
    ;

// multi-dimensional arrays: int a[10][20][30];
arraySuffix
    : (LBRACK expression? RBRACK)+
    ;

// ---- Statements ----
statement
    : emptyStatement
    | exprStatement
    | ifStatement
    | whileStatement
    | forStatement
    | returnStatement
    | breakStatement
    | continueStatement
    | block
    ;

emptyStatement
    : SEMI
    ;

exprStatement
    : expression? SEMI
    ;

ifStatement
    : IF LPAREN expression RPAREN statement (ELSE statement)?
    ;

whileStatement
    : WHILE LPAREN expression RPAREN statement
    ;

// for (init; cond; update) stmt
forStatement
    : FOR LPAREN forInit? SEMI expression? SEMI expression? RPAREN statement
    ;

forInit
    : declarationNoSemi
    | expression
    ;

returnStatement
    : RETURN expression? SEMI
    ;

breakStatement
    : BREAK SEMI
    ;

continueStatement
    : CONTINUE SEMI
    ;


/* =========================
   EXPRESSIONS (with precedence)
   ========================= */

expression
    : assignmentExpression (COMMA assignmentExpression)*
    ;

// assignment and compound assignment
assignmentExpression
    : conditionalExpression
    | unaryExpression assignmentOperator assignmentExpression
    ;

assignmentOperator
    : ASSIGN
    | ADD_ASSIGN
    | SUB_ASSIGN
    | MUL_ASSIGN
    | DIV_ASSIGN
    | MOD_ASSIGN
    ;

conditionalExpression
    : logicalOrExpression (QUESTION expression COLON conditionalExpression)?
    ;

logicalOrExpression
    : logicalAndExpression (OR logicalAndExpression)*
    ;

logicalAndExpression
    : equalityExpression (AND equalityExpression)*
    ;

equalityExpression
    : relationalExpression ((EQ | NEQ) relationalExpression)*
    ;

relationalExpression
    : additiveExpression ((LT | LTE | GT | GTE) additiveExpression)*
    ;

additiveExpression
    : multiplicativeExpression ((PLUS | MINUS) multiplicativeExpression)*
    ;

multiplicativeExpression
    : unaryExpression ((MUL | DIV | MOD) unaryExpression)*
    ;

// unary: ++x, --x, +x, -x, !x
unaryExpression
    : postfixExpression
    | (INC | DEC | PLUS | MINUS | NOT) unaryExpression
    ;

// postfix: x++, x--, calls f(a,b), array indexing a[i]
postfixExpression
    : primaryExpression postfixPart*
    ;

postfixPart
    : LBRACK expression RBRACK           // a[i]
    | LPAREN argumentList? RPAREN        // f(...)
    | INC                                // x++
    | DEC                                // x--
    ;

argumentList
    : assignmentExpression (COMMA assignmentExpression)*
    ;

primaryExpression
    : IDENTIFIER
    | INTEGER
    | FLOAT_LITERAL
    | CHAR_LITERAL
    | LPAREN expression RPAREN
    ;


/* =========================
   TYPES
   ========================= */

typeSpecifier
    : INT
    | FLOAT
    | CHAR
    | VOID
    ;


/* =========================
   LEXER RULES
   ========================= */

INT      : 'int';
FLOAT    : 'float';
CHAR     : 'char';
VOID     : 'void';

RETURN   : 'return';
IF       : 'if';
ELSE     : 'else';
WHILE    : 'while';
FOR      : 'for';
BREAK    : 'break';
CONTINUE : 'continue';

INC      : '++';
DEC      : '--';

ADD_ASSIGN : '+=';
SUB_ASSIGN : '-=';
MUL_ASSIGN : '*=';
DIV_ASSIGN : '/=';
MOD_ASSIGN : '%=';

EQ       : '==';
NEQ      : '!=';
LTE      : '<=';
GTE      : '>=';
AND      : '&&';
OR       : '||';

PLUS     : '+';
MINUS    : '-';
MUL      : '*';
DIV      : '/';
MOD      : '%';

LT       : '<';
GT       : '>';
NOT      : '!';

ASSIGN   : '=';

QUESTION : '?';
COLON    : ':';
COMMA    : ',';
SEMI     : ';';

LPAREN   : '(';
RPAREN   : ')';
LBRACE   : '{';
RBRACE   : '}';
LBRACK   : '[';
RBRACK   : ']';

IDENTIFIER
    : [a-zA-Z_][a-zA-Z_0-9]*
    ;

INTEGER
    : [0-9]+
    ;

FLOAT_LITERAL
    : [0-9]+ '.' [0-9]+
    ;

// simple char literal support: 'a' '\n' '\t' '\''
CHAR_LITERAL
    : '\'' ( ~['\\\r\n] | '\\' [nrt'\\] ) '\''
    ;

WS
    : [ \t\r\n]+ -> skip
    ;

LINE_COMMENT
    : '//' ~[\r\n]* -> skip
    ;

BLOCK_COMMENT
    : '/*' .*? '*/' -> skip
    ;

// predictable illegal token handling
ERROR_CHAR
    : .
    ;