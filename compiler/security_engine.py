from typing import List, Tuple, Dict

from compiler.security_checker import SecurityChecker
from compiler.taint_checker import TaintChecker
from compiler.string_flow_checker import StringFlowChecker


BLOCK_SEVERITIES = {"CRITICAL"}


class SecurityEngine:

    def __init__(self):
        self.security_checker = SecurityChecker()
        self.taint_checker = TaintChecker()
        self.string_flow_checker = StringFlowChecker()

    def analyze(self, source_text: str) -> Tuple[List[object], bool, Dict[str, List[object]]]:
        """
        Returns:
            issues: all issues
            blocked: whether compilation should be blocked
            categorized: { "CRITICAL": [...], "WARNING": [...], "INFO": [...] }
        """

        issues: List[object] = []

        # Run all checkers
        issues += self.security_checker.check(source_text)
        issues += self.taint_checker.check(source_text)
        issues += self.string_flow_checker.check(source_text)

        categorized = {
            "CRITICAL": [],
            "WARNING": [],
            "INFO": []
        }

        blocked = False

        # Categorize + policy decision
        for issue in issues:
            severity = getattr(issue, "severity", "INFO")

            if severity not in categorized:
                categorized["INFO"].append(issue)
            else:
                categorized[severity].append(issue)

            if severity in BLOCK_SEVERITIES:
                blocked = True

        return issues, blocked, categorized

    def print_summary(self, categorized):
        print("\n================ SECURITY ANALYSIS ================")

        for level in ["CRITICAL", "HIGH", "WARNING", "MEDIUM", "LOW", "INFO"]:
            items = categorized.get(level, [])
            if not items:
                continue

            print(f"\n[{level}] ({len(items)} issues)")
            print("-" * 50)

            for issue in items:
                message = getattr(issue, "message", str(issue))
                line = getattr(issue, "line", "?")
                suggestion = getattr(issue, "suggestion", None)

                print(f"Line {line}: {message}")
                if suggestion:
                    print(f"  Suggestion: {suggestion}")

        print("\n==================================================\n")