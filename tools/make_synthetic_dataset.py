import os
import re
import json
import random
import argparse
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict
import sys


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

RNG_SEED = 2026

DEFAULT_SEEDS_DIR = os.path.join("data", "seed_programs")
DEFAULT_OUT = os.path.join("data", "patch_synth.jsonl")
DEFAULT_N = 80000


# -----------------------------
# Optional parser verification (ANTLR)
# -----------------------------
def _try_import_parser():
    try:
        from antlr4 import InputStream, CommonTokenStream
        from antlr4.error.ErrorListener import ErrorListener
        from generated.SimpleCLexer import SimpleCLexer
        from generated.SimpleCParser import SimpleCParser
        return InputStream, CommonTokenStream, ErrorListener, SimpleCLexer, SimpleCParser
    except Exception:
        return None


def _parse_errors_for_source(src: str, require_parser: bool) -> List[str]:
    pack = _try_import_parser()
    if pack is None:
        if require_parser:
            raise RuntimeError(
                "Parser/lexer not importable. If you passed --verify, you MUST have generated/ in PYTHONPATH.\n"
                "Fix: generate ANTLR files (SimpleCLexer/SimpleCParser) and run from project root."
            )
        return ["<no-parser-available>"]

    InputStream, CommonTokenStream, ErrorListener, SimpleCLexer, SimpleCParser = pack

    class CollectingErrorListener(ErrorListener):
        def __init__(self, stage: str):
            super().__init__()
            self.stage = stage
            self.errors: List[str] = []

        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            off = ""
            try:
                if offendingSymbol is not None and hasattr(offendingSymbol, "text") and offendingSymbol.text:
                    off = f" (offending: {offendingSymbol.text})"
            except Exception:
                off = ""
            self.errors.append(f"L{line}:{column} {self.stage}: {msg}{off}")

    input_stream = InputStream(src)
    lexer = SimpleCLexer(input_stream)

    lex_listener = CollectingErrorListener("LEX")
    lexer.removeErrorListeners()
    lexer.addErrorListener(lex_listener)

    tokens = CommonTokenStream(lexer)
    parser = SimpleCParser(tokens)

    parse_listener = CollectingErrorListener("PARSE")
    parser.removeErrorListeners()
    parser.addErrorListener(parse_listener)

    parser.program()

    return lex_listener.errors + parse_listener.errors


# -----------------------------
# Prompt window (same as your ai_error_corrector format)
# -----------------------------
def build_prompt_window(source_text: str, error_line: int, error_col: int, radius: int = 3) -> str:
    lines = source_text.splitlines()
    if not lines:
        return "repair:\n<CODE>\n<ERR>\n</CODE>"

    li = max(1, min(error_line, len(lines))) - 1
    start = max(0, li - radius)
    end = min(len(lines), li + radius + 1)

    window = lines[start:end]
    rel = li - start

    target = window[rel]
    col = max(0, min(error_col, len(target)))
    window[rel] = target[:col] + "<ERR>" + target[col:]

    return "repair:\n<CODE>\n" + "\n".join(window) + "\n</CODE>"


# -----------------------------
# Patch language (explicit)
# -----------------------------
_PATCH_INS_RE = re.compile(r"^INS\s+(\d+)\s+(.*)$", re.DOTALL)
_PATCH_DEL_RE = re.compile(r"^DEL\s+(\d+)\s+(\d+)\s*$")
_PATCH_REP_RE = re.compile(r"^REP\s+(\d+)\s+(\d+)\s+(.*)$", re.DOTALL)


def apply_explicit_patch(src: str, cmd: str) -> Optional[str]:
    cmd = cmd.strip()
    m = _PATCH_INS_RE.match(cmd)
    if m:
        idx = int(m.group(1))
        text = m.group(2)
        idx = max(0, min(idx, len(src)))
        return src[:idx] + text + src[idx:]

    m = _PATCH_DEL_RE.match(cmd)
    if m:
        a = int(m.group(1))
        b = int(m.group(2))
        a = max(0, min(a, len(src)))
        b = max(0, min(b, len(src)))
        if b < a:
            a, b = b, a
        return src[:a] + src[b:]

    m = _PATCH_REP_RE.match(cmd)
    if m:
        a = int(m.group(1))
        b = int(m.group(2))
        text = m.group(3)
        a = max(0, min(a, len(src)))
        b = max(0, min(b, len(src)))
        if b < a:
            a, b = b, a
        return src[:a] + text + src[b:]

    return None


# -----------------------------
# Utilities: line/col <-> absolute index
# -----------------------------
def _split_lines_keepends(src: str) -> List[str]:
    return src.splitlines(keepends=True)


def _join_lines(lines: List[str]) -> str:
    return "".join(lines)


def _line_col_to_index(src: str, line: int, col: int) -> int:
    lines = _split_lines_keepends(src)
    if not lines:
        return 0
    li = max(1, min(line, len(lines))) - 1
    before = "".join(lines[:li])
    line_text = lines[li].rstrip("\r\n")
    c = max(0, min(col, len(line_text)))
    return len(before) + c


def _index_to_line_col(src: str, idx: int) -> Tuple[int, int]:
    if idx < 0:
        return 1, 0
    if idx > len(src):
        idx = len(src)

    lines = _split_lines_keepends(src)
    if not lines:
        return 1, 0

    total = 0
    for i, ln in enumerate(lines):
        ln_no_nl = ln.rstrip("\r\n")
        ln_len = len(ln_no_nl)
        if total + ln_len >= idx:
            return i + 1, idx - total
        total += len(ln)
    last_no = lines[-1].rstrip("\r\n")
    return len(lines), len(last_no)


def _apply_delete_char_at(src: str, line: int, col: int) -> str:
    lines = _split_lines_keepends(src)
    if not lines:
        return src
    li = max(1, min(line, len(lines))) - 1
    original = lines[li]
    line_no_nl = original.rstrip("\r\n")
    nl = original[len(line_no_nl):]
    c = max(0, min(col, len(line_no_nl)))
    if c >= len(line_no_nl):
        return src
    new_line = line_no_nl[:c] + line_no_nl[c + 1:]
    lines[li] = new_line + nl
    return _join_lines(lines)


def _apply_insert_text_at(src: str, line: int, col: int, text: str) -> str:
    lines = _split_lines_keepends(src)
    if not lines:
        return src
    li = max(1, min(line, len(lines))) - 1
    original = lines[li]
    line_no_nl = original.rstrip("\r\n")
    nl = original[len(line_no_nl):]
    c = max(0, min(col, len(line_no_nl)))
    new_line = line_no_nl[:c] + text + line_no_nl[c:]
    lines[li] = new_line + nl
    return _join_lines(lines)


def _all_seed_files(seeds_dir: str) -> List[str]:
    out = []
    if not os.path.isdir(seeds_dir):
        return out
    for fn in os.listdir(seeds_dir):
        if fn.endswith(".c"):
            out.append(os.path.join(seeds_dir, fn))
    out.sort()
    return out


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# -----------------------------
# Corruption definition
# -----------------------------
@dataclass(frozen=True)
class Corruption:
    family: str
    split_hint: str  # v1 = single-step fully fixes, v2 = hard improves only
    error_line: int
    error_col: int
    corrupted_src: str
    target_cmd: str  # explicit: INS idx text | DEL a b | REP a b text


# -----------------------------
# Candidate finders
# -----------------------------
def _lines_no_keep(src: str) -> List[str]:
    return src.splitlines(keepends=False)


def _find_statement_semicolons(seed_src: str) -> List[Tuple[int, int]]:
    lines = _lines_no_keep(seed_src)
    out = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s:
            continue
        if re.search(r"\bfor\s*\(", ln):
            continue
        if s.endswith(";"):
            col = len(ln.rstrip()) - 1
            out.append((i + 1, col))
    return out


def _find_return_break_continue_semicolons(seed_src: str) -> List[Tuple[int, int, str]]:
    # Return: list of (line, col, kind) where col is position of trailing ';'
    lines = _lines_no_keep(seed_src)
    out: List[Tuple[int, int, str]] = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s:
            continue
        m = re.match(r"^(return|break|continue)\b", s)
        if not m:
            continue
        if s.endswith(";"):
            col = len(ln.rstrip()) - 1
            out.append((i + 1, col, m.group(1)))
    return out


def _find_chars(seed_src: str, ch: str) -> List[Tuple[int, int]]:
    lines = _lines_no_keep(seed_src)
    out = []
    for i, ln in enumerate(lines):
        idx = ln.find(ch)
        while idx != -1:
            out.append((i + 1, idx))
            idx = ln.find(ch, idx + 1)
    return out


def _find_calls_lparen_sites(seed_src: str) -> List[Tuple[int, int]]:
    # Find patterns like: IDENTIFIER '(' ... ')' but avoid control keywords.
    lines = _lines_no_keep(seed_src)
    out: List[Tuple[int, int]] = []
    for i, ln in enumerate(lines):
        # skip obvious control headers
        if re.search(r"\b(if|while|for)\s*\(", ln):
            continue
        for m in re.finditer(r"\b([A-Za-z_]\w*)\s*\(", ln):
            name = m.group(1)
            if name in ("if", "while", "for", "return", "break", "continue"):
                continue
            # position of '('
            lparen_pos = ln.find("(", m.start())
            if lparen_pos != -1:
                out.append((i + 1, lparen_pos))
    return out


def _find_grouping_lparen_sites(seed_src: str) -> List[Tuple[int, int]]:
    # Grouping parentheses, not function calls, not control headers.
    lines = _lines_no_keep(seed_src)
    out: List[Tuple[int, int]] = []
    for i, ln in enumerate(lines):
        if re.search(r"\b(if|while|for)\s*\(", ln):
            continue
        # grouping often looks like: ( expr )
        for m in re.finditer(r"\(\s*[A-Za-z_0-9]", ln):
            out.append((i + 1, m.start()))
    return out


def _find_calls_with_commas(seed_src: str) -> List[Tuple[int, int]]:
    lines = _lines_no_keep(seed_src)
    out = []
    for i, ln in enumerate(lines):
        if "(" in ln and ")" in ln and "," in ln:
            out.append((i + 1, ln.find(",")))
    return out


def _find_paramlist_commas(seed_src: str) -> List[Tuple[int, int]]:
    lines = _lines_no_keep(seed_src)
    out = []
    for i, ln in enumerate(lines):
        if "(" in ln and ")" in ln and "," in ln and re.search(r"\b(int|float|char|void)\b", ln):
            out.append((i + 1, ln.find(",")))
    return out


def _find_decl_commas(seed_src: str) -> List[Tuple[int, int]]:
    lines = _lines_no_keep(seed_src)
    out = []
    for i, ln in enumerate(lines):
        if "," in ln and ";" in ln and re.search(r"\b(int|float|char|void)\b", ln):
            out.append((i + 1, ln.find(",")))
    return out


def _find_ternary_colon(seed_src: str) -> List[Tuple[int, int]]:
    lines = _lines_no_keep(seed_src)
    out = []
    for i, ln in enumerate(lines):
        if "?" in ln and ":" in ln:
            out.append((i + 1, ln.find(":")))
    return out


def _find_array_brackets(seed_src: str) -> List[Tuple[int, int, str]]:
    lines = _lines_no_keep(seed_src)
    out: List[Tuple[int, int, str]] = []
    for i, ln in enumerate(lines):
        for ch in ["[", "]"]:
            idx = ln.find(ch)
            while idx != -1:
                out.append((i + 1, idx, ch))
                idx = ln.find(ch, idx + 1)
    return out


def _find_keyword_occurrences(seed_src: str) -> List[Tuple[int, int, str]]:
    kws = ["return", "if", "else", "while", "for", "break", "continue", "int", "float", "char", "void"]
    lines = _lines_no_keep(seed_src)
    out = []
    for i, ln in enumerate(lines):
        for kw in kws:
            m = re.search(rf"\b{re.escape(kw)}\b", ln)
            if m:
                out.append((i + 1, m.start(), kw))
    return out


def _find_float_literals(seed_src: str) -> List[Tuple[int, int, int]]:
    # returns (line, start_col, end_col_exclusive)
    lines = _lines_no_keep(seed_src)
    out: List[Tuple[int, int, int]] = []
    for i, ln in enumerate(lines):
        for m in re.finditer(r"\b\d+\.\d+\b", ln):
            out.append((i + 1, m.start(), m.end()))
    return out


def _find_char_literals(seed_src: str) -> List[Tuple[int, int, int]]:
    # crude char literal: 'a' or '\n' etc on same line
    lines = _lines_no_keep(seed_src)
    out: List[Tuple[int, int, int]] = []
    for i, ln in enumerate(lines):
        for m in re.finditer(r"\'(?:[^\'\\]|\\[nrt\'\\])\'", ln):
            out.append((i + 1, m.start(), m.end()))
    return out


def _find_inc_tokens(seed_src: str) -> List[Tuple[int, int]]:
    lines = _lines_no_keep(seed_src)
    out: List[Tuple[int, int]] = []
    for i, ln in enumerate(lines):
        idx = ln.find("++")
        while idx != -1:
            out.append((i + 1, idx))
            idx = ln.find("++", idx + 2)
    return out


def _find_compound_assign_tokens(seed_src: str) -> List[Tuple[int, int, str]]:
    toks = ["+=", "-=", "*=", "/=", "%="]
    lines = _lines_no_keep(seed_src)
    out: List[Tuple[int, int, str]] = []
    for i, ln in enumerate(lines):
        for t in toks:
            idx = ln.find(t)
            while idx != -1:
                out.append((i + 1, idx, t))
                idx = ln.find(t, idx + 2)
    return out


def _find_eqeq_tokens(seed_src: str) -> List[Tuple[int, int]]:
    lines = _lines_no_keep(seed_src)
    out: List[Tuple[int, int]] = []
    for i, ln in enumerate(lines):
        idx = ln.find("==")
        while idx != -1:
            out.append((i + 1, idx))
            idx = ln.find("==", idx + 2)
    return out


def _find_single_assign_sites(seed_src: str) -> List[Tuple[int, int]]:
    # Find '=' that are not part of '==', '!=', '<=', '>=' and not in compound assigns.
    lines = _lines_no_keep(seed_src)
    out: List[Tuple[int, int]] = []
    for i, ln in enumerate(lines):
        for m in re.finditer(r"=", ln):
            j = m.start()
            prev = ln[j - 1] if j - 1 >= 0 else ""
            nxt = ln[j + 1] if j + 1 < len(ln) else ""
            pair = prev + nxt
            if nxt == "=":
                continue
            if prev in ("!", "<", ">", "+", "-", "*", "/", "%"):
                # != <= >= += -= *= /= %=
                continue
            # heuristically avoid for-header semicolons locations; fine
            out.append((i + 1, j))
    return out


# -----------------------------
# Corruption builders
# -----------------------------
def _make_missing_semicolon(seed_src: str) -> Optional[Corruption]:
    cands = _find_statement_semicolons(seed_src)
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} ;"
    return Corruption("missing_semicolon", "v1", line, col, corrupted, target)


def _make_missing_semicolon_after_keyword(seed_src: str) -> Optional[Corruption]:
    cands = _find_return_break_continue_semicolons(seed_src)
    if not cands:
        return None
    line, col, kind = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} ;"
    return Corruption(f"missing_semicolon_after_{kind}", "v1", line, col, corrupted, target)


def _make_extra_semicolon(seed_src: str) -> Optional[Corruption]:
    cands = _find_statement_semicolons(seed_src)
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_insert_text_at(seed_src, line, col, ";")
    del_start = _line_col_to_index(corrupted, line, col)
    del_end = del_start + 1
    target = f"DEL {del_start} {del_end}"
    return Corruption("extra_semicolon", "v1", line, col, corrupted, target)


def _make_missing_rbrace(seed_src: str) -> Optional[Corruption]:
    cands = _find_chars(seed_src, "}")
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} }}"
    return Corruption("missing_rbrace", "v1", line, col, corrupted, target)


def _make_missing_lbrace(seed_src: str) -> Optional[Corruption]:
    # Robust: pick any '{' and delete it.
    cands = _find_chars(seed_src, "{")
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} {{"
    return Corruption("missing_lbrace", "v1", line, col, corrupted, target)


def _make_missing_rparen(seed_src: str) -> Optional[Corruption]:
    cands = _find_chars(seed_src, ")")
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} )"
    return Corruption("missing_rparen", "v1", line, col, corrupted, target)


def _make_missing_lparen_control(seed_src: str) -> Optional[Corruption]:
    lines = _lines_no_keep(seed_src)
    cands = []
    for i, ln in enumerate(lines):
        m = re.search(r"\b(if|while|for)\s*\(", ln)
        if m:
            cands.append((i + 1, ln.find("(")))
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} ("
    return Corruption("missing_lparen_control", "v1", line, col, corrupted, target)


def _make_missing_lparen_general(seed_src: str) -> Optional[Corruption]:
    # Function calls
    cands = _find_calls_lparen_sites(seed_src)
    # Grouping parentheses
    cands2 = _find_grouping_lparen_sites(seed_src)
    cands_all = cands + cands2
    if not cands_all:
        return None
    line, col = random.choice(cands_all)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} ("
    return Corruption("missing_lparen_general", "v1", line, col, corrupted, target)


def _make_for_missing_first_semicolon(seed_src: str) -> Optional[Corruption]:
    lines = _lines_no_keep(seed_src)
    cands = []
    for i, ln in enumerate(lines):
        if re.search(r"\bfor\s*\(", ln) and ";" in ln:
            cands.append((i + 1, ln.find(";")))
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} ;"
    return Corruption("for_missing_first_semicolon", "v1", line, col, corrupted, target)


def _make_for_missing_second_semicolon(seed_src: str) -> Optional[Corruption]:
    lines = _lines_no_keep(seed_src)
    cands = []
    for i, ln in enumerate(lines):
        if re.search(r"\bfor\s*\(", ln):
            semi_positions = [m.start() for m in re.finditer(";", ln)]
            if len(semi_positions) >= 2:
                cands.append((i + 1, semi_positions[1]))
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} ;"
    return Corruption("for_missing_second_semicolon", "v1", line, col, corrupted, target)


def _make_for_missing_both_semicolons(seed_src: str) -> Optional[Corruption]:
    lines = _lines_no_keep(seed_src)
    cands = []
    for i, ln in enumerate(lines):
        if re.search(r"\bfor\s*\(", ln):
            semi_positions = [m.start() for m in re.finditer(";", ln)]
            if len(semi_positions) >= 2:
                cands.append((i + 1, semi_positions[0], semi_positions[1]))
    if not cands:
        return None
    line, c1, c2 = random.choice(cands)
    tmp = _apply_delete_char_at(seed_src, line, c2)
    corrupted = _apply_delete_char_at(tmp, line, c1)
    ins_idx = _line_col_to_index(seed_src, line, c1)
    target = f"INS {ins_idx} ;"
    return Corruption("for_missing_both_semicolons", "v2", line, c1, corrupted, target)


def _make_missing_rbrack(seed_src: str) -> Optional[Corruption]:
    cands = [(l, c, k) for (l, c, k) in _find_array_brackets(seed_src) if k == "]"]
    if not cands:
        return None
    line, col, _ = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} ]"
    return Corruption("missing_rbrack", "v1", line, col, corrupted, target)


def _make_missing_lbrack(seed_src: str) -> Optional[Corruption]:
    cands = [(l, c, k) for (l, c, k) in _find_array_brackets(seed_src) if k == "["]
    if not cands:
        return None
    line, col, _ = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} ["
    return Corruption("missing_lbrack", "v1", line, col, corrupted, target)


def _make_extra_rbrack(seed_src: str) -> Optional[Corruption]:
    cands = _find_chars(seed_src, "]")
    if not cands:
        return None
    line, col = random.choice(cands)
    # insert extra ']' right after an existing ']'
    corrupted = _apply_insert_text_at(seed_src, line, col + 1, "]")
    del_start = _line_col_to_index(corrupted, line, col + 1)
    target = f"DEL {del_start} {del_start + 1}"
    return Corruption("extra_rbrack", "v1", line, col + 1, corrupted, target)


def _make_extra_rparen(seed_src: str) -> Optional[Corruption]:
    cands = _find_chars(seed_src, ")")
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_insert_text_at(seed_src, line, col + 1, ")")
    del_start = _line_col_to_index(corrupted, line, col + 1)
    target = f"DEL {del_start} {del_start + 1}"
    return Corruption("extra_rparen", "v1", line, col + 1, corrupted, target)


def _make_extra_rbrace(seed_src: str) -> Optional[Corruption]:
    cands = _find_chars(seed_src, "}")
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_insert_text_at(seed_src, line, col + 1, "}")
    del_start = _line_col_to_index(corrupted, line, col + 1)
    target = f"DEL {del_start} {del_start + 1}"
    return Corruption("extra_rbrace", "v1", line, col + 1, corrupted, target)


def _make_missing_comma_args(seed_src: str) -> Optional[Corruption]:
    cands = _find_calls_with_commas(seed_src)
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} ,"
    return Corruption("missing_comma_args", "v1", line, col, corrupted, target)


def _make_missing_comma_params(seed_src: str) -> Optional[Corruption]:
    cands = _find_paramlist_commas(seed_src)
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} ,"
    return Corruption("missing_comma_params", "v1", line, col, corrupted, target)


def _make_missing_comma_decl(seed_src: str) -> Optional[Corruption]:
    cands = _find_decl_commas(seed_src)
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} ,"
    return Corruption("missing_comma_decl", "v1", line, col, corrupted, target)


def _make_ternary_missing_colon(seed_src: str) -> Optional[Corruption]:
    cands = _find_ternary_colon(seed_src)
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_delete_char_at(seed_src, line, col)
    ins_idx = _line_col_to_index(seed_src, line, col)
    target = f"INS {ins_idx} :"
    return Corruption("ternary_missing_colon", "v1", line, col, corrupted, target)


def _make_ternary_extra_colon(seed_src: str) -> Optional[Corruption]:
    cands = _find_ternary_colon(seed_src)
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_insert_text_at(seed_src, line, col + 1, ":")
    del_start = _line_col_to_index(corrupted, line, col + 1)
    target = f"DEL {del_start} {del_start + 1}"
    return Corruption("ternary_extra_colon", "v1", line, col + 1, corrupted, target)


def _make_mismatched_rparen_to_rbrack(seed_src: str) -> Optional[Corruption]:
    cands = _find_chars(seed_src, ")")
    if not cands:
        return None
    line, col = random.choice(cands)
    abs_start = _line_col_to_index(seed_src, line, col)
    abs_end = abs_start + 1
    corrupted = apply_explicit_patch(seed_src, f"REP {abs_start} {abs_end} ]")
    if corrupted is None or corrupted == seed_src:
        return None
    target = f"REP {abs_start} {abs_end} )"
    return Corruption("mismatch_rparen_to_rbrack", "v1", line, col, corrupted, target)


def _make_mismatched_rbrack_to_rparen(seed_src: str) -> Optional[Corruption]:
    cands = _find_chars(seed_src, "]")
    if not cands:
        return None
    line, col = random.choice(cands)
    abs_start = _line_col_to_index(seed_src, line, col)
    abs_end = abs_start + 1
    corrupted = apply_explicit_patch(seed_src, f"REP {abs_start} {abs_end} )")
    if corrupted is None or corrupted == seed_src:
        return None
    target = f"REP {abs_start} {abs_end} ]"
    return Corruption("mismatch_rbrack_to_rparen", "v1", line, col, corrupted, target)


def _make_mismatch_lbrack_to_lparen(seed_src: str) -> Optional[Corruption]:
    cands = _find_chars(seed_src, "[")
    if not cands:
        return None
    line, col = random.choice(cands)
    abs_start = _line_col_to_index(seed_src, line, col)
    abs_end = abs_start + 1
    corrupted = apply_explicit_patch(seed_src, f"REP {abs_start} {abs_end} (")
    if corrupted is None or corrupted == seed_src:
        return None
    target = f"REP {abs_start} {abs_end} ["
    return Corruption("mismatch_lbrack_to_lparen", "v1", line, col, corrupted, target)


def _make_mismatch_lparen_to_lbrack(seed_src: str) -> Optional[Corruption]:
    cands = _find_chars(seed_src, "(")
    # avoid control headers to diversify; still ok if some slip
    if not cands:
        return None
    line, col = random.choice(cands)
    abs_start = _line_col_to_index(seed_src, line, col)
    abs_end = abs_start + 1
    corrupted = apply_explicit_patch(seed_src, f"REP {abs_start} {abs_end} [")
    if corrupted is None or corrupted == seed_src:
        return None
    target = f"REP {abs_start} {abs_end} ("
    return Corruption("mismatch_lparen_to_lbrack", "v1", line, col, corrupted, target)


def _make_illegal_char_injection(seed_src: str) -> Optional[Corruption]:
    lines = _lines_no_keep(seed_src)
    cands = [i for i, ln in enumerate(lines) if ln.strip()]
    if not cands:
        return None
    i = random.choice(cands)
    ln = lines[i]
    col = min(len(ln), max(0, len(ln) // 2))
    corrupted = _apply_insert_text_at(seed_src, i + 1, col, "@")
    abs_idx = _line_col_to_index(corrupted, i + 1, col)
    target = f"DEL {abs_idx} {abs_idx + 1}"
    return Corruption("illegal_char", "v1", i + 1, col, corrupted, target)


def _make_break_and_or(seed_src: str) -> Optional[Corruption]:
    lines = _lines_no_keep(seed_src)
    cands = []
    for i, ln in enumerate(lines):
        if "&&" in ln:
            cands.append((i + 1, ln.find("&&"), "&&", "&"))
        if "||" in ln:
            cands.append((i + 1, ln.find("||"), "||", "|"))
    if not cands:
        return None
    line, col, old, new = random.choice(cands)
    abs_start = _line_col_to_index(seed_src, line, col)
    abs_end = abs_start + len(old)
    corrupted = apply_explicit_patch(seed_src, f"REP {abs_start} {abs_end} {new}")
    if corrupted is None or corrupted == seed_src:
        return None
    # In corrupted, new has len 1
    target = f"REP {abs_start} {abs_start + len(new)} {old}"
    return Corruption("broken_logical_op", "v1", line, col, corrupted, target)


def _make_keyword_typo(seed_src: str) -> Optional[Corruption]:
    cands = _find_keyword_occurrences(seed_src)
    if not cands:
        return None
    line, col, kw = random.choice(cands)
    typo_map = {
        "return": "retrun",
        "while": "whlie",
        "continue": "contnue",
        "break": "breaak",
        "for": "fro",
        "else": "esle",
        "if": "fi",
        "int": "itn",
        "float": "floaat",
        "char": "chra",
        "void": "vodi",
    }
    typo = typo_map.get(kw)
    if not typo:
        return None
    abs_start = _line_col_to_index(seed_src, line, col)
    abs_end = abs_start + len(kw)
    corrupted = apply_explicit_patch(seed_src, f"REP {abs_start} {abs_end} {typo}")
    if corrupted is None or corrupted == seed_src:
        return None
    target = f"REP {abs_start} {abs_start + len(typo)} {kw}"
    return Corruption("keyword_typo", "v1", line, col, corrupted, target)


def _make_missing_operand_after_operator(seed_src: str) -> Optional[Corruption]:
    lines = _lines_no_keep(seed_src)
    cands = []
    for i, ln in enumerate(lines):
        m = re.search(r"\b([A-Za-z_]\w*|\d+)\s*(\+|\-|\*|/|%|==|!=|<=|>=|<|>|&&|\|\|)\s*([A-Za-z_]\w*|\d+)\b", ln)
        if m:
            rhs_start = m.start(3)
            rhs_end = m.end(3)
            cands.append((i + 1, rhs_start, rhs_end))
    if not cands:
        return None
    line, rhs_s, rhs_e = random.choice(cands)
    abs_s = _line_col_to_index(seed_src, line, rhs_s)
    abs_e = _line_col_to_index(seed_src, line, rhs_e)
    corrupted = apply_explicit_patch(seed_src, f"DEL {abs_s} {abs_e}")
    if corrupted is None or corrupted == seed_src:
        return None
    target = f"INS {abs_s} 0"
    return Corruption("missing_operand", "v1", line, rhs_s, corrupted, target)


def _make_extra_operator(seed_src: str) -> Optional[Corruption]:
    lines = _lines_no_keep(seed_src)
    cands = []
    for i, ln in enumerate(lines):
        m = re.search(r"\b([A-Za-z_]\w*|\d+)\s*(\+|\-|\*|/|%|==|!=|<=|>=|<|>|&&|\|\|)\s*([A-Za-z_]\w*|\d+)\b", ln)
        if m:
            op_end = m.end(2)
            cands.append((i + 1, op_end))
    if not cands:
        return None
    line, col = random.choice(cands)
    corrupted = _apply_insert_text_at(seed_src, line, col, " *")
    abs_ins = _line_col_to_index(corrupted, line, col)
    target = f"DEL {abs_ins} {abs_ins + 2}"
    return Corruption("extra_operator", "v1", line, col, corrupted, target)


def _make_inc_split(seed_src: str) -> Optional[Corruption]:
    # "x++" -> "x+ +"
    cands = _find_inc_tokens(seed_src)
    if not cands:
        return None
    line, col = random.choice(cands)
    abs_start = _line_col_to_index(seed_src, line, col)
    abs_end = abs_start + 2  # "++"
    corrupted = apply_explicit_patch(seed_src, f"REP {abs_start} {abs_end} + +")
    if corrupted is None or corrupted == seed_src:
        return None
    # In corrupted, replacement is length 3
    target = f"REP {abs_start} {abs_start + 3} ++"
    return Corruption("inc_split", "v1", line, col, corrupted, target)


def _make_compound_assign_split(seed_src: str) -> Optional[Corruption]:
    # "+=" -> "+ ="
    cands = _find_compound_assign_tokens(seed_src)
    if not cands:
        return None
    line, col, tok = random.choice(cands)
    abs_start = _line_col_to_index(seed_src, line, col)
    abs_end = abs_start + 2  # tok length
    split = tok[0] + " ="  # "+ ="
    corrupted = apply_explicit_patch(seed_src, f"REP {abs_start} {abs_end} {split}")
    if corrupted is None or corrupted == seed_src:
        return None
    # split length is 3
    target = f"REP {abs_start} {abs_start + len(split)} {tok}"
    return Corruption("compound_assign_split", "v1", line, col, corrupted, target)


def _make_assign_vs_eqeq(seed_src: str) -> Optional[Corruption]:
    # Two directions:
    #  - "=" -> "=="
    #  - "==" -> "="
    # Both are common mistakes.
    choose_dir = random.random()
    if choose_dir < 0.5:
        cands = _find_single_assign_sites(seed_src)
        if not cands:
            return None
        line, col = random.choice(cands)
        abs_start = _line_col_to_index(seed_src, line, col)
        abs_end = abs_start + 1
        corrupted = apply_explicit_patch(seed_src, f"REP {abs_start} {abs_end} ==")
        if corrupted is None or corrupted == seed_src:
            return None
        target = f"REP {abs_start} {abs_start + 2} ="
        return Corruption("assign_to_eqeq", "v1", line, col, corrupted, target)
    else:
        cands = _find_eqeq_tokens(seed_src)
        if not cands:
            return None
        line, col = random.choice(cands)
        abs_start = _line_col_to_index(seed_src, line, col)
        abs_end = abs_start + 2
        corrupted = apply_explicit_patch(seed_src, f"REP {abs_start} {abs_end} =")
        if corrupted is None or corrupted == seed_src:
            return None
        target = f"REP {abs_start} {abs_start + 1} =="
        return Corruption("eqeq_to_assign", "v1", line, col, corrupted, target)


def _make_broken_float_literal(seed_src: str) -> Optional[Corruption]:
    # Make "12.34" -> "12..34" (inject one extra dot), oracle removes extra dot
    cands = _find_float_literals(seed_src)
    if not cands:
        return None
    line, s_col, e_col = random.choice(cands)
    # find the '.' inside that literal
    ln = _lines_no_keep(seed_src)[line - 1]
    dot_pos = ln.find(".", s_col, e_col)
    if dot_pos == -1:
        return None

    # insert an extra '.' right after the existing '.'
    corrupted = _apply_insert_text_at(seed_src, line, dot_pos + 1, ".")
    abs_del = _line_col_to_index(corrupted, line, dot_pos + 1)
    target = f"DEL {abs_del} {abs_del + 1}"
    return Corruption("broken_float_literal", "v1", line, dot_pos + 1, corrupted, target)


def _make_broken_char_literal(seed_src: str) -> Optional[Corruption]:
    # "'a'" -> "'a" (delete closing quote), oracle inserts quote back
    cands = _find_char_literals(seed_src)
    if not cands:
        return None
    line, s_col, e_col = random.choice(cands)
    # closing quote is at e_col-1
    closing_col = e_col - 1
    corrupted = _apply_delete_char_at(seed_src, line, closing_col)
    ins_idx = _line_col_to_index(seed_src, line, closing_col)
    target = f"INS {ins_idx} '"
    return Corruption("broken_char_literal", "v1", line, closing_col, corrupted, target)


CORRUPTION_BUILDERS = [
    # Semicolons
    _make_missing_semicolon,
    _make_missing_semicolon_after_keyword,
    _make_extra_semicolon,

    # Braces / parens
    _make_missing_rbrace,
    _make_missing_lbrace,
    _make_missing_rparen,
    _make_missing_lparen_control,
    _make_missing_lparen_general,
    _make_extra_rparen,
    _make_extra_rbrace,

    # for header
    _make_for_missing_first_semicolon,
    _make_for_missing_second_semicolon,
    _make_for_missing_both_semicolons,  # v2 hard

    # brackets
    _make_missing_rbrack,
    _make_missing_lbrack,
    _make_extra_rbrack,

    # commas
    _make_missing_comma_args,
    _make_missing_comma_params,
    _make_missing_comma_decl,

    # ternary
    _make_ternary_missing_colon,
    _make_ternary_extra_colon,

    # mismatches
    _make_mismatched_rparen_to_rbrack,
    _make_mismatched_rbrack_to_rparen,
    _make_mismatch_lbrack_to_lparen,
    _make_mismatch_lparen_to_lbrack,

    # lexer-ish
    _make_illegal_char_injection,
    _make_break_and_or,

    # keywords/types typos
    _make_keyword_typo,

    # expression issues
    _make_missing_operand_after_operator,
    _make_extra_operator,

    # operator split confusions
    _make_inc_split,
    _make_compound_assign_split,
    _make_assign_vs_eqeq,

    # literal corruptions
    _make_broken_float_literal,
    _make_broken_char_literal,
]


# -----------------------------
# Verification gate
# -----------------------------
def _passes_gate(seed_src: str, corr: Corruption, verify: bool) -> bool:
    if not verify:
        return True

    errs_before = _parse_errors_for_source(corr.corrupted_src, require_parser=True)
    if errs_before == ["<no-parser-available>"]:
        return False
    if len(errs_before) == 0:
        return False

    fixed_src = apply_explicit_patch(corr.corrupted_src, corr.target_cmd)
    if fixed_src is None:
        return False

    errs_after = _parse_errors_for_source(fixed_src, require_parser=True)
    if errs_after == ["<no-parser-available>"]:
        return False

    if corr.split_hint == "v1":
        return len(errs_after) == 0

    return len(errs_after) < len(errs_before)


# -----------------------------
# Emit JSONL example
# -----------------------------
def _to_example(corr: Corruption, radius: int) -> Dict:
    prompt = build_prompt_window(corr.corrupted_src, corr.error_line, corr.error_col, radius=radius)
    return {
        "task": "patch_repair",
        "split_hint": corr.split_hint,
        "family": corr.family,
        "error_line": corr.error_line,
        "error_col": corr.error_col,
        "input": prompt,
        "target": corr.target_cmd,
    }


# -----------------------------
# Main
# -----------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds_dir", type=str, default=DEFAULT_SEEDS_DIR)
    ap.add_argument("--out", type=str, default=DEFAULT_OUT)
    ap.add_argument("-n", type=int, default=DEFAULT_N)
    ap.add_argument("--radius", type=int, default=3)
    ap.add_argument("--verify", action="store_true", help="Require ANTLR parse-based quality gate")
    ap.add_argument("--max_attempts", type=int, default=600000, help="Max attempts to produce n passing examples")
    args = ap.parse_args()

    random.seed(RNG_SEED)

    seed_files = _all_seed_files(args.seeds_dir)
    if not seed_files:
        raise RuntimeError(f"No .c seed files found in: {args.seeds_dir}")

    if args.verify:
        _ = _parse_errors_for_source("int main(){return 0;}", require_parser=True)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    written = 0
    attempts = 0

    with open(args.out, "w", encoding="utf-8") as w:
        while written < args.n and attempts < args.max_attempts:
            attempts += 1

            seed_path = random.choice(seed_files)
            seed_src = _read_text(seed_path)

            builder = random.choice(CORRUPTION_BUILDERS)
            corr = builder(seed_src)
            if corr is None:
                continue
            if corr.corrupted_src == seed_src:
                continue

            if not _passes_gate(seed_src, corr, verify=args.verify):
                continue

            ex = _to_example(corr, radius=args.radius)
            w.write(json.dumps(ex, ensure_ascii=False) + "\n")
            written += 1

    print(f"Wrote {written} examples to {args.out}")
    if written < args.n:
        print(f"WARNING: Could not reach requested n={args.n}. Attempts={attempts}. Increase --max_attempts or add more seeds.")


if __name__ == "__main__":
    main()