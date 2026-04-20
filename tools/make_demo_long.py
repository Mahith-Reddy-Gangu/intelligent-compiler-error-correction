from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
SEED_DIR = ROOT / "data" / "seed_programs_generated"
OUT_DIR = ROOT / "examples" / "week12_benchmark"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VALID_OUT = OUT_DIR / "demo_long_valid.c"
CORRUPT_OUT = OUT_DIR / "demo_long_corrupt.c"

# Pick a few seed files from your corpus
seed_files = [
    "seedg_003.c",
    "seedg_011.c",
    "seedg_027.c",
    "seedg_041.c",
    "seedg_058.c",
    "seedg_072.c",
    "seedg_104.c",
    "seedg_121.c",
    "seedg_166.c",
    "seedg_203.c",
]

def safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def rename_main(code: str, idx: int) -> str:
    # Rename main to helper function
    return re.sub(r'\bmain\s*\(', f'demo_part_{idx}(', code)

parts = []
for i, fname in enumerate(seed_files):
    path = SEED_DIR / fname
    code = safe_read(path)
    code = rename_main(code, i)
    parts.append(f"\n/* ===== {fname} ===== */\n{code}\n")

driver = "\nint main() {\n    int total = 0;\n"
for i in range(len(seed_files)):
    driver += f"    total = total + demo_part_{i}();\n"
driver += "    return total;\n}\n"

valid_code = "\n".join(parts) + "\n" + driver
VALID_OUT.write_text(valid_code, encoding="utf-8")

lines = valid_code.splitlines()

# Controlled, demo-friendly repairable errors
error_injections = {
    25:  lambda s: s.replace(";", "", 1),
    60:  lambda s: s.replace("if (", "if ", 1),
    110: lambda s: s.replace(",", "", 1),
    170: lambda s: s.replace("while", "whlie", 1),
    230: lambda s: s.replace(")", "", 1),
    300: lambda s: s.replace("return", "retun", 1),
    360: lambda s: s.replace(";", "", 1),
    410: lambda s: s.replace(",", "", 1),
}

for idx, fn in error_injections.items():
    if 0 <= idx < len(lines):
        lines[idx] = fn(lines[idx])

CORRUPT_OUT.write_text("\n".join(lines), encoding="utf-8")

print("Created:")
print(" ", VALID_OUT)
print(" ", CORRUPT_OUT)
print("Valid file lines:", len(valid_code.splitlines()))
print("Corrupt file lines:", len(lines))