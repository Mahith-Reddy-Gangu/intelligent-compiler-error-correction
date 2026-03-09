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
    if not classification.fixable:
        return source_text, None

    reason = classification.reason

    if reason == "missing_semicolon":
        return _insert_semicolon_near_line(source_text, error_line)

    if reason == "missing_rbrace":
        return _append_missing_rbrace(source_text)

    if reason == "missing_lbrace":
        # best-effort: insert "{" after a function header line if it looks like one
        return _insert_missing_lbrace(source_text, error_line)

    if reason == "missing_lparen":
    # First try main() special-case: "main {" -> "main() {"
        new_src, msg = _fix_main_parentheses(source_text)
        if msg:
            return new_src, msg

    # Then try control headers like if/while/for
        return _insert_missing_lparen(source_text, error_line)

    if reason == "missing_rparen":
        return _insert_missing_rparen(source_text, error_line)

    if reason == "extraneous_token":
        return _delete_extraneous_token_at(source_text, error_line, error_column)

    # Legacy reason you had earlier (keep if classifier still emits it in some cases)
    if reason == "main_lparen_expected":
        return _fix_main_parentheses(source_text)

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
    # Things that usually should NOT get an extra semicolon added
    return code_part.rstrip().endswith((";", "{", "}", ":", ","))


def _insert_semicolon_near_line(source_text: str, error_line: int) -> Tuple[str, Optional[str]]:
    """
    Try to insert a semicolon on the most likely statement line.

    Key ANTLR behavior:
    - For a missing ';' after a declaration like "int x", ANTLR often reports the error
      at the NEXT token (e.g. the start of the next statement "x = 10;").
    So if the reported line already looks "complete" (ends with ';'), we should try the previous code line.

    Strategy:
    - Start from reported line.
    - If reported line is a block header/control header -> previous code line.
    - If reported line already ends with ';' (or other "complete" endings) -> previous code line.
    - Never touch preprocessor lines.
    """
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
            if s.startswith("#"):  # preprocessor
                j -= 1
                continue
            return j
        return None

    target = idx

    cur = lines[target]
    cur_no_nl = cur.rstrip("\r\n")
    cur_code = _strip_line_comment(cur_no_nl)

    # Case 1: current line is a block header or control header
    if cur_code.endswith("{") or _looks_like_control_header(cur_code):
        p = prev_code_line(target - 1)
        if p is not None:
            target = p
            return _insert_semicolon_at_line_index(lines, target)

    # Case 2: current line already looks complete (common when missing ';' is on PREVIOUS line)
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

    # Already ends with ; or { or } or : or , -> don't add
    if _line_ends_like_complete_statement(code_part):
        return "".join(lines), None

    # Avoid adding after control headers: if(...), while(...), for(...)
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
    """
    Best-effort:
    - If the error is around a function header line like: int main()
      and next line isn't '{', insert '{' after that header line.
    """
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
# Parenthesis fixes (very conservative)
# -----------------------------
def _insert_missing_lparen(source_text: str, error_line: int) -> Tuple[str, Optional[str]]:
    """
    Conservative: fix patterns like
      if x)   -> if (x)
      while x) -> while (x)
    """
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
    """
    Conservative: fix control headers missing closing ')', e.g.
      if (x {  -> if (x) {
    """
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
    """
    Delete a single character at the reported location (best-effort),
    but only if it looks like a common nuisance: extra ';' or ',' or ')'.
    """
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