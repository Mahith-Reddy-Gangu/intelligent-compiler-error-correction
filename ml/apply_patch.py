from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

INS_LC_RE = re.compile(r"^\s*INS_LC\s+(\d+)\s+(\d+)\s+(.+?)\s*$", re.IGNORECASE)
DEL_LC_RE = re.compile(r"^\s*DEL_LC\s+(\d+)\s+(\d+)\s*$", re.IGNORECASE)
REP_LC_RE = re.compile(r"^\s*REP_LC\s+(\d+)\s+(\d+)\s+(.+?)\s*$", re.IGNORECASE)


@dataclass(frozen=True)
class PatchCommandLC:
    op: str
    line: int        # 1-based
    col: int         # 0-based
    payload: Optional[str] = None


def parse_lc_patch(patch: str) -> Optional[PatchCommandLC]:
    patch = (patch or "").strip()
    if not patch:
        return None

    m = INS_LC_RE.match(patch)
    if m:
        return PatchCommandLC("INS_LC", int(m.group(1)), int(m.group(2)), m.group(3).strip())

    m = DEL_LC_RE.match(patch)
    if m:
        return PatchCommandLC("DEL_LC", int(m.group(1)), int(m.group(2)), None)

    m = REP_LC_RE.match(patch)
    if m:
        return PatchCommandLC("REP_LC", int(m.group(1)), int(m.group(2)), m.group(3).strip())

    return None


def apply_lc_patch(source: str, patch_cmd: PatchCommandLC) -> str:
    lines = source.splitlines(keepends=True)
    if not lines:
        return source

    li = max(1, min(patch_cmd.line, len(lines))) - 1
    original_line = lines[li]

    line_no_nl = original_line.rstrip("\r\n")
    nl = original_line[len(line_no_nl):]

    col = max(0, min(patch_cmd.col, len(line_no_nl)))

    if patch_cmd.op == "INS_LC":
        payload = patch_cmd.payload or ""
        new_line = line_no_nl[:col] + payload + line_no_nl[col:]

    elif patch_cmd.op == "DEL_LC":
        if col >= len(line_no_nl):
            new_line = line_no_nl
        else:
            new_line = line_no_nl[:col] + line_no_nl[col + 1 :]

    elif patch_cmd.op == "REP_LC":
        payload = patch_cmd.payload or ""
        if col >= len(line_no_nl):
            new_line = line_no_nl + payload
        else:
            new_line = line_no_nl[:col] + payload + line_no_nl[col + 1 :]

    else:
        return source

    lines[li] = new_line + nl
    return "".join(lines)


def apply_patch(source: str, patch_str: str) -> str:
    """
    Public helper for your pipeline.
    Currently supports only LC commands.
    """
    cmd = parse_lc_patch(patch_str)
    if not cmd:
        return source
    return apply_lc_patch(source, cmd)