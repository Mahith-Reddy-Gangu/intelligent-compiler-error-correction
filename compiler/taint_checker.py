import re
from dataclasses import dataclass
from typing import List, Set


INPUT_APIS = [
    "scanf",
    "gets",
    "fgets",
]

ENV_APIS = [
    "getenv",
]

DANGEROUS_SINKS = [
    "system",
    "popen",
    "execl",
    "execv",
    "execvp",
    "execve",
    "WinExec",
    "ShellExecute",
    "CreateProcess",
]


@dataclass
class TaintIssue:
    severity: str
    message: str
    suggestion: str
    score: int


class TaintChecker:
    def check(self, source_text: str) -> List[TaintIssue]:
        issues: List[TaintIssue] = []
        tainted_vars: Set[str] = set()

        # scanf("%s", cmd) or scanf("%d", &x)
        scanf_matches = re.findall(
            r"\bscanf\s*\([^;]*,\s*&?([A-Za-z_]\w*)\s*\)",
            source_text,
        )
        tainted_vars.update(scanf_matches)

        # fgets(buf, ...)
        fgets_matches = re.findall(
            r"\bfgets\s*\(\s*([A-Za-z_]\w*)\s*,",
            source_text,
        )
        tainted_vars.update(fgets_matches)

        # gets(buf)
        gets_matches = re.findall(
            r"\bgets\s*\(\s*([A-Za-z_]\w*)\s*\)",
            source_text,
        )
        tainted_vars.update(gets_matches)

        # x = getenv(...)
        getenv_assign_matches = re.findall(
            r"\b([A-Za-z_]\w*)\s*=\s*getenv\s*\(",
            source_text,
        )
        tainted_vars.update(getenv_assign_matches)

        # argv usage is tainted
        if re.search(r"\bargv\b", source_text):
            tainted_vars.add("argv")

        # Simple assignment propagation: a = b;
        for _ in range(2):
            assign_matches = re.findall(
                r"\b([A-Za-z_]\w*)\s*=\s*([A-Za-z_]\w*(?:\[[^\]]+\])?)\s*;",
                source_text,
            )
            changed = False
            for lhs, rhs in assign_matches:
                rhs_base = rhs.split("[")[0]
                if rhs_base in tainted_vars and lhs not in tainted_vars:
                    tainted_vars.add(lhs)
                    changed = True
            if not changed:
                break

        # Tainted variable passed to dangerous sink
        for var in sorted(tainted_vars):
            for sink in DANGEROUS_SINKS:
                if re.search(
                    rf"\b{re.escape(sink)}\s*\(\s*{re.escape(var)}(?:\[[^\]]+\])?\b",
                    source_text,
                ):
                    issues.append(
                        TaintIssue(
                            severity="CRITICAL",
                            message=f"Tainted input '{var}' passed to dangerous sink '{sink}'",
                            suggestion="Sanitize or validate the input before use, or avoid passing external input to command-execution APIs.",
                            score=5,
                        )
                    )

        # Direct argv[i] to sink
        for sink in DANGEROUS_SINKS:
            if re.search(rf"\b{re.escape(sink)}\s*\(\s*argv\s*\[", source_text):
                issues.append(
                    TaintIssue(
                        severity="CRITICAL",
                        message=f"Command-line argument passed directly to dangerous sink '{sink}'",
                        suggestion="Copy argv input into a validated buffer and strictly sanitize it before command execution.",
                        score=5,
                    )
                )

        # Direct getenv(...) to sink
        for sink in DANGEROUS_SINKS:
            if re.search(rf"\b{re.escape(sink)}\s*\(\s*getenv\s*\(", source_text):
                issues.append(
                    TaintIssue(
                        severity="CRITICAL",
                        message=f"Environment-derived value passed directly to dangerous sink '{sink}'",
                        suggestion="Do not directly execute environment-derived content; validate against an allowlist first.",
                        score=5,
                    )
                )

        return issues