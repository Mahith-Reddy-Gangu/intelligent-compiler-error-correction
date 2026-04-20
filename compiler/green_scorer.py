from __future__ import annotations

from typing import Dict, Any


def build_green_report(metrics: Dict[str, Any]) -> Dict[str, Any]:
    phase_ms = metrics.get("phase_ms", {})
    counters = metrics.get("counters", {})
    values = metrics.get("values", {})

    total_ms = metrics.get("total_runtime_ms", 0.0)

    score = 100

    score -= min(int(total_ms / 80), 30)
    score -= min(counters.get("ai_fixes", 0) * 4, 20)
    score -= min(counters.get("rule_fixes", 0) * 2, 10)
    score -= min(counters.get("lex_fixes", 0), 5)
    score -= min(counters.get("sym_fixes", 0) * 2, 10)
    score -= min(counters.get("sem_fixes", 0) * 2, 10)
    score -= min(values.get("semantic_issue_count", 0) * 3, 15)

    if values.get("parse_success"):
        score += 5

    status = values.get("status", "")
    if status == "STOPPED":
        score -= 15
    elif status == "UNFIXABLE":
        score -= 10
    elif status == "BLOCKED_SECURITY":
        score -= 12

    if score < 0:
        score = 0
    if score > 100:
        score = 100

    hotspot = "overall pipeline"
    hotspot_time = -1.0
    for name, ms in phase_ms.items():
        if name == "total":
            continue
        if ms > hotspot_time:
            hotspot = name
            hotspot_time = ms

    suggestion = "Pipeline looks efficient."

    if counters.get("ai_fixes", 0) >= 4:
        suggestion = "Reduce repeated AI fallback by improving deterministic fixes and early stopping."
    elif hotspot == "syntax_repair":
        suggestion = "Syntax repair dominates runtime; add stronger recovery sync points and prune weak AI candidates."
    elif hotspot == "semantic_phase":
        suggestion = "Semantic checking dominates runtime; run lighter checks before full semantic analysis."
    elif hotspot == "security_phase":
        suggestion = "Security phase dominates runtime; run targeted security checks only after parse success."
    elif hotspot == "lexical_phase":
        suggestion = "Lexical cleanup is taking noticeable time; consolidate typo cleanup rules."
    elif values.get("semantic_issue_count", 0) > 0:
        suggestion = "Reduce downstream semantic issues by improving identifier and declaration fixes earlier."

    report = {
        "total_runtime_ms": round(total_ms, 2),
        "phase_ms": {k: round(v, 2) for k, v in phase_ms.items()},
        "counters": dict(counters),
        "values": dict(values),
        "green_score": score,
        "hotspot": hotspot,
        "suggestion": suggestion,
    }

    return report