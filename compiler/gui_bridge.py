import re
from typing import Dict, Any, List

from compiler.error_classifier import classify_error_message
from compiler.error_corrector import apply_correction
from compiler.lexical_corrector import fix_common_lexical_issues
from compiler.ai_error_corrector import ai_generate_patch_candidates
from compiler.identifier_corrector import fix_identifier_typo_at
from compiler.security_checker import SecurityChecker

from test_parser import (
    parse_source,
    has_any_errors,
    get_all_error_strings,
    get_first_error_object,
    build_symbols,
    DETERMINISTIC_REASONS,
    _select_best_ai_candidate_by_reparse,
)

# Repair limits
MAX_LEX_EDITS = 5
MAX_SYN_EDITS = 120
NO_IMPROVE_LIMIT = 8
REPEAT_LIMIT = 6


def _compute_changed_lines(old_text: str, new_text: str) -> List[int]:
    """Return 1-indexed line numbers that differ between old and new source."""
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()
    max_len = max(len(old_lines), len(new_lines))
    changed = []
    for i in range(max_len):
        old_line = old_lines[i] if i < len(old_lines) else ""
        new_line = new_lines[i] if i < len(new_lines) else ""
        if old_line != new_line:
            changed.append(i + 1)
    return changed


def _run_security_check(source_text: str) -> List[str]:
    """Run SecurityChecker and return formatted warning strings."""
    checker = SecurityChecker()
    return [
        f"[{issue.severity}] {issue.message} — {issue.suggestion}"
        for issue in checker.check(source_text)
    ]


def _emit_progress(
    kind: str,
    message: str,
    working: str,
    steps: List[str],
    stats: Dict[str, int],
    status: str = "RUNNING",
) -> Dict[str, Any]:
    total_done = (
        stats.get("lex_fixes", 0)
        + stats.get("rule_fixes", 0)
        + stats.get("ai_fixes", 0)
        + stats.get("sym_fixes", 0)
    )
    return {
        "type": kind,
        "status": status,
        "message": message,
        "corrected_code": working,
        "applied_steps": steps[:],
        "stats": dict(stats),
        "total_repairs": total_done,
    }


def repair_source_for_gui_stream(source_text: str, filename: str = "main.c"):
    """
    Streaming repair pipeline (Server-Sent Events).

    Phases:
      1. Lexical cleanup
      2. Syntax repair loop (rule-based → AI fallback)
      3. Security check (read-only report)
    """
    original_source = source_text
    working = source_text

    steps: List[str] = []
    parse_errors: List[str] = []

    stats = {
        "lex_fixes": 0,
        "rule_fixes": 0,
        "ai_fixes": 0,
        "sym_fixes": 0,
        "iterations": 0,
    }

    yield _emit_progress("start", f"Started repairing {filename}", working, steps, stats)

    # ------------------------------------------------------------------
    # Phase 1: Lexical cleanup
    # ------------------------------------------------------------------
    for _ in range(MAX_LEX_EDITS):
        new_src, lex_fix = fix_common_lexical_issues(working)
        if not lex_fix or new_src == working:
            break
        working = new_src
        step_msg = f"LEX: {lex_fix}"
        steps.append(step_msg)
        stats["lex_fixes"] += 1
        yield _emit_progress("fix", step_msg, working, steps, stats)

    # ------------------------------------------------------------------
    # Initial parse after lexical cleanup
    # ------------------------------------------------------------------
    tree, listeners, parser = parse_source(working, f"{filename} (after-lex)")

    if tree is None:
        yield {
            "type": "done",
            "status": "STOPPED",
            "message": "Parsing stopped after lexical phase.",
            "corrected_code": working,
            "applied_steps": steps,
            "stats": stats,
            "errors": parse_errors,
            "security_warnings": [],
            "changed_lines": _compute_changed_lines(original_source, working),
            "success": False,
        }
        return

    edits = 0
    parse_errors = get_all_error_strings(listeners) if has_any_errors(listeners) else []
    best_error_count = len(parse_errors)
    no_improve_rounds = 0
    last_sig = None
    repeat = 0

    # ------------------------------------------------------------------
    # Phase 2: Syntax repair loop
    # ------------------------------------------------------------------
    while has_any_errors(listeners) and edits < MAX_SYN_EDITS:
        stats["iterations"] += 1
        errs = get_all_error_strings(listeners)
        parse_errors = errs[:]

        error_obj = get_first_error_object(listeners)
        if not error_obj:
            break

        msg = error_obj["msg"]
        line = error_obj["line"]
        col = error_obj["column"]
        stage = error_obj.get("stage", "?")
        off = error_obj.get("offending")

        classification = classify_error_message(msg)

        yield _emit_progress(
            "detect",
            f"Detected {classification.reason} at line {line}",
            working,
            steps,
            stats,
        )

        sig = (stage, line, col, classification.reason, msg)
        if sig == last_sig:
            repeat += 1
        else:
            repeat = 0
        last_sig = sig

        if repeat >= REPEAT_LIMIT:
            break

        symbols = build_symbols(tree)

        # Try symbol/identifier typo fix first
        if off and isinstance(off, str) and re.match(r"^[A-Za-z_][A-Za-z_0-9]*$", off):
            corrected, msg2 = fix_identifier_typo_at(working, line, col, symbols, max_dist=2)
            if msg2 is not None and corrected != working:
                working = corrected
                steps.append(f"SYM: {msg2}")
                stats["sym_fixes"] += 1
                edits += 1

                yield _emit_progress("fix", f"SYM: {msg2}", working, steps, stats)

                tree, listeners, parser = parse_source(working, f"{filename} (sym-fixed)")
                if tree is None:
                    break

                cur_error_count = len(get_all_error_strings(listeners))
                if cur_error_count < best_error_count:
                    best_error_count = cur_error_count
                    no_improve_rounds = 0
                else:
                    no_improve_rounds += 1

                if no_improve_rounds >= NO_IMPROVE_LIMIT:
                    break
                if not has_any_errors(listeners):
                    break
                continue

        if stage == "LEX":
            # Lexer errors: go straight to AI candidates
            candidates = ai_generate_patch_candidates(
                working, line, col, reason=classification.reason, top_k=5, debug=False
            )
            ai_src, cmd, tree2, listeners2, parser2 = _select_best_ai_candidate_by_reparse(
                filename, working, candidates
            )
            if cmd is None or ai_src == working or tree2 is None:
                break

            working = ai_src
            steps.append(f"AI: {cmd}")
            stats["ai_fixes"] += 1
            edits += 1
            tree, listeners, parser = tree2, listeners2, parser2

            yield _emit_progress("fix", f"AI: {cmd}", working, steps, stats)

        else:
            # Parser errors: try deterministic rule first, then AI fallback
            deterministic_attempted = False
            deterministic_changed = False

            if classification.reason in DETERMINISTIC_REASONS:
                deterministic_attempted = True
                corrected, applied = apply_correction(working, line, col, classification)

                if applied is not None and corrected != working:
                    deterministic_changed = True
                    working = corrected
                    steps.append(f"RULE: {applied}")
                    stats["rule_fixes"] += 1
                    edits += 1

                    tree, listeners, parser = parse_source(working, f"{filename} (rule-fixed)")
                    if tree is None:
                        break

                    yield _emit_progress("fix", f"RULE: {applied}", working, steps, stats)

            if has_any_errors(listeners):
                if classification.reason not in DETERMINISTIC_REASONS or (
                    deterministic_attempted and not deterministic_changed
                ):
                    candidates = ai_generate_patch_candidates(
                        working, line, col, reason=classification.reason, top_k=5, debug=False
                    )
                    ai_src, cmd, tree2, listeners2, parser2 = _select_best_ai_candidate_by_reparse(
                        filename, working, candidates
                    )
                    if cmd is None or ai_src == working or tree2 is None:
                        break

                    working = ai_src
                    steps.append(f"AI: {cmd}")
                    stats["ai_fixes"] += 1
                    edits += 1
                    tree, listeners, parser = tree2, listeners2, parser2

                    yield _emit_progress("fix", f"AI: {cmd}", working, steps, stats)

        cur_error_count = len(get_all_error_strings(listeners))
        if cur_error_count < best_error_count:
            best_error_count = cur_error_count
            no_improve_rounds = 0
        else:
            no_improve_rounds += 1

        if no_improve_rounds >= NO_IMPROVE_LIMIT:
            break
        if not has_any_errors(listeners):
            break

    # ------------------------------------------------------------------
    # Determine final status
    # ------------------------------------------------------------------
    if tree is None:
        status = "STOPPED"
    elif has_any_errors(listeners):
        status = "UNFIXABLE"
        parse_errors = get_all_error_strings(listeners)
    else:
        status = "SUCCESS"

    # ------------------------------------------------------------------
    # Phase 3: Security check (read-only)
    # ------------------------------------------------------------------
    security_warnings = _run_security_check(working)

    yield {
        "type": "done",
        "status": status,
        "success": status == "SUCCESS",
        "filename": filename,
        "corrected_code": working,
        "applied_steps": steps,
        "errors": parse_errors,
        "security_warnings": security_warnings,
        "changed_lines": _compute_changed_lines(original_source, working),
        "stats": stats,
        "total_repairs": (
            stats.get("lex_fixes", 0)
            + stats.get("rule_fixes", 0)
            + stats.get("ai_fixes", 0)
            + stats.get("sym_fixes", 0)
        ),
    }


def repair_source_for_gui(source_text: str, filename: str = "main.c") -> Dict[str, Any]:
    """
    Non-streaming repair pipeline.

    Phases:
      1. Lexical cleanup
      2. Syntax repair loop (rule-based → AI fallback)
      3. Security check (read-only report)
    """
    original_source = source_text
    working = source_text

    steps: List[str] = []
    parse_errors: List[str] = []

    stats = {
        "lex_fixes": 0,
        "rule_fixes": 0,
        "ai_fixes": 0,
        "sym_fixes": 0,
        "iterations": 0,
    }

    # ------------------------------------------------------------------
    # Phase 1: Lexical cleanup
    # ------------------------------------------------------------------
    for _ in range(MAX_LEX_EDITS):
        new_src, lex_fix = fix_common_lexical_issues(working)
        if not lex_fix or new_src == working:
            break
        working = new_src
        steps.append(f"LEX: {lex_fix}")
        stats["lex_fixes"] += 1

    # ------------------------------------------------------------------
    # Initial parse after lexical cleanup
    # ------------------------------------------------------------------
    tree, listeners, parser = parse_source(working, f"{filename} (after-lex)")

    if tree is None:
        return {
            "success": False,
            "status": "STOPPED",
            "filename": filename,
            "corrected_code": working,
            "applied_steps": steps,
            "errors": [],
            "security_warnings": [],
            "changed_lines": _compute_changed_lines(original_source, working),
            "stats": stats,
        }

    if has_any_errors(listeners):
        parse_errors = get_all_error_strings(listeners)

    # ------------------------------------------------------------------
    # Phase 2: Syntax repair loop
    # ------------------------------------------------------------------
    edits = 0
    best_error_count = len(parse_errors)
    no_improve_rounds = 0
    last_sig = None
    repeat = 0

    while has_any_errors(listeners) and edits < MAX_SYN_EDITS:
        stats["iterations"] += 1
        errs = get_all_error_strings(listeners)
        parse_errors = errs[:]

        error_obj = get_first_error_object(listeners)
        if not error_obj:
            break

        msg = error_obj["msg"]
        line = error_obj["line"]
        col = error_obj["column"]
        stage = error_obj.get("stage", "?")
        off = error_obj.get("offending")

        classification = classify_error_message(msg)

        sig = (stage, line, col, classification.reason, msg)
        if sig == last_sig:
            repeat += 1
        else:
            repeat = 0
        last_sig = sig

        if repeat >= REPEAT_LIMIT:
            break

        symbols = build_symbols(tree)

        # Try symbol/identifier typo fix first
        if off and isinstance(off, str) and re.match(r"^[A-Za-z_][A-Za-z_0-9]*$", off):
            corrected, msg2 = fix_identifier_typo_at(working, line, col, symbols, max_dist=2)
            if msg2 is not None and corrected != working:
                working = corrected
                steps.append(f"SYM: {msg2}")
                stats["sym_fixes"] += 1
                edits += 1

                tree, listeners, parser = parse_source(working, f"{filename} (sym-fixed)")
                if tree is None:
                    break

                cur_error_count = len(get_all_error_strings(listeners))
                if cur_error_count < best_error_count:
                    best_error_count = cur_error_count
                    no_improve_rounds = 0
                else:
                    no_improve_rounds += 1

                if no_improve_rounds >= NO_IMPROVE_LIMIT:
                    break
                if not has_any_errors(listeners):
                    break
                continue

        if stage == "LEX":
            candidates = ai_generate_patch_candidates(
                working, line, col, reason=classification.reason, top_k=5, debug=False
            )
            ai_src, cmd, tree2, listeners2, parser2 = _select_best_ai_candidate_by_reparse(
                filename, working, candidates
            )
            if cmd is None or ai_src == working or tree2 is None:
                break

            working = ai_src
            steps.append(f"AI: {cmd}")
            stats["ai_fixes"] += 1
            edits += 1
            tree, listeners, parser = tree2, listeners2, parser2

        else:
            # Parser errors: try deterministic rule first, then AI fallback
            deterministic_attempted = False
            deterministic_changed = False

            if classification.reason in DETERMINISTIC_REASONS:
                deterministic_attempted = True
                corrected, applied = apply_correction(working, line, col, classification)

                if applied is not None and corrected != working:
                    deterministic_changed = True
                    working = corrected
                    steps.append(f"RULE: {applied}")
                    stats["rule_fixes"] += 1
                    edits += 1

                    tree, listeners, parser = parse_source(working, f"{filename} (rule-fixed)")
                    if tree is None:
                        break

            if has_any_errors(listeners):
                if classification.reason not in DETERMINISTIC_REASONS or (
                    deterministic_attempted and not deterministic_changed
                ):
                    candidates = ai_generate_patch_candidates(
                        working, line, col, reason=classification.reason, top_k=5, debug=False
                    )
                    ai_src, cmd, tree2, listeners2, parser2 = _select_best_ai_candidate_by_reparse(
                        filename, working, candidates
                    )
                    if cmd is None or ai_src == working or tree2 is None:
                        break

                    working = ai_src
                    steps.append(f"AI: {cmd}")
                    stats["ai_fixes"] += 1
                    edits += 1
                    tree, listeners, parser = tree2, listeners2, parser2

        cur_error_count = len(get_all_error_strings(listeners))
        if cur_error_count < best_error_count:
            best_error_count = cur_error_count
            no_improve_rounds = 0
        else:
            no_improve_rounds += 1

        if no_improve_rounds >= NO_IMPROVE_LIMIT:
            break
        if not has_any_errors(listeners):
            break

    # ------------------------------------------------------------------
    # Determine final status
    # ------------------------------------------------------------------
    if tree is None:
        status = "STOPPED"
    elif has_any_errors(listeners):
        status = "UNFIXABLE"
        parse_errors = get_all_error_strings(listeners)
    else:
        status = "SUCCESS"

    # ------------------------------------------------------------------
    # Phase 3: Security check (read-only)
    # ------------------------------------------------------------------
    security_warnings = _run_security_check(working)

    return {
        "success": status == "SUCCESS",
        "status": status,
        "filename": filename,
        "corrected_code": working,
        "applied_steps": steps,
        "errors": parse_errors,
        "security_warnings": security_warnings,
        "changed_lines": _compute_changed_lines(original_source, working),
        "stats": stats,
        "total_applied_steps": len(steps),
    }