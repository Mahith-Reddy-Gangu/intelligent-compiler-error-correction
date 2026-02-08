import re
from typing import Optional, Tuple

from .error_classifier import ErrorClassification


def apply_correction(
    source_text: str,
    error_line: int,
    error_column: int,
    classification: ErrorClassification,
) -> Tuple[str, Optional[str]]:
    if not classification.fixable:
        return source_text, None

    if classification.reason == "missing_semicolon":
        return _insert_semicolon_at_line(source_text, error_line)

    if classification.reason == "missing_rbrace":
        return _append_missing_rbrace(source_text)

    if classification.reason == "main_lparen_expected":
        return _fix_main_parentheses(source_text)

    return source_text, None


def _insert_semicolon_at_line(source_text: str, error_line: int) -> Tuple[str, Optional[str]]:
    lines = source_text.splitlines()
    index = error_line - 1

    if index < 0 or index >= len(lines):
        return source_text, None

    line_text = lines[index]
    if ";" in line_text:
        prev_index = index - 1
        if prev_index < 0:
            return source_text, None
        return _insert_semicolon_at_specific_line(lines, prev_index)

    return _insert_semicolon_at_specific_line(lines, index)


def _insert_semicolon_at_specific_line(lines, index: int) -> Tuple[str, Optional[str]]:
    line_text = lines[index]
    if ";" in line_text:
        return "\n".join(lines), None

    if "//" in line_text:
        code_part, sep, comment = line_text.partition("//")
        updated = code_part.rstrip() + ";" + " " + sep + comment
    else:
        updated = line_text.rstrip() + ";"

    lines[index] = updated

    return "\n".join(lines), "inserted missing ';'"


def _append_missing_rbrace(source_text: str) -> Tuple[str, Optional[str]]:
    stripped = source_text.rstrip()
    if stripped.endswith("}"):
        return source_text, None

    updated = stripped + "\n}"
    return updated, "inserted missing '}' at end"


def _fix_main_parentheses(source_text: str) -> Tuple[str, Optional[str]]:
    pattern = re.compile(r"\bmain\s*\{")

    if not pattern.search(source_text):
        return source_text, None

    updated = pattern.sub("main() {", source_text, count=1)
    return updated, "replaced '{' with '() {' after main"
