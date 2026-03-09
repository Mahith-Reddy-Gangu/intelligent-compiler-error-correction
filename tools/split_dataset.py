import os
import json
import argparse
import random

RNG_SEED = 2026

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default=os.path.join("data", "patch_synth.jsonl"))
    ap.add_argument("--out_dir", default=os.path.join("data", "splits"))
    ap.add_argument("--val_ratio", type=float, default=0.05)
    args = ap.parse_args()

    random.seed(RNG_SEED)
    os.makedirs(args.out_dir, exist_ok=True)

    train_path = os.path.join(args.out_dir, "train.jsonl")
    val_path = os.path.join(args.out_dir, "val.jsonl")
    hard_path = os.path.join(args.out_dir, "hard_v2.jsonl")

    train_w = open(train_path, "w", encoding="utf-8")
    val_w = open(val_path, "w", encoding="utf-8")
    hard_w = open(hard_path, "w", encoding="utf-8")

    n = 0
    n_train = 0
    n_val = 0
    n_hard = 0

    with open(args.inp, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n += 1
            ex = json.loads(line)

            if ex.get("split_hint") == "v2":
                hard_w.write(json.dumps(ex, ensure_ascii=False) + "\n")
                n_hard += 1
                continue

            if random.random() < args.val_ratio:
                val_w.write(json.dumps(ex, ensure_ascii=False) + "\n")
                n_val += 1
            else:
                train_w.write(json.dumps(ex, ensure_ascii=False) + "\n")
                n_train += 1

    train_w.close()
    val_w.close()
    hard_w.close()

    print(f"Total: {n}")
    print(f"Train: {n_train}  Val: {n_val}  Hard(v2): {n_hard}")
    print("Wrote:", train_path)
    print("Wrote:", val_path)
    print("Wrote:", hard_path)

if __name__ == "__main__":
    main()