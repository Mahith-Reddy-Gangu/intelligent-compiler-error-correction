import os

folder = "data/seed_programs_generated"

lengths = []

for file in os.listdir(folder):

    if not file.endswith(".c"):
        continue

    path = os.path.join(folder, file)

    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    lines = len(code.split("\n"))
    lengths.append(lines)

print("Seed program stats")
print("------------------")

print("count:", len(lengths))
print("min lines:", min(lengths))
print("max lines:", max(lengths))
print("avg lines:", sum(lengths) / len(lengths))