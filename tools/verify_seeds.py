import os
import argparse
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def _try_import_parser():
    try:
        from antlr4 import InputStream, CommonTokenStream
        from antlr4.error.ErrorListener import ErrorListener
        from generated.SimpleCLexer import SimpleCLexer
        from generated.SimpleCParser import SimpleCParser
        return InputStream, CommonTokenStream, ErrorListener, SimpleCLexer, SimpleCParser
    except Exception:
        return None

def _parse_errors(src: str):
    pack = _try_import_parser()
    if pack is None:
        raise RuntimeError("ANTLR parser not importable. Generate ANTLR files and run from project root.")

    InputStream, CommonTokenStream, ErrorListener, SimpleCLexer, SimpleCParser = pack

    class EL(ErrorListener):
        def __init__(self, stage: str):
            super().__init__()
            self.stage = stage
            self.errs = []

        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            self.errs.append(f"L{line}:{column} {self.stage}: {msg}")

    inp = InputStream(src)
    lex = SimpleCLexer(inp)
    lex_el = EL("LEX")
    lex.removeErrorListeners()
    lex.addErrorListener(lex_el)

    tok = CommonTokenStream(lex)
    par = SimpleCParser(tok)
    par_el = EL("PARSE")
    par.removeErrorListeners()
    par.addErrorListener(par_el)

    par.program()
    return lex_el.errs + par_el.errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds_dir", default=os.path.join("data", "seed_programs"))
    args = ap.parse_args()

    seeds = []
    for fn in sorted(os.listdir(args.seeds_dir)):
        if fn.endswith(".c"):
            seeds.append(os.path.join(args.seeds_dir, fn))

    if not seeds:
        raise RuntimeError(f"No .c files found in {args.seeds_dir}")

    bad = 0
    for p in seeds:
        with open(p, "r", encoding="utf-8") as f:
            src = f.read()
        errs = _parse_errors(src)
        if errs:
            bad += 1
            print("\n--- BAD SEED ---")
            print(p)
            for e in errs[:10]:
                print(" ", e)

    print(f"\nChecked {len(seeds)} seeds. Bad seeds: {bad}")
    if bad:
        sys.exit(1)

if __name__ == "__main__":
    main()