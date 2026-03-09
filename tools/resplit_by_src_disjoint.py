# tools/resplit_by_src_disjoint.py
import argparse
import hashlib
import json
import os
import random
from collections import defaultdict
from typing import Dict, List, Tuple


def _stable_hash(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="replace")).hexdigest()


def read_jsonl(path: str) -> List[dict]:
    rows: List[dict] = []
    bad = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                bad += 1
    if bad:
        print(f"⚠️ Bad JSON lines skipped: {bad}")
    return rows


def write_jsonl(path: str, rows: List[dict]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def split_by_unique_src(
    rows: List[dict],
    src_key: str,
    val_src_frac: float,
    seed: int,
) -> Tuple[List[dict], List[dict]]:
    """
    Split rows into train/val by unique src (rows grouped by src value).
    Guarantees src-disjoint splits.
    """
    groups: Dict[str, List[dict]] = defaultdict(list)
    for r in rows:
        if src_key not in r or not isinstance(r[src_key], str):
            raise ValueError(f"Row missing string field '{src_key}'. Keys={list(r.keys())}")
        groups[r[src_key]].append(r)

    unique_srcs = list(groups.keys())
    rng = random.Random(seed)
    rng.shuffle(unique_srcs)

    n_total = len(unique_srcs)
    n_val = int(round(n_total * val_src_frac))
    n_val = max(1, min(n_val, n_total - 1))  # keep both sides non-empty

    val_srcs = set(unique_srcs[:n_val])
    train_rows: List[dict] = []
    val_rows: List[dict] = []

    for src, g in groups.items():
        if src in val_srcs:
            val_rows.extend(g)
        else:
            train_rows.extend(g)

    # Sanity: disjoint src sets
    train_src_set = {r[src_key] for r in train_rows}
    val_src_set = {r[src_key] for r in val_rows}
    overlap = train_src_set.intersection(val_src_set)
    if overlap:
        raise RuntimeError(f"BUG: src overlap detected: {len(overlap)}")

    return train_rows, val_rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", required=True, help="Input JSONL (e.g., data/patch_synth.jsonl)")
    ap.add_argument("--out_dir", default="data/splits", help="Output directory for splits")
    ap.add_argument("--src_key", default="input", help="Source field name (your dataset uses 'input')")
    ap.add_argument("--split_hint_key", default="split_hint", help="Field name for split hint")
    ap.add_argument("--hard_hint_value", default="v2", help="Value that goes to hard split (default v2)")
    ap.add_argument("--val_src_frac", type=float, default=0.05, help="Fraction of UNIQUE src to put in val")
    ap.add_argument("--seed", type=int, default=1337, help="Random seed for deterministic split")
    args = ap.parse_args()

    rows = read_jsonl(args.in_path)
    print(f"Read rows: {len(rows)} from {args.in_path}")

    hard_rows: List[dict] = []
    pool_rows: List[dict] = []

    # 1) isolate hard split (v2)
    for r in rows:
        hint = r.get(args.split_hint_key, None)
        if hint == args.hard_hint_value:
            hard_rows.append(r)
        else:
            pool_rows.append(r)

    print(f"Hard ({args.hard_hint_value}) rows: {len(hard_rows)}")
    print(f"Pool rows (everything else): {len(pool_rows)}")

    # 2) split pool by unique src
    train_rows, val_rows = split_by_unique_src(
        pool_rows,
        src_key=args.src_key,
        val_src_frac=args.val_src_frac,
        seed=args.seed,
    )

    out_train = os.path.join(args.out_dir, "train.jsonl")
    out_val = os.path.join(args.out_dir, "val.jsonl")
    out_hard = os.path.join(args.out_dir, "hard_v2.jsonl")

    write_jsonl(out_train, train_rows)
    write_jsonl(out_val, val_rows)
    write_jsonl(out_hard, hard_rows)

    # stats
    train_src_unique = len({r[args.src_key] for r in train_rows})
    val_src_unique = len({r[args.src_key] for r in val_rows})
    hard_src_unique = len({r[args.src_key] for r in hard_rows}) if hard_rows else 0

    print("\n=== RESPLIT SUMMARY (src-disjoint) ===")
    print(f"Train rows: {len(train_rows)} | unique src: {train_src_unique}")
    print(f"Val rows:   {len(val_rows)} | unique src: {val_src_unique}")
    print(f"Hard rows:  {len(hard_rows)} | unique src: {hard_src_unique}")
    print(f"Wrote:\n  {out_train}\n  {out_val}\n  {out_hard}")

    # quick overlap checks
    train_src = {r[args.src_key] for r in train_rows}
    val_src = {r[args.src_key] for r in val_rows}
    hard_src = {r[args.src_key] for r in hard_rows}

    print("\n=== OVERLAP CHECKS (should be 0) ===")
    print(f"train ∩ val:  {len(train_src & val_src)}")
    print(f"train ∩ hard: {len(train_src & hard_src)}")
    print(f"val ∩ hard:   {len(val_src & hard_src)}")


if __name__ == "__main__":
    main()