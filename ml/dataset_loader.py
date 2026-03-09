import json
from typing import List, Tuple, Dict, Any, Optional


def load_jsonl_rows(path: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Loads a jsonl file into a list of dict rows.
    Each line must be valid JSON.
    """
    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if limit is not None and i >= limit:
                break
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def load_jsonl_inputs_targets(
    path: str,
    src_key: str = "input",
    tgt_key: str = "target",
    limit: Optional[int] = None,
) -> Tuple[List[str], List[str]]:
    """
    Returns two lists: inputs, targets
    """
    rows = load_jsonl_rows(path, limit=limit)
    inputs: List[str] = []
    targets: List[str] = []

    for r in rows:
        if src_key not in r or tgt_key not in r:
            raise KeyError(f"Missing '{src_key}' or '{tgt_key}' in row keys: {list(r.keys())}")
        inputs.append(r[src_key])
        targets.append(r[tgt_key])

    return inputs, targets