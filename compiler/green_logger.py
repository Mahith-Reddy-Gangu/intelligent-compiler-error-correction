from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class GreenLogger:
    def __init__(self, log_path: str = "logs/green_metrics.jsonl"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log_run(self, payload: Dict[str, Any]) -> None:
        record = {
            "ts_utc": _utc_now_iso(),
            **payload,
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")