from __future__ import annotations

from typing import Dict, Any


def build_green_recommendation(metrics: Dict[str, Any]) -> Dict[str, str]:
    phase_ms = metrics.get("phase_ms", {})
    counters = metrics.get("counters", {})
    values = metrics.get("values", {})

    hotspot = "overall pipeline"
    hotspot_time = -1.0
    for name, ms in phase_ms.items():
        if ms > hotspot_time:
            hotspot = name
            hotspot_time = ms

    suggestion = "Pipeline looks efficient."

    if counters.get("ai_fixes", 0) >= 4:
        suggestion = "Reduce repeated AI fallback by improving deterministic fixes and early stopping."
    elif hotspot == "syntax_repair":
        suggestion = "Syntax repair dominates runtime; add stronger sync-point recovery and candidate pruning."
    elif hotspot == "semantic_phase":
        suggestion = "Semantic checking dominates runtime; consider lightweight pre-checks before full analysis."
    elif hotspot == "security_phase":
        suggestion = "Security phase dominates runtime; run targeted checks only after parse success."
    elif values.get("semantic_issue_count", 0) > 0:
        suggestion = "Reduce downstream semantic issues by improving identifier and declaration fixes earlier."

    return {
        "hotspot": hotspot,
        "suggestion": suggestion,
    }