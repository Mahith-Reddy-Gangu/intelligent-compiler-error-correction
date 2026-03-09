import json
import statistics

path = "data/patch_synth.jsonl"

line_counts = []
char_counts = []

with open(path, "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)

        code = obj["input"]

        lines = code.split("\n")
        line_counts.append(len(lines))
        char_counts.append(len(code))


print("Program length statistics")
print("------------------------")

print("Total programs:", len(line_counts))

print("\nLines:")
print("min:", min(line_counts))
print("max:", max(line_counts))
print("avg:", round(statistics.mean(line_counts), 2))

print("\nCharacters:")
print("min:", min(char_counts))
print("max:", max(char_counts))
print("avg:", round(statistics.mean(char_counts), 2))