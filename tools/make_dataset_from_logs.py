import json
import os
from typing import Dict, List, Optional, Tuple


def _safe_int(x, default=0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def _extract_line_col_from_error_string(s: str) -> Tuple[Optional[int], Optional[int]]:
    # Example: "Line 3:2 - PARSE Error: missing ';' at 'return' (offending: return)"
    # We parse the "Line X:Y" part.
    s = s.strip()
    if not s.lower().startswith("line "):
        return None, None
    try:
        after = s.split("Line ", 1)[1]
        loc = after.split(" - ", 1)[0]  # "3:2"
        line_s, col_s = loc.split(":", 1)
        return _safe_int(line_s, None), _safe_int(col_s, None)
    except Exception:
        return None, None


def make_dataset_from_repair_log(
    log_path: str,
    out_path: str,
    only_ai_steps: bool = True,
) -> None:
    """
    Reads repair_log.jsonl and emits patch-training JSONL.

    We look for events:
      - case_start -> gives original_source
      - parse_errors -> contains list[str] with "Line X:Y ..."
      - repair_step with kind == "AI" -> contains cmd and source_after

    We reconstruct source_before_ai as:
      - last known source (starts at original_source, then each repair_step updates it)
    """
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"repair log not found: {log_path}")

    # State per case_id
    cases: Dict[str, Dict] = {}

    out_rows: List[Dict] = []
    ex_idx = 0

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            obj = json.loads(line)
            event = obj.get("event")
            data = obj.get("data", {})
            case_id = data.get("case_id")
            if not case_id:
                continue

            if case_id not in cases:
                cases[case_id] = {
                    "original_source": None,
                    "current_source": None,
                    "latest_err_line": None,
                    "latest_err_col": None,
                    "latest_reason": None,
                    "filename": None,
                }

            st = cases[case_id]

            if event == "case_start":
                st["original_source"] = data.get("original_source", "")
                st["current_source"] = st["original_source"]
                st["filename"] = data.get("filename")
                st["latest_err_line"] = None
                st["latest_err_col"] = None
                st["latest_reason"] = None

            elif event == "parse_errors":
                # Parse first error line/col from the first error string
                errors = data.get("errors", [])
                if errors:
                    line_num, col_num = _extract_line_col_from_error_string(errors[0])
                    st["latest_err_line"] = line_num
                    st["latest_err_col"] = col_num

                # We can also store reason from message if present (best-effort)
                # Example fragment: "missing ';'"
                if errors:
                    msg = errors[0].lower()
                    if "missing" in msg and "';'" in msg:
                        st["latest_reason"] = "missing_semicolon"
                    elif "missing" in msg and "'}'" in msg:
                        st["latest_reason"] = "missing_rbrace"
                    elif "missing" in msg and "'{'" in msg:
                        st["latest_reason"] = "missing_lbrace"
                    elif "missing" in msg and "')'" in msg:
                        st["latest_reason"] = "missing_rparen"
                    elif "missing" in msg and "'('" in msg:
                        st["latest_reason"] = "missing_lparen"
                    elif "extraneous input" in msg:
                        st["latest_reason"] = "extraneous_token"
                    elif "mismatched input" in msg:
                        st["latest_reason"] = "mismatched_token"
                    elif "no viable alternative" in msg:
                        st["latest_reason"] = "no_viable_alternative"
                    elif "token recognition error" in msg:
                        st["latest_reason"] = "illegal_token"
                    else:
                        st["latest_reason"] = st["latest_reason"] or "unknown"

            elif event == "repair_step":
                kind = data.get("kind")
                source_after = data.get("source_after")

                if kind and source_after is not None:
                    # if AI step, record training example
                    if kind == "AI":
                        cmd = data.get("cmd") or data.get("step")
                        if cmd:
                            # Need a prompt window: use same function signature you use in ai_corrector.py.
                            # We reproduce prompt building here without importing your project.
                            source_before = st["current_source"] if st["current_source"] is not None else ""

                            err_line = st["latest_err_line"]
                            err_col = st["latest_err_col"]

                            # If error location missing, skip (we can't place <ERR>)
                            if err_line is None or err_col is None:
                                # Still update state and continue
                                st["current_source"] = source_after
                                continue

                            prompt = build_prompt_window(source_before, err_line, err_col, radius=3)

                            out_rows.append(
                                {
                                    "id": f"log-{case_id}-{ex_idx}",
                                    "prompt": prompt,
                                    "target": cmd.strip(),
                                    "meta": {
                                        "source": "logs",
                                        "filename": st.get("filename"),
                                        "reason": st.get("latest_reason") or "unknown",
                                        "error_line": int(err_line),
                                        "error_col": int(err_col),
                                    },
                                }
                            )
                            ex_idx += 1

                    # Update current source no matter what step kind
                    st["current_source"] = source_after

            else:
                # ignore other events
                pass

    # Optionally filter
    if only_ai_steps:
        filtered = out_rows
    else:
        filtered = out_rows

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as out:
        for row in filtered:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote {len(filtered)} examples to {out_path}")


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


def main():
    log_path = "logs/repair_log.jsonl"
    out_path = "data/raw/patch_train_from_logs.jsonl"
    make_dataset_from_repair_log(log_path, out_path, only_ai_steps=True)


if __name__ == "__main__":
    main()