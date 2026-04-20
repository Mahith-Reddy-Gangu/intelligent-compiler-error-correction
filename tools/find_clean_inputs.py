from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent

search_dirs = [
    ROOT / "examples",
    ROOT / "data" / "seed_programs_generated",
]

c_files = []
for d in search_dirs:
    if d.exists():
        c_files.extend(d.rglob("*.c"))

print(f"Found {len(c_files)} C files\n")

clean = []
parsed = []
partial = []

for f in c_files:
    cmd = ["python", "test_parser.py", "--file", str(f)]
    result = subprocess.run(cmd, capture_output=True, text=True)

    out = result.stdout + "\n" + result.stderr

    if "PARSING SUCCESSFUL" in out:
        parsed.append(str(f))

        if "Total semantic issues: 0" in out:
            clean.append(str(f))
        elif "Total semantic issues:" in out:
            partial.append(str(f))

print("=" * 70)
print("FILES THAT PARSE:")
for x in parsed[:100]:
    print(x)

print("\n" + "=" * 70)
print("FILES WITH ZERO SEMANTIC ISSUES:")
for x in clean[:100]:
    print(x)

print("\n" + "=" * 70)
print("FILES THAT PARSE BUT STILL HAVE SEMANTIC ISSUES:")
for x in partial[:100]:
    print(x)