import json
import hashlib
from pathlib import Path
from collections import Counter, defaultdict

TRAIN = Path("data/splits/train.jsonl")
VAL   = Path("data/splits/val.jsonl")
HARD  = Path("data/splits/hard_v2.jsonl")

SRC_KEY = "input"

def h(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()

def read_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows

def split_hint_counts(rows):
    c = Counter()
    for r in rows:
        c[r.get("split_hint", "<missing>")] += 1
    return c

def src_hash_set(rows):
    s = set()
    for r in rows:
        src = r.get(SRC_KEY, "")
        s.add(h(src))
    return s

def show_overlap_examples(rows_a, rows_b, overlap_hashes, limit=5):
    # map hash -> one example
    map_a = {}
    for r in rows_a:
        map_a.setdefault(h(r.get(SRC_KEY, "")), r.get(SRC_KEY, ""))
    map_b = {}
    for r in rows_b:
        map_b.setdefault(h(r.get(SRC_KEY, "")), r.get(SRC_KEY, ""))

    shown = 0
    for hh in list(overlap_hashes)[:limit]:
        print("\n--- overlap example ---")
        print("A snippet:", (map_a.get(hh,"")[:160]).replace("\n","\\n"))
        print("B snippet:", (map_b.get(hh,"")[:160]).replace("\n","\\n"))
        shown += 1
    if shown == 0:
        print("(no overlap examples to show)")

def main():
    train = read_jsonl(TRAIN)
    val   = read_jsonl(VAL)
    hard  = read_jsonl(HARD)

    print("=== COUNTS ===")
    print("train:", len(train))
    print("val:  ", len(val))
    print("hard: ", len(hard))

    print("\n=== SPLIT HINTS ===")
    print("train:", split_hint_counts(train))
    print("val:  ", split_hint_counts(val))
    print("hard: ", split_hint_counts(hard))

    # hard_v2 must be only v2
    bad = [r for r in hard if r.get("split_hint") != "v2"]
    if bad:
        print(f"\n❌ hard_v2 contains non-v2 rows: {len(bad)}")
        print("Example split_hint values:", Counter([r.get("split_hint") for r in bad]))
    else:
        print("\n✅ hard_v2 contains only split_hint=v2")

    # src overlap
    tr = src_hash_set(train)
    va = src_hash_set(val)
    ha = src_hash_set(hard)

    ov_tr_va = tr & va
    ov_tr_ha = tr & ha
    ov_va_ha = va & ha

    print("\n=== SRC OVERLAP (input) ===")
    print("train ∩ val :", len(ov_tr_va))
    print("train ∩ hard:", len(ov_tr_ha))
    print("val   ∩ hard:", len(ov_va_ha))

    if ov_tr_va:
        print("\n❌ train/val overlap examples:")
        show_overlap_examples(train, val, ov_tr_va, limit=5)
    if ov_tr_ha:
        print("\n❌ train/hard overlap examples:")
        show_overlap_examples(train, hard, ov_tr_ha, limit=5)
    if ov_va_ha:
        print("\n❌ val/hard overlap examples:")
        show_overlap_examples(val, hard, ov_va_ha, limit=5)

    if not ov_tr_va and not ov_tr_ha and not ov_va_ha:
        print("\n✅ All splits are src-disjoint on `input`")

if __name__ == "__main__":
    main()