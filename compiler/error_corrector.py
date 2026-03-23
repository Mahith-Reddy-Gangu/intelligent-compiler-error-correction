import re
from typing import Optional, Tuple, List

from .error_classifier import ErrorClassification


def apply_correction(
    source_text: str,
    error_line: int,
    error_column: int,
    classification: ErrorClassification,
) -> Tuple[str, Optional[str]]:
    """
    Deterministic correction dispatcher.
    Returns: (new_source, applied_fix_message_or_None)
    """

    new_src, msg = repair_missing_rhs(source_text, error_line)

    if msg:
        return new_src, msg
    if not classification.fixable:
        return source_text, None

    reason = classification.reason

    if reason == "missing_semicolon":
        return _insert_semicolon_near_line(source_text, error_line)

    if reason == "missing_rbrace":
        return _append_missing_rbrace(source_text)

    if reason == "missing_lbrace":
        return _insert_missing_lbrace(source_text, error_line)

    if reason == "missing_lparen":
        new_src, msg = _fix_main_parentheses(source_text)
        if msg:
            return new_src, msg
        return _insert_missing_lparen(source_text, error_line)

    if reason == "missing_rparen":
        return _insert_missing_rparen(source_text, error_line)

    if reason == "extraneous_token":
        return _delete_extraneous_token_at(source_text, error_line, error_column)

    if reason == "main_lparen_expected":
        return _fix_main_parentheses(source_text)
    
    if reason == "missing_rhs":
        return _repair_missing_rhs(source_text, error_line)

    # New deterministic rescue for incomplete declarations like:
    #   int
    #   return 0;
    if reason == "mismatched_token":
        new_src, msg = _remove_dangling_type_line(source_text, error_line)
        if msg:
            return new_src, msg

    return source_text, None


# -----------------------------
# Semicolon insertion
# -----------------------------
_CONTROL_KEYWORDS = ("if", "while", "for", "switch")


def _looks_like_control_header(code: str) -> bool:
    s = code.strip()
    return any(s.startswith(k + " ") or s.startswith(k + "(") for k in _CONTROL_KEYWORDS)


def _strip_line_comment(s: str) -> str:
    return s.split("//", 1)[0].rstrip()


def _line_ends_like_complete_statement(code_part: str) -> bool:
    return code_part.rstrip().endswith((";", "{", "}", ":", ","))


def _insert_semicolon_near_line(source_text: str, error_line: int) -> Tuple[str, Optional[str]]:
    lines = source_text.splitlines(keepends=True)
    idx = error_line - 1
    if idx < 0 or idx >= len(lines):
        return source_text, None

    def prev_code_line(start: int) -> Optional[int]:
        j = start
        while j >= 0:
            s = lines[j].strip()
            if not s:
                j -= 1
                continue
            if s.startswith("#"):
                j -= 1
                continue
            return j
        return None

    target = idx

    cur = lines[target]
    cur_no_nl = cur.rstrip("\r\n")
    cur_code = _strip_line_comment(cur_no_nl)

    if cur_code.endswith("{") or _looks_like_control_header(cur_code):
        p = prev_code_line(target - 1)
        if p is not None:
            target = p
            return _insert_semicolon_at_line_index(lines, target)

    if _line_ends_like_complete_statement(cur_code):
        p = prev_code_line(target - 1)
        if p is not None:
            target = p

    return _insert_semicolon_at_line_index(lines, target)


def _insert_semicolon_at_line_index(lines: List[str], idx: int) -> Tuple[str, Optional[str]]:
    if idx < 0 or idx >= len(lines):
        return "".join(lines), None

    original = lines[idx]
    nl = "\n"
    if original.endswith("\r\n"):
        nl = "\r\n"
    elif original.endswith("\n"):
        nl = "\n"
    elif original.endswith("\r"):
        nl = "\r"
    else:
        nl = ""

    no_nl = original.rstrip("\r\n")

    stripped = no_nl.strip()
    if not stripped or stripped.startswith("#"):
        return "".join(lines), None

    code_part = _strip_line_comment(no_nl)

    if _line_ends_like_complete_statement(code_part):
        return "".join(lines), None

    if _looks_like_control_header(code_part):
        return "".join(lines), None

    if "//" in no_nl:
        code, sep, comment = no_nl.partition("//")
        updated = code.rstrip() + ";" + " " + sep + comment
    else:
        updated = no_nl.rstrip() + ";"

    lines[idx] = updated + nl
    return "".join(lines), "inserted missing ';'"


# -----------------------------
# Brace fixes
# -----------------------------
def _append_missing_rbrace(source_text: str) -> Tuple[str, Optional[str]]:
    stripped = source_text.rstrip()
    if stripped.endswith("}"):
        return source_text, None
    return stripped + "\n}", "inserted missing '}' at end"


def _insert_missing_lbrace(source_text: str, error_line: int) -> Tuple[str, Optional[str]]:
    lines = source_text.splitlines(keepends=True)
    idx = max(0, min(len(lines) - 1, error_line - 1))

    func_re = re.compile(r"^\s*(?:int|void|char|float|double)\s+[A-Za-z_]\w*\s*\([^;]*\)\s*$")

    candidates = [idx, idx - 1]
    for c in candidates:
        if c < 0 or c >= len(lines):
            continue
        line_no_nl = lines[c].rstrip("\r\n")
        code = _strip_line_comment(line_no_nl)
        if func_re.match(code):
            insert_at = c + 1
            j = insert_at
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].lstrip().startswith("{"):
                return source_text, None

            nl = "\n"
            if lines[c].endswith("\r\n"):
                nl = "\r\n"
            elif lines[c].endswith("\n"):
                nl = "\n"
            elif lines[c].endswith("\r"):
                nl = "\r"
            else:
                nl = "\n"

            lines.insert(insert_at, "{" + nl)
            return "".join(lines), "inserted missing '{' after function header"

    return source_text, None


# -----------------------------
# Parenthesis fixes
# -----------------------------
def _insert_missing_lparen(source_text: str, error_line: int) -> Tuple[str, Optional[str]]:
    lines = source_text.splitlines(keepends=True)
    idx = error_line - 1
    if idx < 0 or idx >= len(lines):
        return source_text, None

    line = lines[idx]
    line_no_nl = line.rstrip("\r\n")
    nl = line[len(line_no_nl):]

    m = re.search(r"\b(if|while|for)\s+([^\(].*\))", line_no_nl)
    if not m:
        return source_text, None

    kw = m.group(1)
    updated = re.sub(rf"\b{kw}\s+(.+)", rf"{kw} (\1", line_no_nl, count=1)
    lines[idx] = updated + nl
    return "".join(lines), f"inserted missing '(' after {kw}"


def _insert_missing_rparen(source_text: str, error_line: int) -> Tuple[str, Optional[str]]:
    lines = source_text.splitlines(keepends=True)
    idx = error_line - 1
    if idx < 0 or idx >= len(lines):
        return source_text, None

    line = lines[idx]
    line_no_nl = line.rstrip("\r\n")
    nl = line[len(line_no_nl):]

    if re.search(r"\b(if|while|for)\s*\(", line_no_nl) and "{" in line_no_nl and ")" not in line_no_nl:
        updated = line_no_nl.replace("{", ") {", 1)
        lines[idx] = updated + nl
        return "".join(lines), "inserted missing ')' before '{'"

    return source_text, None


# -----------------------------
# Extraneous token deletion
# -----------------------------
def _delete_extraneous_token_at(source_text: str, error_line: int, error_column: int) -> Tuple[str, Optional[str]]:
    lines = source_text.splitlines(keepends=True)
    idx = error_line - 1
    if idx < 0 or idx >= len(lines):
        return source_text, None

    line = lines[idx]
    line_no_nl = line.rstrip("\r\n")
    nl = line[len(line_no_nl):]

    col = max(0, min(len(line_no_nl), error_column))

    if col >= len(line_no_nl):
        return source_text, None

    ch = line_no_nl[col]
    if ch not in (";", ",", ")", "]"):
        if col > 0 and line_no_nl[col - 1] in (";", ",", ")", "]"):
            col = col - 1
            ch = line_no_nl[col]
        else:
            return source_text, None

    updated = line_no_nl[:col] + line_no_nl[col + 1:]
    lines[idx] = updated + nl
    return "".join(lines), f"deleted extraneous token '{ch}'"


# -----------------------------
# Special-case main() {
# -----------------------------
def _fix_main_parentheses(source_text: str) -> Tuple[str, Optional[str]]:
    pattern = re.compile(r"\bmain\s*\{")
    if not pattern.search(source_text):
        return source_text, None
    updated = pattern.sub("main() {", source_text, count=1)
    return updated, "replaced '{' with '() {' after main"


# -----------------------------
# New: dangling type-line removal
# -----------------------------
def _remove_dangling_type_line(source_text: str, error_line: int) -> Tuple[str, Optional[str]]:
    """
    Remove an incomplete declaration line containing only a type keyword, e.g.

        int
        return 0;

    This is conservative:
    - only removes a line that is exactly one type keyword
    - only when the next non-empty line starts with something statement-like
    """
    lines = source_text.splitlines(keepends=True)

    type_only_re = re.compile(r"^\s*(int|float|char|double|void)\s*(//.*)?$")
    next_stmt_re = re.compile(
        r"^\s*(return|if|while|for|break|continue|\{|\}|[A-Za-z_])\b"
    )

    # First try the line just before the reported error
    candidates = [error_line - 2, error_line - 1]

    for idx in candidates:
        if idx < 0 or idx >= len(lines):
            continue

        cur = lines[idx].rstrip("\r\n")
        if not type_only_re.match(cur):
            continue

        j = idx + 1
        while j < len(lines) and not lines[j].strip():
            j += 1

        if j >= len(lines):
            continue

        nxt = lines[j].rstrip("\r\n")
        if not next_stmt_re.match(nxt):
            continue

        new_lines = lines[:idx] + lines[idx + 1:]
        return "".join(new_lines), "removed dangling incomplete declaration"

    return source_text, None

def _repair_missing_rhs(source_text: str, error_line: int) -> Tuple[str, Optional[str]]:
    """
    Repair patterns like:
        x = ;
        int x = ;
    Conservative strategy:
    - If line looks like a declaration assignment, use 0 as initializer
    - If line looks like a normal assignment, use 0 as RHS
    """
    lines = source_text.splitlines(keepends=True)
    idx = error_line - 1
    if idx < 0 or idx >= len(lines):
        return source_text, None

    line = lines[idx]
    line_no_nl = line.rstrip("\r\n")
    nl = line[len(line_no_nl):]

    # declaration with missing initializer
    decl_pat = re.compile(r"^(\s*(?:int|float|char|double)\s+[A-Za-z_]\w*\s*=\s*);(\s*(?://.*)?)$")
    m = decl_pat.match(line_no_nl)
    if m:
        updated = m.group(1) + "0;" + m.group(2)
        lines[idx] = updated + nl
        return "".join(lines), "inserted default initializer '0' for missing RHS"

    # generic assignment with missing RHS
    assign_pat = re.compile(r"^(\s*[A-Za-z_]\w*\s*=\s*);(\s*(?://.*)?)$")
    m = assign_pat.match(line_no_nl)
    if m:
        updated = m.group(1) + "0;" + m.group(2)
        lines[idx] = updated + nl
        return "".join(lines), "inserted default RHS '0'"

    return source_text, None
def repair_missing_rhs(source: str, error_line: int) -> Tuple[str, Optional[str]]:
    """
    Fix patterns like:
        int x=;
        x=;
    """

    lines = source.splitlines(keepends=True)

    idx = error_line - 1
    if idx < 0 or idx >= len(lines):
        return source, None

    line = lines[idx]
    stripped = line.strip()

    # declaration initializer missing RHS
    m = re.match(r"(int|float|char|double)\s+[A-Za-z_]\w*\s*=\s*;", stripped)
    if m:
        fixed = stripped.replace("=;", "=0;")
        lines[idx] = line.replace(stripped, fixed)
        return "".join(lines), "inserted default initializer 0"

    # simple assignment missing RHS
    m = re.match(r"[A-Za-z_]\w*\s*=\s*;", stripped)
    if m:
        fixed = stripped.replace("=;", "=0;")
        lines[idx] = line.replace(stripped, fixed)
        return "".join(lines), "inserted default RHS 0"

    return source, None