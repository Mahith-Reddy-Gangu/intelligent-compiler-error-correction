import json
from pathlib import Path
from collections import defaultdict, Counter

SRC_KEY = "input"
TGT_KEY = "target"

def load_rows(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows

def canonicalize(rows):
    # group all targets by identical input
    groups = defaultdict(list)
    for r in rows:
        groups[r[SRC_KEY]].append(r)

    out = []
    dropped = 0
    multi = 0

    for src, items in groups.items():
        tgts = [it[TGT_KEY] for it in items]
        c = Counter(tgts)
        if len(c) > 1:
            multi += 1
        # pick most common target; deterministic tie-break by lexicographic
        best_tgt = sorted(c.items(), key=lambda x: (-x[1], x[0]))[0][0]

        # keep ONE representative row with best_tgt
        kept = None
        for it in items:
            if it[TGT_KEY] == best_tgt:
                kept = it
                break

        out.append(kept)
        dropped += (len(items) - 1)

    return out, dropped, multi, len(groups)

def write_rows(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def main():
    train_in = Path("data/splits/train.jsonl")
    val_in   = Path("data/splits/val.jsonl")
    hard_in  = Path("data/splits/hard_v2.jsonl")

    out_dir = Path("data/splits_canon")

    train_rows = load_rows(train_in)
    val_rows   = load_rows(val_in)
    hard_rows  = load_rows(hard_in)

    train_c, dtr, mtr, utr = canonicalize(train_rows)
    val_c,   dva, mva, uva = canonicalize(val_rows)

    print("=== CANONICALIZE BY INPUT ===")
    print(f"train: in={len(train_rows)} unique_inputs={utr} out={len(train_c)} dropped={dtr} multi_input_conflicts={mtr}")
    print(f"val:   in={len(val_rows)} unique_inputs={uva} out={len(val_c)} dropped={dva} multi_input_conflicts={mva}")
    print(f"hard:  unchanged={len(hard_rows)}")

    write_rows(out_dir / "train.jsonl", train_c)
    write_rows(out_dir / "val.jsonl", val_c)
    write_rows(out_dir / "hard_v2.jsonl", hard_rows)

    print("\nWrote:")
    print(" ", out_dir / "train.jsonl")
    print(" ", out_dir / "val.jsonl")
    print(" ", out_dir / "hard_v2.jsonl")

if __name__ == "__main__":
    main()