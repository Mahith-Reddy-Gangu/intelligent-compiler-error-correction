from typing import Dict, Any, List, Optional

from compiler.error_classifier import classify_error_message
from compiler.error_corrector import apply_correction
from compiler.lexical_corrector import fix_common_lexical_issues
from compiler.ai_error_corrector import ai_generate_patch_candidates
from compiler.identifier_corrector import fix_identifier_typo_at
from compiler.semantic_checker import SemanticChecker
from compiler.security_checker import SecurityChecker
from compiler.taint_checker import TaintChecker
from compiler.string_flow_checker import StringFlowChecker
from compiler.unused_var_fixer import remove_unused_decl_at
from compiler.security_auto_fixer import SecurityAutoFixer

from test_parser import (
    parse_source,
    has_any_errors,
    get_all_error_strings,
    get_first_error_object,
    build_symbols,
    DETERMINISTIC_REASONS,
    _select_best_ai_candidate_by_reparse,
)


def _compute_changed_lines(old_text: str, new_text: str) -> List[int]:
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


def _collect_security_issues(source_text: str) -> List[str]:
    issues = []

    security_checker = SecurityChecker()
    taint_checker = TaintChecker()
    string_checker = StringFlowChecker()

    for issue in security_checker.check(source_text):
        issues.append(f"[{issue.severity}] {issue.message} (score={issue.score})")

    for issue in taint_checker.check(source_text):
        issues.append(f"[{issue.severity}] {issue.message} (score={issue.score})")

    for issue in string_checker.check(source_text):
        issues.append(f"[{issue.severity}] {issue.message} (score={issue.score})")

    return issues


def _collect_semantic_issues(tree) -> List[Dict[str, Any]]:
    checker = SemanticChecker()
    checker.visit(tree)
    return checker.get_issues()


def _status_from_security(security_warnings: List[str]) -> str:
    if not security_warnings:
        return "SUCCESS"

    blocked = False
    total_score = 0

    for item in security_warnings:
        if "[CRITICAL]" in item:
            blocked = True

        marker = "(score="
        pos = item.find(marker)
        if pos != -1:
            end = item.find(")", pos)
            if end != -1:
                try:
                    total_score += int(item[pos + len(marker):end])
                except ValueError:
                    pass

    if blocked or total_score >= 6:
        return "BLOCKED_SECURITY"

    return "SUCCESS_WITH_WARNINGS"


def _try_remove_unused_decl(
    working: str,
    issue: Dict[str, Any],
) -> tuple[str, Optional[str]]:
    name = issue.get("name")
    line = issue.get("line")
    col = issue.get("col")

    corrected = None
    msg = None

    try:
        corrected, msg = remove_unused_decl_at(working, line, col, name)
    except TypeError:
        try:
            corrected, msg = remove_unused_decl_at(working, line, col)
        except TypeError:
            try:
                corrected, msg = remove_unused_decl_at(working, line, name)
            except Exception:
                corrected, msg = None, None
    except Exception:
        corrected, msg = None, None

    return corrected if corrected is not None else working, msg


def _run_semantic_phase_for_gui(
    filename: str,
    working: str,
    tree,
    listeners,
    parser,
    steps: List[str],
    logs: List[str],
    stats: Dict[str, int],
):
    """
    GUI version of the unified iterative semantic phase.

    Important design choice:
    - Do NOT stop immediately on undeclared identifiers that may actually be
      security-relevant library calls like gets/strcpy/sprintf.
    - Allow security phase to run after semantic checking.
    """
    MAX_SEM_EDITS = 5
    sem_edits = 0

    while sem_edits < MAX_SEM_EDITS:
        issues = _collect_semantic_issues(tree)

        if not issues:
            break

        first = issues[0]
        kind = first.get("kind")

        if kind == "unused":
            corrected, msg = _try_remove_unused_decl(working, first)

            if msg is None or corrected == working:
                # Cannot apply semantic fix; let security phase still run.
                break

            working = corrected
            steps.append(f"SEM: {msg}")
            logs.append(f"Applied semantic fix: {msg}")
            stats["sem_fixes"] = stats.get("sem_fixes", 0) + 1
            sem_edits += 1

            tree2, listeners2, parser2 = parse_source(working, f"{filename} (unused-removed)")
            if tree2 is None or has_any_errors(listeners2):
                remaining = get_all_error_strings(listeners2) if tree2 is not None else []
                return {
                    "status": "STOPPED",
                    "working": working,
                    "tree": tree2,
                    "listeners": listeners2,
                    "parser": parser2,
                    "semantic_issues": issues,
                    "parse_errors": remaining,
                }

            tree, listeners, parser = tree2, listeners2, parser2
            continue

        if kind == "undeclared":
            name = first.get("name")
            line = first.get("line")
            col = first.get("col")

            symbols = build_symbols(tree)
            corrected, msg = fix_identifier_typo_at(
                working,
                line,
                col,
                symbols,
                max_dist=2,
                expected_name=name,
            )

            if msg is None or corrected == working:
                # Important: do not return yet.
                # names like gets/strcpy/sprintf may be security-fixable.
                break

            working = corrected
            steps.append(f"SEM: {msg}")
            logs.append(f"Applied semantic fix: {msg}")
            stats["sem_fixes"] = stats.get("sem_fixes", 0) + 1
            sem_edits += 1

            tree2, listeners2, parser2 = parse_source(working, f"{filename} (sym-fixed-sem)")
            if tree2 is None or has_any_errors(listeners2):
                remaining = get_all_error_strings(listeners2) if tree2 is not None else []
                return {
                    "status": "STOPPED",
                    "working": working,
                    "tree": tree2,
                    "listeners": listeners2,
                    "parser": parser2,
                    "semantic_issues": issues,
                    "parse_errors": remaining,
                }

            tree, listeners, parser = tree2, listeners2, parser2
            continue

        # Other semantic issues: stop semantic auto-fixing here, but still let
        # security phase run afterwards.
        break

    issues = _collect_semantic_issues(tree)

    return {
        "status": "SEM_CLEAN" if not issues else "SEM_ISSUES",
        "working": working,
        "tree": tree,
        "listeners": listeners,
        "parser": parser,
        "semantic_issues": issues,
    }


def repair_source_for_gui(source_text: str, filename: str = "main.c") -> Dict[str, Any]:
    original_source = source_text
    working = source_text

    steps: List[str] = []
    logs: List[str] = []
    parse_errors: List[str] = []
    semantic_issues: List[Dict[str, Any]] = []
    security_warnings: List[str] = []
    security_changed_lines: List[int] = []

    MAX_LEX_EDITS = 3
    MAX_SYN_EDITS = 5
    MAX_SECURITY_ROUNDS = 3

    stats = {
        "lex_fixes": 0,
        "rule_fixes": 0,
        "ai_fixes": 0,
        "sym_fixes": 0,
        "sem_fixes": 0,
        "iterations": 0,
    }

    result: Dict[str, Any] = {
        "success": False,
        "status": "STOPPED",
        "filename": filename,
        "corrected_code": working,
        "applied_steps": [],
        "logs": [],
        "errors": [],
        "semantic_issues": [],
        "security_warnings": [],
        "changed_lines": [],
        "security_changed_lines": [],
        "stats": stats,
    }

    # ---------------------------------------------------------
    # Phase 1: lexical cleanup
    # ---------------------------------------------------------
    for _ in range(MAX_LEX_EDITS):
        new_src, lex_fix = fix_common_lexical_issues(working)
        if not lex_fix or new_src == working:
            break

        working = new_src
        step_msg = f"LEX: {lex_fix}"
        steps.append(step_msg)
        logs.append(f"Applied lexical fix: {lex_fix}")
        stats["lex_fixes"] += 1

    # ---------------------------------------------------------
    # Initial parse after lexical cleanup
    # ---------------------------------------------------------
    tree, listeners, parser = parse_source(working, f"{filename} (gui-after-lex)")
    if tree is None:
        result["status"] = "STOPPED"
        result["corrected_code"] = working
        result["applied_steps"] = steps
        result["logs"] = logs + ["Parsing stopped: tree is None after lexical phase."]
        result["changed_lines"] = _compute_changed_lines(original_source, working)
        result["security_changed_lines"] = []
        return result

    if has_any_errors(listeners):
        parse_errors = get_all_error_strings(listeners)

    # ---------------------------------------------------------
    # Phase 2: syntax repair loop
    # ---------------------------------------------------------
    edits = 0
    best_error_count = len(parse_errors) if parse_errors else 0
    no_improve_rounds = 0
    last_sig = None
    repeat = 0

    while has_any_errors(listeners) and edits < MAX_SYN_EDITS:
        stats["iterations"] += 1
        errs = get_all_error_strings(listeners)
        parse_errors = errs[:]
        logs.append("Parsing failed; attempting repair.")
        logs.extend(errs)

        error_obj = get_first_error_object(listeners)
        if not error_obj:
            result["status"] = "STOPPED"
            break

        msg = error_obj["msg"]
        line = error_obj["line"]
        col = error_obj["column"]
        stage = error_obj.get("stage", "?")
        off = error_obj.get("offending")

        classification = classify_error_message(msg)

        logs.append(
            f"Classified error -> stage={stage}, category={classification.category}, "
            f"reason={classification.reason}, fixable={classification.fixable}"
        )

        sig = (stage, line, col, classification.reason, msg)
        if sig == last_sig:
            repeat += 1
        else:
            repeat = 0
        last_sig = sig

        if repeat >= 2:
            logs.append("Stopping: repeating same error (stuck).")
            result["status"] = "STOPPED"
            break

        symbols = build_symbols(tree)

        # Optional symbol typo correction
        if off and isinstance(off, str):
            import re
            if re.match(r"^[A-Za-z_][A-Za-z_0-9]*$", off):
                corrected, msg2 = fix_identifier_typo_at(working, line, col, symbols, max_dist=2)
                if msg2 is not None and corrected != working:
                    working = corrected
                    steps.append(f"SYM: {msg2}")
                    logs.append(f"Applied symbol fix: {msg2}")
                    stats["sym_fixes"] += 1
                    edits += 1

                    tree, listeners, parser = parse_source(working, f"{filename} (gui-sym-fixed)")
                    if tree is None:
                        result["status"] = "STOPPED"
                        break

                    cur_error_count = len(get_all_error_strings(listeners))
                    if cur_error_count < best_error_count:
                        best_error_count = cur_error_count
                        no_improve_rounds = 0
                    else:
                        no_improve_rounds += 1

                    if no_improve_rounds >= 2:
                        logs.append("Stopping: not improving error count (stuck).")
                        result["status"] = "STOPPED"
                        break

                    if not has_any_errors(listeners):
                        break

                    continue

        # Lexer-stage -> AI fallback
        if stage == "LEX":
            logs.append("Lexer-stage error remains; invoking AI patch candidates.")

            candidates = ai_generate_patch_candidates(
                working,
                line,
                col,
                reason=classification.reason,
                top_k=5,
                debug=False,
            )

            ai_src, cmd, tree2, listeners2, parser2 = _select_best_ai_candidate_by_reparse(
                filename,
                working,
                candidates,
            )

            if cmd is None or ai_src == working or tree2 is None:
                logs.append("AI: no valid patch produced.")
                result["status"] = "UNFIXABLE"
                break

            working = ai_src
            steps.append(f"AI: {cmd}")
            logs.append(f"Applied AI patch: {cmd}")
            stats["ai_fixes"] += 1
            edits += 1

            tree, listeners, parser = tree2, listeners2, parser2

        else:
            deterministic_attempted = False
            deterministic_changed = False

            if classification.reason in DETERMINISTIC_REASONS:
                deterministic_attempted = True
                corrected, applied = apply_correction(working, line, col, classification)

                if applied is not None and corrected != working:
                    deterministic_changed = True
                    working = corrected
                    steps.append(f"RULE: {applied}")
                    logs.append(f"Applied deterministic fix: {applied}")
                    stats["rule_fixes"] += 1
                    edits += 1

                    tree, listeners, parser = parse_source(working, f"{filename} (gui-rule-fixed)")
                    if tree is None:
                        result["status"] = "STOPPED"
                        break
                else:
                    logs.append("Deterministic fix made no change; allowing AI fallback.")

            if has_any_errors(listeners):
                if classification.reason not in DETERMINISTIC_REASONS or (
                    deterministic_attempted and not deterministic_changed
                ):
                    logs.append("Invoking AI patch-based correction.")

                    candidates = ai_generate_patch_candidates(
                        working,
                        line,
                        col,
                        reason=classification.reason,
                        top_k=5,
                        debug=False,
                    )

                    ai_src, cmd, tree2, listeners2, parser2 = _select_best_ai_candidate_by_reparse(
                        filename,
                        working,
                        candidates,
                    )

                    if cmd is None or ai_src == working or tree2 is None:
                        logs.append("AI: no valid patch produced.")
                        result["status"] = "UNFIXABLE"
                        break

                    working = ai_src
                    steps.append(f"AI: {cmd}")
                    logs.append(f"Applied AI patch: {cmd}")
                    stats["ai_fixes"] += 1
                    edits += 1

                    tree, listeners, parser = tree2, listeners2, parser2

        cur_error_count = len(get_all_error_strings(listeners))
        if cur_error_count < best_error_count:
            best_error_count = cur_error_count
            no_improve_rounds = 0
        else:
            no_improve_rounds += 1

        if no_improve_rounds >= 2:
            logs.append("Stopping: not improving error count (stuck).")
            result["status"] = "STOPPED"
            break

        if not has_any_errors(listeners):
            break

    # ---------------------------------------------------------
    # Final status after syntax phase
    # ---------------------------------------------------------
    if tree is None:
        result["status"] = "STOPPED"
    elif has_any_errors(listeners):
        if result["status"] not in {"STOPPED", "UNFIXABLE"}:
            result["status"] = "UNFIXABLE"
        parse_errors = get_all_error_strings(listeners)
    else:
        result["status"] = "PARSE_SUCCESS"

    # ---------------------------------------------------------
    # Phase 3: semantic + iterative security
    # ---------------------------------------------------------
    if tree is not None and not has_any_errors(listeners):
        security_rounds = 0

        while True:
            sem_result = _run_semantic_phase_for_gui(
                filename,
                working,
                tree,
                listeners,
                parser,
                steps,
                logs,
                stats,
            )

            working = sem_result["working"]
            tree = sem_result["tree"]
            listeners = sem_result["listeners"]
            parser = sem_result["parser"]
            semantic_issues = sem_result.get("semantic_issues", [])
            parse_errors = sem_result.get("parse_errors", parse_errors)

            if sem_result["status"] == "STOPPED":
                result["status"] = "STOPPED"
                result["success"] = False
                break

            # Always allow security phase to run, even if semantic issues remain.
            security_warnings = _collect_security_issues(working)

            if security_warnings:
                logs.append(f"Security issues detected: {len(security_warnings)}")
                logs.append("Invoking SecurityAutoFixer for GUI parity with CLI.")

                try:
                    auto_fixer = SecurityAutoFixer()
                    fix_result = auto_fixer.apply_fixes(working)

                    if fix_result.source != working:
                        changed_now = _compute_changed_lines(working, fix_result.source)
                        security_changed_lines = sorted(set(security_changed_lines + changed_now))

                        for step in fix_result.applied_steps:
                            steps.append(step)
                            logs.append(f"Applied security fix: {step}")

                        stats["ai_fixes"] += sum(
                            1 for s in fix_result.applied_steps if s.startswith("AISEC:")
                        )

                        working = fix_result.source
                        security_rounds += 1

                        if security_rounds > MAX_SECURITY_ROUNDS:
                            logs.append("Stopping: exceeded maximum security reparse rounds.")
                            result["status"] = "STOPPED"
                            result["success"] = False
                            break

                        tree2, listeners2, parser2 = parse_source(
                            working,
                            f"{filename} (gui-after-security-{security_rounds})",
                        )

                        if tree2 is None or has_any_errors(listeners2):
                            logs.append("Stopping: security fix broke parsing.")
                            parse_errors = get_all_error_strings(listeners2) if tree2 is not None else []
                            result["status"] = "STOPPED"
                            result["success"] = False
                            tree = tree2
                            listeners = listeners2
                            parser = parser2
                            break

                        tree, listeners, parser = tree2, listeners2, parser2
                        continue

                    logs.append("SecurityAutoFixer produced no code change.")
                except Exception as e:
                    logs.append(f"Security auto-fix failed: {str(e)}")

            # If semantic issues remain after giving security a chance, stop here.
            if semantic_issues:
                result["status"] = "SEM_ISSUES"
                result["success"] = True
                break

            # Final status after security
            final_status = _status_from_security(security_warnings)

            if security_warnings:
                logs.append(f"Security warnings remaining: {len(security_warnings)}")
            else:
                logs.append("No security warnings found.")

            result["status"] = final_status
            result["success"] = final_status in {"SUCCESS", "SUCCESS_WITH_WARNINGS"}
            break

        result["semantic_issues"] = semantic_issues
        result["security_warnings"] = security_warnings

    else:
        result["semantic_issues"] = []
        result["security_warnings"] = _collect_security_issues(working)
        result["success"] = False

    # ---------------------------------------------------------
    # Final payload
    # ---------------------------------------------------------
    changed_lines = _compute_changed_lines(original_source, working)

    result["corrected_code"] = working
    result["applied_steps"] = steps
    result["logs"] = logs
    result["errors"] = parse_errors
    result["changed_lines"] = changed_lines
    result["security_changed_lines"] = security_changed_lines
    result["stats"] = stats

    return result