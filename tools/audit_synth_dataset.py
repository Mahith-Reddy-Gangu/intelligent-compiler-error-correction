import os
import json
import random
import argparse
from collections import Counter

RNG_SEED = 999

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default=os.path.join("data", "patch_synth.jsonl"))
    ap.add_argument("--n", type=int, default=3000, help="How many lines to sample for audit")
    args = ap.parse_args()

    random.seed(RNG_SEED)

    with open(args.inp, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    total = len(lines)
    sample_n = min(args.n, total)
    sample = random.sample(lines, sample_n) if sample_n > 0 else []

    cmd_ctr = Counter()
    fam_ctr = Counter()
    split_ctr = Counter()

    bad_json = 0
    missing_fields = 0
    missing_err = 0
    err_marker_count = Counter()
    bad_target = 0

    for l in sample:
        try:
            ex = json.loads(l)
        except Exception:
            bad_json += 1
            continue

        if "input" not in ex or "target" not in ex or "family" not in ex:
            missing_fields += 1
            continue

        cmd = ex["target"]
        if not (cmd.startswith("INS ") or cmd.startswith("DEL ") or cmd.startswith("REP ")):
            bad_target += 1

        cmd_ctr[cmd] += 1
        fam_ctr[ex.get("family", "<none>")] += 1
        split_ctr[ex.get("split_hint", "<none>")] += 1

        inp = ex["input"]
        if "<ERR>" not in inp:
            missing_err += 1
        else:
            err_marker_count[inp.count("<ERR>")] += 1

    print("\n=== AUDIT SUMMARY ===")
    print("File:", args.inp)
    print("Total examples:", total)
    print("Sampled:", sample_n)
    print("Bad JSON:", bad_json)
    print("Missing required fields:", missing_fields)
    print("Missing <ERR> marker:", missing_err)
    print("Bad target format:", bad_target)

    print("\n<ERR> marker count distribution:")
    for k in sorted(err_marker_count):
        print(f"  {k}: {err_marker_count[k]}")

    print("\nTop families:")
    for fam, c in fam_ctr.most_common(30):
        print(f"  {fam:35s}  {c}")

    print("\nSplit hints:")
    for s, c in split_ctr.most_common():
        print(f"  {s:10s}  {c}")

    print("\nExample targets (top 15):")
    for cmd, c in cmd_ctr.most_common(15):
        print(f"  {cmd[:60]:60s}  {c}")

if __name__ == "__main__":
    main()