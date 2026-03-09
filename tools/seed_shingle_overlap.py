import json
import re
import random
from pathlib import Path
from collections import defaultdict

DATASET = Path("data/patch_synth.jsonl")
SEED_DIR = Path("data/seed_programs_generated")

SAMPLES = 40          # dataset examples to inspect
SHINGLE = 18          # chunk size in tokens (try 12, 18, 25)
MAX_SHINGLES_PER_EX = 30  # limit per example to keep it fast
SEED_LIMIT = None     # None = load all seeds

random.seed(1337)

TOKEN_RE = re.compile(
    r"[A-Za-z_]\w*|\d+|==|!=|<=|>=|\+\+|--|&&|\|\||[{}()\[\];,=+\-*/%<>?:]"
)

KEYWORDS = {"int","return","if","else","for","while","break","continue","main"}

def tokenize(s: str):
    s = s.replace("\r\n", "\n")
    return TOKEN_RE.findall(s)

def normalize_tokens(tokens):
    norm = []
    for t in tokens:
        if re.fullmatch(r"[A-Za-z_]\w*", t):
            norm.append(t if t in KEYWORDS else "ID")
        elif re.fullmatch(r"\d+", t):
            norm.append("NUM")
        else:
            norm.append(t)
    return norm

def shingles(tokens, k):
    if len(tokens) < k:
        return []
    return [tuple(tokens[i:i+k]) for i in range(len(tokens) - k + 1)]

def load_seed_shingle_index(k):
    paths = sorted(SEED_DIR.glob("*.c"))
    if SEED_LIMIT is not None:
        paths = paths[:SEED_LIMIT]

    index = defaultdict(set)  # shingle -> set(seed_name)
    for p in paths:
        text = p.read_text(encoding="utf-8", errors="ignore")
        toks = normalize_tokens(tokenize(text))
        for sh in shingles(toks, k):
            index[sh].add(p.name)

    return index, len(paths)

def reservoir_sample_jsonl(path: Path, k: int):
    chosen = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if len(chosen) < k:
                chosen.append(row)
            else:
                j = random.randint(1, i)
                if j <= k:
                    chosen[j - 1] = row
    return chosen

def main():
    if not DATASET.exists():
        print(f"ERROR: missing {DATASET}")
        return
    if not SEED_DIR.exists():
        print(f"ERROR: missing {SEED_DIR}")
        return

    print(f"Building seed shingle index (k={SHINGLE}) ...")
    index, seed_count = load_seed_shingle_index(SHINGLE)
    print(f"Loaded seeds: {seed_count}")
    print(f"Unique shingles indexed: {len(index)}")

    rows = reservoir_sample_jsonl(DATASET, SAMPLES)
    print(f"\nDataset samples: {len(rows)}\n")

    hit_examples = 0

    for idx, row in enumerate(rows, start=1):
        src = row.get("input", "")
        fam = row.get("family")
        hint = row.get("split_hint")

        toks = normalize_tokens(tokenize(src))
        shs = shingles(toks, SHINGLE)

        # sample some shingles to keep it fast
        if len(shs) > MAX_SHINGLES_PER_EX:
            shs = random.sample(shs, MAX_SHINGLES_PER_EX)

        found_seeds = set()
        for sh in shs:
            if sh in index:
                found_seeds |= index[sh]
                if len(found_seeds) >= 3:
                    break

        ok = len(found_seeds) > 0
        if ok:
            hit_examples += 1

        print(f"[{idx:02d}] family={fam} split_hint={hint}  tokens={len(toks)}")
        if ok:
            seeds_preview = ", ".join(sorted(list(found_seeds))[:3])
            print(f"     ✅ shingle overlap found in: {seeds_preview}{' ...' if len(found_seeds)>3 else ''}")
        else:
            print("     ❌ no shingle overlap found")

    print("\n=== SUMMARY ===")
    print(f"Examples with any seed overlap: {hit_examples}/{len(rows)}")
    if hit_examples == 0:
        print("Interpretation: dataset likely NOT derived from seeds, or seeds are irrelevant to generator.")
    else:
        print("Interpretation: seeds likely influenced dataset (at least partially).")

if __name__ == "__main__":
    main()