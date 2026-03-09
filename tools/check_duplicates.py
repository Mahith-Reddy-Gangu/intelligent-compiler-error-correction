import json
import sys

file = sys.argv[1]

seen = set()
dup = 0
total = 0

with open(file) as f:
    for line in f:
        obj = json.loads(line)
        inp = obj["input"]

        total += 1
        if inp in seen:
            dup += 1
        else:
            seen.add(inp)

print("Total:", total)
print("Unique:", len(seen))
print("Duplicates:", dup)