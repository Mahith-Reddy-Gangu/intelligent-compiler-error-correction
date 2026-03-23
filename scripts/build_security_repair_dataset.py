import os
import json
import random
from typing import Dict, List, Tuple

random.seed(42)

TRAIN_SAMPLES = 24000
VAL_SAMPLES = 2400

OUTPUT_DIR = "data/security_patch_dataset_v1"
TRAIN_PATH = os.path.join(OUTPUT_DIR, "train.jsonl")
VAL_PATH = os.path.join(OUTPUT_DIR, "val.jsonl")


VAR_NAMES = [
    "buf", "name", "input", "cmd", "dest", "src",
    "message", "text", "payload", "user", "password"
]

FORMATS = [
    '"User: %s"',
    '"Hello %s"',
    '"Value=%d"',
    '"%s-%d"',
    '"[%s]"',
    '"Result: %s"'
]

STRING_VALUES = [
    '"Mahith"',
    '"admin"',
    '"guest"',
    '"hello"',
    '"world"',
    '"unsafe_input"',
    '"payload"',
]

INT_VALUES = ["1", "7", "10", "42", "99", "123"]

FUNCTION_NAMES = [
    "process",
    "handle_input",
    "copy_name",
    "build_message",
    "read_data",
    "demo",
    "log_user",
    "run_case"
]


def normalize_spaces(s: str) -> str:
    return " ".join(s.strip().split())


def make_prompt(category: str, line_no: int, code: str) -> str:
    return (
        f"SECURITY_FIX\n"
        f"CATEGORY {category}\n"
        f"LINE {line_no}\n\n"
        f"<CODE>\n{code}\n</CODE>"
    )


def make_target(line_no: int, fixed_line: str) -> str:
    return f"REPLACE_LINE {line_no} {normalize_spaces(fixed_line)}"


def choose_buffer_size() -> int:
    return random.choice([8, 12, 16, 24, 32, 48, 64, 128])


def choose_var(exclude: str = "") -> str:
    choices = [v for v in VAR_NAMES if v != exclude]
    return random.choice(choices)


def choose_func() -> str:
    return random.choice(FUNCTION_NAMES)


def build_record(
    family: str,
    category: str,
    code: str,
    line_no: int,
    vulnerable_line: str,
    fixed_line: str,
    split_hint: str
) -> Dict:
    return {
        "task": "security_repair_line",
        "split_hint": split_hint,
        "family": family,
        "category": category,
        "error_line": line_no,
        "input": make_prompt(category, line_no, code),
        "target": make_target(line_no, fixed_line),
        "metadata": {
            "vulnerable_line": normalize_spaces(vulnerable_line),
            "fixed_line": normalize_spaces(fixed_line)
        }
    }


def case_gets(split_hint: str) -> Dict:
    buf = choose_var()
    size = choose_buffer_size()
    func = choose_func()

    lines = [
        "#include <stdio.h>",
        "",
        f"void {func}(void) {{",
        f"    char {buf}[{size}];",
        f"    gets({buf});",
        f'    printf("%s\\n", {buf});',
        "}"
    ]

    vuln_line_no = 5
    vulnerable_line = lines[vuln_line_no - 1]
    fixed_line = f"    fgets({buf}, sizeof({buf}), stdin);"
    code = "\n".join(lines)

    return build_record(
        family="gets_to_fgets",
        category="UNSAFE_INPUT",
        code=code,
        line_no=vuln_line_no,
        vulnerable_line=vulnerable_line,
        fixed_line=fixed_line,
        split_hint=split_hint
    )


def case_strcpy(split_hint: str) -> Dict:
    dest = choose_var()
    src = choose_var(exclude=dest)
    dsize = choose_buffer_size()
    ssize = max(dsize + random.choice([4, 8, 12]), dsize + 1)
    func = choose_func()

    lines = [
        "#include <stdio.h>",
        "#include <string.h>",
        "",
        f"void {func}(void) {{",
        f"    char {dest}[{dsize}];",
        f"    char {src}[{ssize}] = {random.choice(STRING_VALUES)};",
        f"    strcpy({dest}, {src});",
        f'    printf("%s\\n", {dest});',
        "}"
    ]

    vuln_line_no = 7
    vulnerable_line = lines[vuln_line_no - 1]
    fixed_line = f'    snprintf({dest}, sizeof({dest}), "%s", {src});'
    code = "\n".join(lines)

    return build_record(
        family="strcpy_to_snprintf",
        category="UNBOUNDED_COPY",
        code=code,
        line_no=vuln_line_no,
        vulnerable_line=vulnerable_line,
        fixed_line=fixed_line,
        split_hint=split_hint
    )


def case_strcat(split_hint: str) -> Dict:
    dest = choose_var()
    src = choose_var(exclude=dest)
    dsize = choose_buffer_size()
    func = choose_func()

    lines = [
        "#include <stdio.h>",
        "#include <string.h>",
        "",
        f"void {func}(void) {{",
        f"    char {dest}[{dsize}] = {random.choice(STRING_VALUES)};",
        f"    char {src}[{dsize}] = {random.choice(STRING_VALUES)};",
        f"    strcat({dest}, {src});",
        f'    printf("%s\\n", {dest});',
        "}"
    ]

    vuln_line_no = 7
    vulnerable_line = lines[vuln_line_no - 1]
    fixed_line = f"    strncat({dest}, {src}, sizeof({dest}) - strlen({dest}) - 1);"
    code = "\n".join(lines)

    return build_record(
        family="strcat_to_strncat",
        category="UNBOUNDED_CONCAT",
        code=code,
        line_no=vuln_line_no,
        vulnerable_line=vulnerable_line,
        fixed_line=fixed_line,
        split_hint=split_hint
    )


def case_sprintf_str(split_hint: str) -> Dict:
    dest = choose_var()
    src = choose_var(exclude=dest)
    dsize = choose_buffer_size()
    func = choose_func()
    fmt = random.choice(['"%s"', '"User=%s"', '"[%s]"', '"Hello %s"'])

    lines = [
        "#include <stdio.h>",
        "",
        f"void {func}(void) {{",
        f"    char {dest}[{dsize}];",
        f"    char {src}[{dsize * 2}] = {random.choice(STRING_VALUES)};",
        f"    sprintf({dest}, {fmt}, {src});",
        f'    printf("%s\\n", {dest});',
        "}"
    ]

    vuln_line_no = 6
    vulnerable_line = lines[vuln_line_no - 1]
    fixed_line = f"    snprintf({dest}, sizeof({dest}), {fmt}, {src});"
    code = "\n".join(lines)

    return build_record(
        family="sprintf_to_snprintf_str",
        category="UNBOUNDED_FORMAT",
        code=code,
        line_no=vuln_line_no,
        vulnerable_line=vulnerable_line,
        fixed_line=fixed_line,
        split_hint=split_hint
    )


def case_sprintf_int(split_hint: str) -> Dict:
    dest = choose_var()
    dsize = choose_buffer_size()
    func = choose_func()
    value = random.choice(INT_VALUES)
    fmt = random.choice(['"%d"', '"Value=%d"', '"[%d]"'])

    lines = [
        "#include <stdio.h>",
        "",
        f"void {func}(void) {{",
        f"    char {dest}[{dsize}];",
        f"    int n = {value};",
        f"    sprintf({dest}, {fmt}, n);",
        f'    printf("%s\\n", {dest});',
        "}"
    ]

    vuln_line_no = 6
    vulnerable_line = lines[vuln_line_no - 1]
    fixed_line = f"    snprintf({dest}, sizeof({dest}), {fmt}, n);"
    code = "\n".join(lines)

    return build_record(
        family="sprintf_to_snprintf_int",
        category="UNBOUNDED_FORMAT",
        code=code,
        line_no=vuln_line_no,
        vulnerable_line=vulnerable_line,
        fixed_line=fixed_line,
        split_hint=split_hint
    )


def case_scanf_s(split_hint: str) -> Dict:
    buf = choose_var()
    size = random.choice([8, 12, 16, 24, 32, 64])
    width = size - 1
    func = choose_func()

    lines = [
        "#include <stdio.h>",
        "",
        f"void {func}(void) {{",
        f"    char {buf}[{size}];",
        f'    scanf("%s", {buf});',
        f'    printf("%s\\n", {buf});',
        "}"
    ]

    vuln_line_no = 5
    vulnerable_line = lines[vuln_line_no - 1]
    fixed_line = f'    scanf("%{width}s", {buf});'
    code = "\n".join(lines)

    return build_record(
        family="scanf_percent_s_bounded",
        category="UNBOUNDED_INPUT",
        code=code,
        line_no=vuln_line_no,
        vulnerable_line=vulnerable_line,
        fixed_line=fixed_line,
        split_hint=split_hint
    )


CASE_BUILDERS = [
    case_gets,
    case_strcpy,
    case_strcat,
    case_sprintf_str,
    case_sprintf_int,
    case_scanf_s,
]


def build_split(n: int, split_hint: str) -> List[Dict]:
    records = []
    for _ in range(n):
        builder = random.choice(CASE_BUILDERS)
        records.append(builder(split_hint))
    return records


def write_jsonl(path: str, records: List[Dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    train_records = build_split(TRAIN_SAMPLES, "train")
    val_records = build_split(VAL_SAMPLES, "val")

    write_jsonl(TRAIN_PATH, train_records)
    write_jsonl(VAL_PATH, val_records)

    print("=" * 70)
    print("Security repair dataset generated successfully")
    print("=" * 70)
    print(f"Train path : {TRAIN_PATH}")
    print(f"Val path   : {VAL_PATH}")
    print(f"Train rows : {len(train_records)}")
    print(f"Val rows   : {len(val_records)}")
    print("=" * 70)

    print("\nSample record:\n")
    print(json.dumps(train_records[0], indent=2))


if __name__ == "__main__":
    main()