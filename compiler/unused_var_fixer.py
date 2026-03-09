import re
from typing import Optional, Tuple

# Very conservative:
# Only delete a single-variable declaration with no initializer and no comma/array:
#   int x;
#   float y;
#   char c;
#   void* not in your grammar, so ignore pointers.
#
# We do NOT touch:
#   int x = 1;
#   int x, y;
#   int a[10];
#   anything with comments on the line (to avoid destroying formatting/meaning)

_SIMPLE_DECL_RE = re.compile(
    r"""^
        (?P<indent>\s*)
        int
        \s+
        (?P<name>[A-Za-z_][A-Za-z_0-9]*)
        \s*
        ;
        \s*$
    """,
    re.VERBOSE,
)


def remove_unused_decl_at(source: str, decl_line: int, decl_col: int, name: str) -> Tuple[str, Optional[str]]:
    """
    Remove a very simple unused declaration at the given line.
    Only removes lines like: 'int x;' (no init, no arrays, no commas, no comments).

    Returns: (new_source, msg_or_None)
    """
    lines = source.splitlines(keepends=True)
    idx = decl_line - 1
    if idx < 0 or idx >= len(lines):
        return source, None

    original = lines[idx]
    line_no_nl = original.rstrip("\r\n")

    # refuse to touch if there are comments on the line
    if "//" in line_no_nl or "/*" in line_no_nl or "*/" in line_no_nl:
        return source, None

    m = _SIMPLE_DECL_RE.match(line_no_nl)
    if not m:
        return source, None

    if m.group("name") != name:
        return source, None

    # delete the whole line
    del lines[idx]
    return "".join(lines), f"removed unused declaration: {name}"