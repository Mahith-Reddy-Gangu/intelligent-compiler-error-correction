# Simple C Parser - Setup and Usage Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install antlr4-python3-runtime
```

### 2. Download ANTLR4 Tool
You need the ANTLR4 tool to generate the parser from the grammar.

#### Option A: Download JAR (Recommended)
```bash
# Download ANTLR4 complete JAR
curl -O https://www.antlr.org/download/antlr-4.13.1-complete.jar

# Or download from: https://www.antlr.org/download.html
```

#### Option B: Use alias (Linux/Mac)
```bash
# Add to ~/.bashrc or ~/.zshrc
alias antlr4='java -jar /path/to/antlr-4.13.1-complete.jar'
```

#### Option C: Use pip package
```bash
pip install antlr4-tools
```

### 3. Generate Parser from Grammar
```bash
# Using JAR:
java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 SimpleC.g4

# Using antlr4-tools:
antlr4 -Dlanguage=Python3 SimpleC.g4

# This generates:
# - SimpleCLexer.py
# - SimpleCParser.py
# - SimpleCListener.py
# - SimpleCVisitor.py (if visitor pattern enabled)
```

### 4. Run the Test Script
```bash
python test_parser.py
```

## Expected Output

### For Valid File (valid_example.c):
```
✅ PARSING SUCCESSFUL
----------------------------------------------------------------------
Parse Tree:
----------------------------------------------------------------------
[program]
  [mainFunction]
    └─ int
    └─ main
    └─ (
    └─ )
    └─ {
    [statementList]
      [statement]
        [variableDeclaration]
          └─ int
          └─ x
          └─ ;
      ...
    └─ }
  └─ <EOF>
```

### For Invalid Files:
```
❌ PARSING FAILED - Syntax Errors Detected:
----------------------------------------------------------------------
  Line 2:8 - Syntax Error: mismatched input 'x' expecting ';'
----------------------------------------------------------------------
```

## File Structure After Generation
```
Implementation/
├── SimpleC.g4                 # ANTLR4 grammar
├── SimpleCLexer.py           # Generated lexer
├── SimpleCParser.py          # Generated parser
├── SimpleCListener.py        # Generated listener (optional)
├── test_parser.py            # Test script
├── valid_example.c           # Test file 1
├── invalid_example1.c        # Test file 2
├── invalid_example2.c        # Test file 3
├── invalid_example3.c        # Test file 4
└── README.md                 # Documentation
```

## Troubleshooting

### Error: "SimpleCLexer and SimpleCParser not found"
**Solution**: Generate the parser files first:
```bash
java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 SimpleC.g4
```

### Error: "antlr4: command not found"
**Solution**: Either:
1. Use the JAR directly: `java -jar antlr-4.13.1-complete.jar ...`
2. Install antlr4-tools: `pip install antlr4-tools`

### Error: "No module named 'antlr4'"
**Solution**: Install the runtime:
```bash
pip install antlr4-python3-runtime
```

## Customizing the Script

### Parse a Single File
```python
from test_parser import parse_file

tree, error_listener = parse_file('your_file.c')
if not error_listener.has_errors():
    print("Valid!")
```

### Add More Test Files
Edit the `test_files` list in `main()`:
```python
test_files = [
    'valid_example.c',
    'my_test.c',
    'another_test.c'
]
```

## Next Steps
- Add semantic analysis (symbol table)
- Implement AST generation
- Add more C language features
- Integrate AI-assisted error correction
