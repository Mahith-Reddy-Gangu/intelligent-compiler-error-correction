# Intermediate Representation (IR) Model

This project treats the ANTLR parse tree (CST) as the Intermediate Representation (IR).
The IR is read-only and is used for simple analysis passes in Week 8.

## IR Root
- Program
  - MainFunction
    - StatementList (zero or more Statement nodes)

## Statement Nodes
- VariableDeclaration
  - Keyword: int
  - Identifier: IDENTIFIER

- Assignment
  - Identifier: IDENTIFIER
  - Operator: =
  - Literal: INTEGER

- ReturnStatement
  - Keyword: return
  - Literal: INTEGER

## IR Access Strategy
- The IR is accessed through ANTLR listener traversal.
- Each statement node is analyzed directly from its parse context.
- No transformations or optimizations are performed.

## One Analysis Pass
- Variable Declaration Analysis
  - Collect declared variables in a Symbol Table
  - Report assignments to variables that are not declared
