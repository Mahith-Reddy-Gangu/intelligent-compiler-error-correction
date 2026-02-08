"""
Simple C Parser Test Script
Uses ANTLR4 Python runtime to test the SimpleC grammar

Prerequisites:
1. Install ANTLR4 Python runtime:
   pip install antlr4-python3-runtime

2. Generate lexer and parser from grammar:
   antlr4 -Dlanguage=Python3 SimpleC.g4
   
   This creates:
   - SimpleCLexer.py
   - SimpleCParser.py
   - SimpleCListener.py (optional)
"""

import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

from compiler.error_classifier import classify_error_message
from compiler.error_corrector import apply_correction
from compiler.ir_analysis import analyze_parse_tree

# Import generated lexer and parser
# These will be available after running: antlr4 -Dlanguage=Python3 SimpleC.g4
try:
    from SimpleCLexer import SimpleCLexer
    from SimpleCParser import SimpleCParser
except ImportError:
    print("ERROR: SimpleCLexer and SimpleCParser not found!")
    print("Please generate them first using:")
    print("  antlr4 -Dlanguage=Python3 SimpleC.g4")
    sys.exit(1)


class SyntaxErrorListener(ErrorListener):
    """
    Custom error listener to capture and format syntax errors.
    Overrides the default ANTLR error handling to provide clearer output.
    """
    
    def __init__(self):
        super().__init__()
        self.errors = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """
        Called when ANTLR encounters a syntax error.
        
        Args:
            recognizer: The parser that detected the error
            offendingSymbol: The token that caused the error
            line: Line number where error occurred
            column: Column position where error occurred
            msg: Error message from ANTLR
            e: The exception object (if any)
        """
        self.errors.append(
            {
                "line": line,
                "column": column,
                "msg": msg,
            }
        )
    
    def has_errors(self):
        """Check if any errors were encountered"""
        return len(self.errors) > 0
    
    def get_errors(self):
        """Return list of all error messages"""
        return [f"Line {e['line']}:{e['column']} - Syntax Error: {e['msg']}" for e in self.errors]

    def get_error_objects(self):
        """Return list of structured errors"""
        return list(self.errors)


def parse_source(source_text, source_name="<input>"):
    """
    Parse a C source string using the SimpleC grammar.

    Args:
        source_text: The C source code as a string
        source_name: A human-friendly label for logging

    Returns:
        tuple: (parse_tree, error_listener, parser)
    """
    print(f"\n{'='*70}")
    print(f"Parsing: {source_name}")
    print('='*70)

    # Step 1: Create input stream from source text
    input_stream = InputStream(source_text)

    # Step 2: Create a lexer that feeds off the input stream
    lexer = SimpleCLexer(input_stream)

    # Step 3: Create a buffer of tokens pulled from the lexer
    token_stream = CommonTokenStream(lexer)

    # Step 4: Create a parser that feeds off the tokens buffer
    parser = SimpleCParser(token_stream)

    # Step 5: Remove default error listeners and add custom one
    parser.removeErrorListeners()
    error_listener = SyntaxErrorListener()
    parser.addErrorListener(error_listener)

    # Step 6: Begin parsing at the 'program' rule (entry point)
    tree = parser.program()

    return tree, error_listener, parser


def parse_file(filename):
    """
    Parse a C source file using the SimpleC grammar.
    
    Args:
        filename: Path to the C file to parse
    
    Returns:
        tuple: (parse_tree, error_listener)
    """
    try:
        with open(filename, 'r', encoding='utf-8') as handle:
            source_text = handle.read()

        tree, error_listener, parser = parse_source(source_text, filename)

        return tree, error_listener, parser, source_text
        
    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found!")
        return None, None, None, None
    except Exception as e:
        print(f"ERROR: Unexpected error occurred: {e}")
        return None, None, None, None


def print_parse_tree(tree, parser, indent=0):
    """
    Recursively print the parse tree in a readable format.
    
    Args:
        tree: The parse tree node
        parser: The parser instance (for rule names)
        indent: Current indentation level
    """
    # Get the node name
    if tree.getChildCount() == 0:
        # Leaf node (terminal/token)
        node_text = tree.getText()
        print("  " * indent + f"└─ {node_text}")
    else:
        # Internal node (parser rule)
        rule_name = parser.ruleNames[tree.getRuleIndex()] if hasattr(tree, 'getRuleIndex') else 'unknown'
        print("  " * indent + f"[{rule_name}]")
        
        # Recursively print children
        for i in range(tree.getChildCount()):
            print_parse_tree(tree.getChild(i), parser, indent + 1)


def print_analysis(tree):
    analysis = analyze_parse_tree(tree)

    print("\nIR Analysis: Variable Declaration Check")
    print("-" * 70)
    print("Symbol Table:")
    for name, line in analysis["symbol_table"].items():
        print(f"  {name} (declared at line {line})")

    if analysis["errors"]:
        print("\nAnalysis Errors:")
        for err in analysis["errors"]:
            print(f"  {err}")
    else:
        print("\nAnalysis Result: No undeclared assignments detected")


def test_file(filename):
    """
    Test a single C file: parse it and display results.
    
    Args:
        filename: Path to the C file to test
    """
    tree, error_listener, parser, source_text = parse_file(filename)
    
    if tree is None:
        return
    
    # Check if parsing succeeded
    if error_listener.has_errors():
        # Invalid file: print syntax errors
        print("\nPARSING FAILED - Syntax Errors Detected:")
        print("-" * 70)
        for error in error_listener.get_errors():
            print(f"  {error}")
        print("-" * 70)

        error_obj = error_listener.get_error_objects()[0]
        classification = classify_error_message(error_obj["msg"])

        print("\nError Classification:")
        print(f"  Fixable: {classification.fixable}")
        print(f"  Category: {classification.category}")
        print(f"  Reason: {classification.reason}")

        if classification.fixable:
            corrected_source, applied_fix = apply_correction(
                source_text,
                error_obj["line"],
                error_obj["column"],
                classification,
            )

            if applied_fix is None:
                print("\nFix Applied: None (no deterministic fix matched)")
                print("Re-Parsing Result: UNFIXABLE")
                return

            print(f"\nFix Applied: {applied_fix}")

            reparsed_tree, reparsed_listener, reparsed_parser = parse_source(
                corrected_source,
                f"{filename} (corrected)",
            )

            if reparsed_listener.has_errors():
                print("\nRe-Parsing Result: FAILED")
                print("-" * 70)
                for error in reparsed_listener.get_errors():
                    print(f"  {error}")
                print("-" * 70)
                print("Re-Parsing Result: UNFIXABLE")
                return

            print("\nRe-Parsing Result: SUCCESSFUL")
            print("-" * 70)
            print("Parse Tree:")
            print("-" * 70)

            print_parse_tree(reparsed_tree, reparsed_parser)

            print("\nS-Expression Format:")
            print(reparsed_tree.toStringTree(recog=reparsed_parser))
            print("-" * 70)

            print_analysis(reparsed_tree)
        else:
            print("\nFix Applied: None (error classified as unfixable)")
            print("Re-Parsing Result: UNFIXABLE")
    else:
        # Valid file: print parse tree
        print("\nPARSING SUCCESSFUL")
        print("-" * 70)
        print("Parse Tree:")
        print("-" * 70)
        
        print_parse_tree(tree, parser)
        
        # Alternative: Print S-expression format (compact)
        print("\nS-Expression Format:")
        print(tree.toStringTree(recog=parser))
        print("-" * 70)

        print_analysis(tree)


def main():
    """
    Main function: test all C files.
    """
    print("\n" + "="*70)
    print(" Simple C Parser - Test Suite")
    print("="*70)
    
    # List of test files to parse
    test_files = [
        'valid_example.c',
        'invalid_example1.c',
        'invalid_example2.c',
        'invalid_example3.c'
    ]
    
    # Parse each file and display results
    for filename in test_files:
        test_file(filename)
    
    print("\n" + "="*70)
    print(" Test Suite Complete")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
