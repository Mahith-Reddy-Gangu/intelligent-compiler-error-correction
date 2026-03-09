import json
import os
import random
from collections import defaultdict
from typing import Dict, List


INPUT_JSONL = "data/splits/train.jsonl"
OUTPUT_DIR = "zexamples/generated_ml_cases"
NUM_CASES = 10
SEED = 42

# Families we want to target for ML-style testing.
PREFERRED_FAMILIES = {
    "missing_lbrack",
    "missing_rparen",
    "missing_lparen_control",
    "mismatch_lparen_to_lbrack",
    "mismatch_rparen_to_rbrack",
    "illegal_char",
    "missing_lparen_general",
}

HEADER = """int calc(int x, int y) {
    return x + y;
}

int guard(int x, int y) {
    return x - y;
}
"""


def load_jsonl(path: str):
    rows = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Skipping bad JSON line {i}: {e}")
                print(f"  Content preview: {line[:120]!r}")
    return rows

def collect_by_family(rows: List[dict]) -> Dict[str, List[dict]]:
    out: Dict[str, List[dict]] = defaultdict(list)
    for row in rows:
        family = row.get("family", "").strip()
        if family:
            out[family].append(row)
    return out


def make_program_for_family(family: str, idx: int) -> str:
    """
    Generate a small C program with exactly one intended ML-style syntax error.
    These are aligned to your observed dataset families, not to generic random errors.
    """

    if family == "missing_lparen_control":
        return f"""{HEADER}
int main() {{
    int x = {idx % 5};
    if x == {idx % 5}) {{
        return 1;
    }}
    return 0;
}}
"""

    if family == "missing_rparen":
        return f"""{HEADER}
int main() {{
    int x = 1;
    int y = 2;
    if ((x == 0) || (y == 2) {{
        return 1;
    }}
    return 0;
}}
"""

    if family == "missing_lbrack":
        return f"""{HEADER}
int main() {{
    int m2[3][4];
    m2[1]2] = 7;
    return 0;
}}
"""

    if family == "mismatch_lparen_to_lbrack":
        return f"""{HEADER}
int main() {{
    int x = 1;
    int y = 2;
    calc[x, y);
    return 0;
}}
"""

    if family == "mismatch_rparen_to_rbrack":
        return f"""{HEADER}
int main() {{
    int x = 1;
    int y = 2;
    guard(x, y];
    return 0;
}}
"""

    if family == "illegal_char":
        return f"""{HEADER}
int main() {{
    int @x = 1;
    return 0;
}}
"""

    if family == "missing_lparen_general":
        return f"""{HEADER}
int main() {{
    int x = 1;
    int y = 2;
    calc x, y);
    return 0;
}}
"""

    # fallback
    return f"""{HEADER}
int main() {{
    int x = 1;
    int y = 2;
    guard(x, y];
    return 0;
}}
"""


def choose_families(family_map: Dict[str, List[dict]], num_cases: int) -> List[str]:
    available_preferred = [f for f in PREFERRED_FAMILIES if f in family_map]
    if not available_preferred:
        available_preferred = list(family_map.keys())

    if not available_preferred:
        raise RuntimeError("No families found in dataset.")

    chosen: List[str] = []
    i = 0
    while len(chosen) < num_cases:
        chosen.append(available_preferred[i % len(available_preferred)])
        i += 1
    return chosen


def main() -> None:
    random.seed(SEED)

    rows = load_jsonl(INPUT_JSONL)
    family_map = collect_by_family(rows)

    print("Loaded rows:", len(rows))
    print("Found families:", ", ".join(sorted(family_map.keys())))

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    chosen_families = choose_families(family_map, NUM_CASES)

    manifest: List[dict] = []

    for i, family in enumerate(chosen_families, start=1):
        code = make_program_for_family(family, i)
        filename = f"ml_case_{i:02d}_{family}.c"
        path = os.path.join(OUTPUT_DIR, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        manifest.append(
            {
                "index": i,
                "family": family,
                "file": path,
            }
        )

    manifest_path = os.path.join(OUTPUT_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\nGenerated files:")
    for item in manifest:
        print(f"  [{item['index']:02d}] {item['family']} -> {item['file']}")

    print(f"\nManifest written to: {manifest_path}")


if __name__ == "__main__":
    main()