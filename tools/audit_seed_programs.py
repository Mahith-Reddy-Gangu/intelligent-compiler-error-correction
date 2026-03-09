import os
import re
import argparse
from collections import Counter, defaultdict

# Heuristic checks to approximate grammar construct coverage.
# This is not a parser; it's a "do we have these patterns at all?" audit.

RE_TYPES = re.compile(r"\b(int|float|char|void)\b")
RE_FUNCDEF = re.compile(r"\b(int|float|char|void)\s+[A-Za-z_]\w*\s*\(")
RE_PARAM_COMMA = re.compile(r"\([^)]*,[^)]*\)")  # any comma inside (...) on a single line
RE_CALL_WITH_COMMA = re.compile(r"\b[A-Za-z_]\w*\s*\([^)]*,[^)]*\)")
RE_DECL_COMMA = re.compile(r"\b(int|float|char|void)\b[^;]*,[^;]*;")

RE_FOR = re.compile(r"\bfor\s*\(")
RE_WHILE = re.compile(r"\bwhile\s*\(")
RE_IF = re.compile(r"\bif\s*\(")
RE_ELSE = re.compile(r"\belse\b")

RE_BREAK = re.compile(r"\bbreak\s*;")
RE_CONTINUE = re.compile(r"\bcontinue\s*;")
RE_RETURN = re.compile(r"\breturn\b")

RE_TERNARY = re.compile(r"\?.*:")
RE_COMMA_EXPR = re.compile(r",")  # we’ll refine by excluding obvious lists later

RE_INDEXING = re.compile(r"\[[^\]]+\]")      # a[i], a[i+1]
RE_ARRAY_DECL = re.compile(r"\b[A-Za-z_]\w*\s*\[[^\]]*\]")  # x[10] or x[]
RE_MULTI_DIM = re.compile(r"\[[^\]]*\]\s*\[[^\]]*\]")

RE_FLOAT_LIT = re.compile(r"\b\d+\.\d+\b")
RE_CHAR_LIT = re.compile(r"'(?:[^'\\\r\n]|\\[nrt'\\])'")

# Operators / tokens from grammar
OPS = {
    "==": re.compile(r"=="),
    "!=": re.compile(r"!="),
    "<=": re.compile(r"<="),
    ">=": re.compile(r">="),
    "&&": re.compile(r"&&"),
    "||": re.compile(r"\|\|"),
    "+=": re.compile(r"\+="),
    "-=": re.compile(r"-="),
    "*=": re.compile(r"\*="),
    "/=": re.compile(r"/="),
    "%=": re.compile(r"%="),
    "?:" : RE_TERNARY,
    "++": re.compile(r"\+\+"),
    "--": re.compile(r"--"),
    "!": re.compile(r"!"),
    "=": re.compile(r"="),
    "<": re.compile(r"<"),
    ">": re.compile(r">"),
    "+": re.compile(r"\+"),
    "-": re.compile(r"-"),
    "*": re.compile(r"\*"),
    "/": re.compile(r"/"),
    "%": re.compile(r"%"),
}

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def list_seed_files(seeds_dir: str):
    files = []
    for fn in sorted(os.listdir(seeds_dir)):
        if fn.endswith(".c"):
            files.append(os.path.join(seeds_dir, fn))
    return files

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds_dir", default=os.path.join("data", "seed_programs"))
    ap.add_argument("--show_missing_only", action="store_true")
    ap.add_argument("--top_k_files", type=int, default=8, help="Show example filenames for each feature")
    args = ap.parse_args()

    files = list_seed_files(args.seeds_dir)
    if not files:
        raise RuntimeError(f"No .c seeds found in {args.seeds_dir}")

    feature_hits = Counter()
    feature_examples = defaultdict(list)

    def hit(feature: str, filename: str):
        feature_hits[feature] += 1
        if len(feature_examples[feature]) < args.top_k_files:
            feature_examples[feature].append(os.path.basename(filename))

    for p in files:
        src = read_text(p)

        # Program structure
        if RE_FUNCDEF.search(src):
            hit("has_function_def", p)
        if src.count("{") >= 2 and src.count("}") >= 2:
            hit("nested_blocks_likely", p)

        # Statements
        if RE_IF.search(src):
            hit("if_statement", p)
        if RE_ELSE.search(src):
            hit("else_branch", p)
        if RE_WHILE.search(src):
            hit("while_loop", p)
        if RE_FOR.search(src):
            hit("for_loop", p)

        if RE_BREAK.search(src):
            hit("break_statement", p)
        if RE_CONTINUE.search(src):
            hit("continue_statement", p)
        if RE_RETURN.search(src):
            hit("return_statement", p)

        # Lists (params/args/decl lists)
        if RE_PARAM_COMMA.search(src):
            hit("comma_in_parens_param_or_call", p)
        if RE_CALL_WITH_COMMA.search(src):
            hit("call_with_multiple_args", p)
        if RE_DECL_COMMA.search(src):
            hit("multi_declarator_list", p)

        # Arrays / indexing
        if RE_INDEXING.search(src):
            hit("array_indexing", p)
        if RE_ARRAY_DECL.search(src) and RE_TYPES.search(src):
            hit("array_declaration", p)
        if RE_MULTI_DIM.search(src):
            hit("multi_dim_arrays", p)

        # Literals
        if RE_FLOAT_LIT.search(src):
            hit("float_literals", p)
        if RE_CHAR_LIT.search(src):
            hit("char_literals", p)

        # Ternary
        if RE_TERNARY.search(src):
            hit("ternary_operator", p)

        # Operators
        for op_name, pat in OPS.items():
            if pat.search(src):
                hit(f"op_{op_name}", p)

        # Empty statements
        if re.search(r"^\s*;\s*$", src, flags=re.MULTILINE):
            hit("empty_statement", p)

        # for-init as declaration heuristic: "for (int"
        if re.search(r"\bfor\s*\(\s*(int|float|char|void)\b", src):
            hit("for_init_declaration", p)

        # for-init as expression heuristic: "for (i="
        if re.search(r"\bfor\s*\(\s*[A-Za-z_]\w*\s*=", src):
            hit("for_init_expression", p)

    total = len(files)
    print("\n=== SEED COVERAGE AUDIT ===")
    print("Seeds dir:", args.seeds_dir)
    print("Total seed files:", total)

    # Core features you definitely want present at least once
    must_have = [
        "if_statement",
        "else_branch",
        "while_loop",
        "for_loop",
        "break_statement",
        "continue_statement",
        "return_statement",
        "empty_statement",
        "call_with_multiple_args",
        "multi_declarator_list",
        "array_declaration",
        "array_indexing",
        "multi_dim_arrays",
        "float_literals",
        "char_literals",
        "ternary_operator",
        "for_init_declaration",
        "for_init_expression",
        "op_==",
        "op_!=",
        "op_<=",
        "op_>=",
        "op_&&",
        "op_||",
        "op_+=",
        "op_-=",
        "op_*=",
        "op_/=",
        "op_%=",
        "op_++",
        "op_--",
        "op_!",
    ]

    # Print must-have status
    print("\n--- MUST-HAVE CHECK ---")
    missing = []
    for feat in must_have:
        cnt = feature_hits.get(feat, 0)
        if cnt == 0:
            missing.append(feat)
        if not args.show_missing_only:
            print(f"{feat:28s}  {cnt:4d}/{total}")

    if missing:
        print("\nMISSING FEATURES (add seeds that include these):")
        for feat in missing:
            print(" -", feat)
    else:
        print("\nAll must-have features are present at least once.")

    # Show examples for missing or all (depending)
    print("\n--- EXAMPLE FILES PER FEATURE ---")
    feats_to_show = missing if args.show_missing_only else sorted(feature_examples.keys())
    for feat in feats_to_show:
        ex = feature_examples.get(feat, [])
        if ex:
            print(f"{feat:28s}  e.g. {', '.join(ex)}")
        else:
            print(f"{feat:28s}  <none>")

    print("\nTip: Keep adding seeds until every missing feature shows up in multiple seeds (not just one).")

if __name__ == "__main__":
    main()