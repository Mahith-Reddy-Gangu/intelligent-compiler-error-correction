# Simple C Parser - ANTLR4 Grammar

## Overview
This is a **syntactic parser** for a highly restricted subset of C, built using ANTLR4 for a compiler front-end project.

## Scope
**ONLY syntactic validation** - no semantic analysis, type checking, or error correction.

## Supported Language Features

### Program Structure
- Exactly one function: `int main() { ... }`

### Supported Statements
1. **Variable Declaration**: `int x;`
2. **Assignment**: `x = 10;`
3. **Return Statement**: `return 0;`

### Tokens
- **Keywords**: `int`, `return`, `main`
- **Identifiers**: Variable names (e.g., `x`, `counter`, `_temp`)
- **Integer Literals**: Numeric constants (e.g., `0`, `10`, `123`)
- **Symbols**: `{`, `}`, `(`, `)`, `;`, `=`

## Grammar File
- **File**: `SimpleC.g4`
- **Grammar Name**: `SimpleC`

## How to Use

### 1. Install ANTLR4
Download ANTLR4 from: https://www.antlr.org/download.html

Or use package managers:
```bash
# Java (if using JAR)
# Download antlr-4.x-complete.jar

# Python
pip install antlr4-python3-runtime

# JavaScript
npm install antlr4
```

### 2. Generate Parser Code

#### For Java:
```bash
java -jar antlr-4.x-complete.jar SimpleC.g4
javac SimpleC*.java
```

#### For Python:
```bash
antlr4 -Dlanguage=Python3 SimpleC.g4
```

#### For C++:
```bash
antlr4 -Dlanguage=Cpp SimpleC.g4
```

### 3. Test the Parser

#### Java Example:
```bash
java org.antlr.v4.gui.TestRig SimpleC program -tree valid_example.c
```

#### Python Example:
```python
from antlr4 import *
from SimpleCLexer import SimpleCLexer
from SimpleCParser import SimpleCParser

def parse_file(filename):
    input_stream = FileStream(filename)
    lexer = SimpleCLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = SimpleCParser(token_stream)
    tree = parser.program()
    print(tree.toStringTree(recog=parser))

parse_file('valid_example.c')
```

## Example Programs

### ✅ Valid Example ([valid_example.c](valid_example.c))
```c
int main() {
    int x;
    int y;
    x = 10;
    y = 20;
    return 0;
}
```

### ❌ Invalid Examples

#### 1. Missing Semicolon ([invalid_example1.c](invalid_example1.c))
```c
int main() {
    int x    // ERROR: Missing semicolon
    x = 10;
    return 0;
}
```
**Expected Error**: `mismatched input 'x' expecting ';'`

#### 2. Missing Closing Brace ([invalid_example2.c](invalid_example2.c))
```c
int main() {
    int x;
    x = 5;
    return 0;
// ERROR: Missing }
```
**Expected Error**: `mismatched input '<EOF>' expecting '}'`

#### 3. Missing Parentheses ([invalid_example3.c](invalid_example3.c))
```c
int main {  // ERROR: Missing ()
    int x;
    return 0;
}
```
**Expected Error**: `mismatched input '{' expecting '('`

## Grammar Rules Explained

### Parser Rules (CFG)
1. **program**: Entry point, expects exactly one `mainFunction` followed by EOF
2. **mainFunction**: Matches `int main() { statementList }`
3. **statementList**: Zero or more statements
4. **statement**: One of three types (declaration, assignment, or return)
5. **variableDeclaration**: `int IDENTIFIER ;`
6. **assignment**: `IDENTIFIER = INTEGER ;`
7. **returnStatement**: `return INTEGER ;`

### Lexer Rules (Tokens)
1. **INT, RETURN, MAIN**: Keyword tokens
2. **IDENTIFIER**: Variable names matching `[a-zA-Z_][a-zA-Z_0-9]*`
3. **INTEGER**: Number literals matching `[0-9]+`
4. **WS**: Whitespace (skipped)
5. **COMMENT**: Single-line comments `//` (skipped)

## Limitations (By Design)
- ❌ No semantic analysis (variable scope, type checking)
- ❌ No symbol table
- ❌ No preprocessor directives (#include, #define)
- ❌ No pointers, arrays, structs
- ❌ No function calls or multiple functions
- ❌ No expressions (only integer literals in assignments)
- ❌ No if/while/for statements

## Parser Responsibilities
✅ Validate syntax against grammar rules  
✅ Detect missing semicolons, braces, parentheses  
✅ Generate parse tree (CST) or AST  
✅ Report syntax errors with line numbers  

## Next Steps (Future Phases)
1. Add semantic analysis (symbol table, type checking)
2. Add intermediate code generation
3. Add AI-assisted error correction
4. Extend grammar for expressions, control flow

## Project Structure
```
Implementation/
├── SimpleC.g4              # ANTLR4 grammar file
├── valid_example.c         # Valid test case
├── invalid_example1.c      # Syntax error: missing semicolon
├── invalid_example2.c      # Syntax error: missing brace
├── invalid_example3.c      # Syntax error: missing parentheses
└── README.md               # This file
```

## Contact
For questions about this parser or compiler project, refer to the course materials or project documentation.
