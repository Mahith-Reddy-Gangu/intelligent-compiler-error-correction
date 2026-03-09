import json
import os
import random
from pathlib import Path

DATASET = Path("data/patch_synth.jsonl")
SEED_DIR = Path("data/seed_programs_generated")

SAMPLES = 5
random.seed(1337)

def read_some_dataset_rows(path: Path, k: int):
    # reservoir sampling-ish for big files
    chosen = []
    with path.open("r", encoding="utf-8") as f:
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

def load_seed_texts(seed_dir: Path, limit: int = 50):
    # load only first N seeds to keep it fast
    seeds = []
    for p in sorted(seed_dir.glob("*.c"))[:limit]:
        seeds.append((p.name, p.read_text(encoding="utf-8", errors="ignore")))
    return seeds

def normalize(s: str) -> str:
    # light normalization to make containment checks less brittle
    return "\n".join(line.rstrip() for line in s.replace("\r\n", "\n").split("\n")).strip()

def main():
    if not DATASET.exists():
        print(f"ERROR: missing {DATASET}")
        return
    if not SEED_DIR.exists():
        print(f"ERROR: missing {SEED_DIR}")
        return

    rows = read_some_dataset_rows(DATASET, SAMPLES)
    seeds = load_seed_texts(SEED_DIR, limit=80)

    print("=== Inspecting dataset samples vs seed containment (approx) ===")
    print(f"Dataset samples: {len(rows)}")
    print(f"Seeds loaded: {len(seeds)}\n")

    for idx, row in enumerate(rows, start=1):
        code = row.get("input", "")
        code_norm = normalize(code)
        lines = code_norm.count("\n") + 1 if code_norm else 0
        chars = len(code_norm)

        found_in = None
        for seed_name, seed_text in seeds:
            if code_norm and code_norm in normalize(seed_text):
                found_in = seed_name
                break

        print(f"[{idx}] family={row.get('family')} split_hint={row.get('split_hint')}")
        print(f"    input lines={lines} chars={chars}")
        print(f"    contained_in_seed: {found_in if found_in else '(not found in first 80 seeds)'}")
        print("")

if __name__ == "__main__":
    main()