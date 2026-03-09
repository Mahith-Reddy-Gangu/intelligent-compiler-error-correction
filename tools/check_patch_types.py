import json
import sys
from collections import Counter

file = sys.argv[1]

counts = Counter()

with open(file) as f:
    for line in f:
        obj = json.loads(line)
        target = obj["target"]

        if target.startswith("INS"):
            counts["INS"] += 1
        elif target.startswith("DEL"):
            counts["DEL"] += 1
        elif target.startswith("REP"):
            counts["REP"] += 1

print("\nPatch type distribution:")
for k,v in counts.items():
    print(k, v)