import json
import re
import random
from pathlib import Path
from collections import Counter

DATASET = Path("data/patch_synth.jsonl")
SEED_DIR = Path("data/seed_programs_generated")

SAMPLES = 30
SEED_LIMIT = None  # None = load all seeds
random.seed(1337)

# Very simple tokenization (works fine for C-like snippets)
TOKEN_RE = re.compile(r"[A-Za-z_]\w*|\d+|==|!=|<=|>=|\+\+|--|&&|\|\||[{}()\[\];,=+\-*/%<>?:]")

def tokenize(s: str):
    s = s.replace("\r\n", "\n")
    return TOKEN_RE.findall(s)

def normalize_tokens(tokens):
    # Replace identifiers and numbers to make it robust to renaming
    norm = []
    for t in tokens:
        if re.fullmatch(r"[A-Za-z_]\w*", t):
            # keep keywords as-is, collapse other identifiers
            if t in {"int","return","if","else","for","while","break","continue","main"}:
                norm.append(t)
            else:
                norm.append("ID")
        elif re.fullmatch(r"\d+", t):
            norm.append("NUM")
        else:
            norm.append(t)
    return norm

def load_seeds():
    paths = sorted(SEED_DIR.glob("*.c"))
    if SEED_LIMIT is not None:
        paths = paths[:SEED_LIMIT]
    seeds = []
    for p in paths:
        text = p.read_text(encoding="utf-8", errors="ignore")
        toks = normalize_tokens(tokenize(text))
        seeds.append((p.name, toks))
    return seeds

def read_sample_rows(k):
    chosen = []
    with DATASET.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            if len(chosen) < k:
                chosen.append(row)
            else:
                j = random.randint(1, i)
                if j <= k:
                    chosen[j - 1] = row
    return chosen

def contains_subseq(hay, needle):
    # exact contiguous subsequence search
    if not needle:
        return False
    n = len(needle)
    for i in range(0, len(hay) - n + 1):
        if hay[i:i+n] == needle:
            return True
    return False

def main():
    if not DATASET.exists():
        print(f"ERROR: missing {DATASET}")
        return
    if not SEED_DIR.exists():
        print(f"ERROR: missing {SEED_DIR}")
        return

    print("Loading seeds (tokenized+normalized)...")
    seeds = load_seeds()
    print(f"Loaded seeds: {len(seeds)}")

    rows = read_sample_rows(SAMPLES)
    print(f"Dataset samples: {len(rows)}\n")

    hits = 0
    families = Counter()

    for idx, row in enumerate(rows, start=1):
        src = row.get("input", "")
        fam = row.get("family")
        families[fam] += 1

        src_toks = normalize_tokens(tokenize(src))

        # Use only the first ~120 tokens to speed up; your snippets are short anyway
        src_toks = src_toks[:120]

        found = None
        for seed_name, seed_toks in seeds:
            if contains_subseq(seed_toks, src_toks):
                found = seed_name
                break

        if found:
            hits += 1

        print(f"[{idx:02d}] family={fam} split_hint={row.get('split_hint')}  tokens={len(src_toks)}")
        print(f"     fuzzy_contained_in_seed: {found if found else '(no match)'}")

    print("\n=== SUMMARY ===")
    print(f"Matches: {hits}/{len(rows)}")
    print("Top sampled families:", families.most_common(10))

if __name__ == "__main__":
    main()