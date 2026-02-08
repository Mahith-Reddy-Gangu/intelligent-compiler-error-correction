grammar SimpleC;

/*
 * PARSER RULES
 * Context-Free Grammar for restricted C subset
 */

// Entry point: A program consists of exactly one main function
program
    : mainFunction EOF
    ;

// Main function: int main() { statement* }
mainFunction
    : 'int' 'main' '(' ')' '{' statementList '}'
    ;

// List of statements (can be empty)
statementList
    : statement*
    ;

// Statement types supported
statement
    : variableDeclaration    // int x;
    | assignment             // x = 10;
    | returnStatement        // return 0;
    ;

// Variable declaration: int identifier;
variableDeclaration
    : 'int' IDENTIFIER ';'
    ;

// Assignment: identifier = integer;
assignment
    : IDENTIFIER '=' INTEGER ';'
    ;

// Return statement: return integer;
returnStatement
    : 'return' INTEGER ';'
    ;

/*
 * LEXER RULES
 * Token definitions
 */

// Keywords (must come before IDENTIFIER to take precedence)
INT     : 'int';
RETURN  : 'return';
MAIN    : 'main';

// Identifier: starts with letter or underscore, followed by letters, digits, or underscores
IDENTIFIER
    : [a-zA-Z_][a-zA-Z_0-9]*
    ;

// Integer literal: one or more digits
INTEGER
    : [0-9]+
    ;

// Whitespace: skip spaces, tabs, newlines, carriage returns
WS
    : [ \t\r\n]+ -> skip
    ;

// Single-line comments (optional but useful for testing)
COMMENT
    : '//' ~[\r\n]* -> skip
    ;
