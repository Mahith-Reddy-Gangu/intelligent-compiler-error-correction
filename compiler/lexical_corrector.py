from __future__ import annotations

import re
from typing import Optional, Tuple, List


# Keywords supported by your grammar/project.
# Keep this aligned with the grammar.
KEYWORDS = [
    "int",
    "return",
    "main",
    "if",
    "else",
    "while",
    "for",
    "break",
    "continue",
    "char",
    "float",
    "double",
    "void",
]

# Safe single-character normalizations that often appear from copy/paste.
CHAR_NORMALIZATIONS = {
    "“": '"',
    "”": '"',
    "‘": "'",
    "’": "'",
    "—": "-",
    "–": "-",
    "；": ";",
    "，": ",",
    "（": "(",
    "）": ")",
    "｛": "{",
    "｝": "}",
    "＝": "=",
    "＜": "<",
    "＞": ">",
}

# Safe token-level normalizations.
TOKEN_NORMALIZATIONS = {
    "=<=": "<=",
    "=>=": ">=",
    "=<": "<=",
    "=>": ">=",
    "==>": "=>",   # leave weird cases less destructive
}

IDENT_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")


def fix_common_lexical_issues(source_text: str) -> Tuple[str, List[str]]:
    """
    Fast, deterministic lexical cleanup.

    Returns:
        (new_source, list_of_applied_fixes)

    Scope:
    - character normalization
    - safe token normalization outside strings/comments
    - conservative keyword typo correction outside strings/comments
    """
    fixes: List[str] = []

    new_text, char_fixes = _normalize_characters(source_text)
    fixes.extend(char_fixes)

    new_text, token_fixes = _normalize_common_tokens(new_text)
    fixes.extend(token_fixes)

    new_text, keyword_fixes = _fix_keyword_typos(new_text)
    fixes.extend(keyword_fixes)

    return new_text, fixes


# ------------------------------------------------------------------
# Character normalization
# ------------------------------------------------------------------

def _normalize_characters(source_text: str) -> Tuple[str, List[str]]:
    fixes: List[str] = []
    out_chars: List[str] = []

    changed_pairs = set()

    for ch in source_text:
        if ch in CHAR_NORMALIZATIONS:
            repl = CHAR_NORMALIZATIONS[ch]
            out_chars.append(repl)
            changed_pairs.add((ch, repl))
        else:
            out_chars.append(ch)

    for old, new in sorted(changed_pairs):
        fixes.append(f"normalized character {repr(old)} -> {repr(new)}")

    return "".join(out_chars), fixes


# ------------------------------------------------------------------
# Token normalization outside strings/comments
# ------------------------------------------------------------------

def _normalize_common_tokens(source_text: str) -> Tuple[str, List[str]]:
    segments = _split_code_and_noncode(source_text)
    fixes: List[str] = []
    changed = False

    normalized_segments: List[str] = []

    for kind, chunk in segments:
        if kind != "code":
            normalized_segments.append(chunk)
            continue

        updated = chunk
        for bad, good in TOKEN_NORMALIZATIONS.items():
            if bad in updated:
                count = updated.count(bad)
                updated = updated.replace(bad, good)
                if count > 0:
                    fixes.append(f"normalized token {bad!r} -> {good!r} ({count}x)")
                    changed = True

        normalized_segments.append(updated)

    if not changed:
        return source_text, []

    return "".join(normalized_segments), fixes


# ------------------------------------------------------------------
# Conservative keyword typo correction
# ------------------------------------------------------------------

def _fix_keyword_typos(source_text: str) -> Tuple[str, List[str]]:
    """
    Only fix identifier-like words in code segments, and only if:
    - edit distance is exactly 1 from a known keyword, OR
    - a very common typo pattern is matched
    - and the token is not already a valid keyword
    """
    segments = _split_code_and_noncode(source_text)
    fixes: List[str] = []
    changed = False

    rebuilt: List[str] = []

    for kind, chunk in segments:
        if kind != "code":
            rebuilt.append(chunk)
            continue

        local_changes: List[Tuple[str, str]] = []

        def repl(match: re.Match[str]) -> str:
            nonlocal changed
            word = match.group(0)

            if word in KEYWORDS:
                return word

            replacement = _best_keyword_replacement(word)
            if replacement is None or replacement == word:
                return word

            local_changes.append((word, replacement))
            changed = True
            return replacement

        updated = IDENT_RE.sub(repl, chunk)
        rebuilt.append(updated)

        for old, new in local_changes:
            fixes.append(f"corrected keyword typo {old!r} -> {new!r}")

    if not changed:
        return source_text, []

    return "".join(rebuilt), fixes


def _best_keyword_replacement(word: str) -> Optional[str]:
    common_map = {
        "retrun": "return",
        "reutrn": "return",
        "retun": "return",
        "itre": "int",
        "innt": "int",
        "mian": "main",
        "whlie": "while",
        "fi": "if",
        "esle": "else",
        "fro": "for",
        "breka": "break",
        "contniue": "continue",
        "doulbe": "double",
        "flota": "float",
        "viod": "void",
    }

    if word in common_map:
        return common_map[word]

    candidates = [kw for kw in KEYWORDS if _edit_distance_leq_one(word, kw)]
    if len(candidates) == 1:
        return candidates[0]

    return None


def _edit_distance_leq_one(a: str, b: str) -> bool:
    """
    Fast check for Levenshtein distance <= 1.
    Conservative and enough for typo correction.
    """
    if a == b:
        return True

    la = len(a)
    lb = len(b)

    if abs(la - lb) > 1:
        return False

    # Same length: allow one substitution
    if la == lb:
        mismatches = sum(1 for x, y in zip(a, b) if x != y)
        return mismatches <= 1

    # Ensure a is shorter
    if la > lb:
        a, b = b, a
        la, lb = lb, la

    # Now lb == la + 1 : allow one insertion/deletion
    i = j = 0
    used = False

    while i < la and j < lb:
        if a[i] == b[j]:
            i += 1
            j += 1
        else:
            if used:
                return False
            used = True
            j += 1

    return True


# ------------------------------------------------------------------
# Code/non-code splitting
# ------------------------------------------------------------------

def _split_code_and_noncode(source_text: str) -> List[Tuple[str, str]]:
    """
    Splits source into tagged chunks:
      ("code", ...)
      ("noncode", ...)
    Non-code includes strings, char literals, // comments, /* */ comments.

    This is conservative and good enough for preprocessing.
    """
    result: List[Tuple[str, str]] = []
    i = 0
    n = len(source_text)

    code_buf: List[str] = []

    def flush_code() -> None:
        if code_buf:
            result.append(("code", "".join(code_buf)))
            code_buf.clear()

    while i < n:
        ch = source_text[i]

        # line comment
        if ch == "/" and i + 1 < n and source_text[i + 1] == "/":
            flush_code()
            j = i + 2
            while j < n and source_text[j] != "\n":
                j += 1
            result.append(("noncode", source_text[i:j]))
            i = j
            continue

        # block comment
        if ch == "/" and i + 1 < n and source_text[i + 1] == "*":
            flush_code()
            j = i + 2
            while j + 1 < n and not (source_text[j] == "*" and source_text[j + 1] == "/"):
                j += 1
            j = min(j + 2, n)
            result.append(("noncode", source_text[i:j]))
            i = j
            continue

        # string literal
        if ch == '"':
            flush_code()
            j = i + 1
            while j < n:
                if source_text[j] == "\\" and j + 1 < n:
                    j += 2
                    continue
                if source_text[j] == '"':
                    j += 1
                    break
                j += 1
            result.append(("noncode", source_text[i:j]))
            i = j
            continue

        # char literal
        if ch == "'":
            flush_code()
            j = i + 1
            while j < n:
                if source_text[j] == "\\" and j + 1 < n:
                    j += 2
                    continue
                if source_text[j] == "'":
                    j += 1
                    break
                j += 1
            result.append(("noncode", source_text[i:j]))
            i = j
            continue

        code_buf.append(ch)
        i += 1

    flush_code()
    return result