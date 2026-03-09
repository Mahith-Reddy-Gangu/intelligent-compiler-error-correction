import re
from dataclasses import dataclass
from typing import List


DANGEROUS_FUNCTIONS = {
    "system": "Executes shell command",
    "popen": "Opens process pipe",
    "execl": "Exec family process execution",
    "execv": "Exec family process execution",
    "execvp": "Exec family process execution",
    "execve": "Exec family process execution",
    "WinExec": "Windows command execution",
    "ShellExecute": "Windows shell execution",
    "CreateProcess": "Windows process creation",
}

UNSAFE_FUNCTIONS = {
    "gets": "Unsafe input function",
    "strcpy": "Unsafe string copy",
    "strcat": "Unsafe string concatenation",
    "sprintf": "Unsafe string formatting",
    "vsprintf": "Unsafe variadic string formatting",
}

DANGEROUS_COMMAND_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"del\s+/s\s+/q",
    r"rmdir\s+/s\s+/q",
    r"powershell",
    r"cmd\.exe",
    r"wget\s+",
    r"curl\s+",
    r"shutdown\s+",
    r"format\s+[A-Za-z]:",
]

SENSITIVE_PATH_PATTERNS = [
    r"C:\\Windows",
    r"C:\\System32",
    r"/etc/",
    r"/bin/",
    r"/usr/bin/",
]

DANGEROUS_MACRO_PATTERNS = [
    r"#define\s+\w+\s+\".*rm\s+-rf\s+/.*\"",
    r"#define\s+\w+\s+\".*del\s+/s\s+/q.*\"",
    r"#define\s+\w+\s+\".*powershell.*\"",
]


@dataclass
class SecurityIssue:
    severity: str
    message: str
    score: int


class SecurityChecker:
    def check(self, source_text: str) -> List[SecurityIssue]:
        issues: List[SecurityIssue] = []

        # Dangerous APIs
        for fn, desc in DANGEROUS_FUNCTIONS.items():
            if re.search(rf"\b{re.escape(fn)}\s*\(", source_text):
                issues.append(
                    SecurityIssue(
                        severity="HIGH",
                        message=f"Dangerous API used: {fn} ({desc})",
                        score=4,
                    )
                )

        # Unsafe C functions
        for fn, desc in UNSAFE_FUNCTIONS.items():
            if re.search(rf"\b{re.escape(fn)}\s*\(", source_text):
                issues.append(
                    SecurityIssue(
                        severity="LOW",
                        message=f"Unsafe function detected: {fn} ({desc})",
                        score=1,
                    )
                )

        # Dangerous command strings
        for pattern in DANGEROUS_COMMAND_PATTERNS:
            if re.search(pattern, source_text, flags=re.IGNORECASE):
                issues.append(
                    SecurityIssue(
                        severity="CRITICAL",
                        message=f"Dangerous command pattern detected: {pattern}",
                        score=5,
                    )
                )

        # Sensitive paths
        for pattern in SENSITIVE_PATH_PATTERNS:
            if re.search(pattern, source_text, flags=re.IGNORECASE):
                issues.append(
                    SecurityIssue(
                        severity="HIGH",
                        message=f"Sensitive system path referenced: {pattern}",
                        score=3,
                    )
                )

        # Dangerous macro definitions
        for pattern in DANGEROUS_MACRO_PATTERNS:
            if re.search(pattern, source_text, flags=re.IGNORECASE):
                issues.append(
                    SecurityIssue(
                        severity="HIGH",
                        message="Dangerous macro definition detected",
                        score=4,
                    )
                )

        # Helper-function call into dangerous sink
        sink_call_with_fn = re.findall(
            r"\b(system|popen|execl|execv|execvp|execve|WinExec|ShellExecute|CreateProcess)\s*\(\s*([A-Za-z_]\w*)\s*\(",
            source_text,
        )
        for sink, helper in sink_call_with_fn:
            issues.append(
                SecurityIssue(
                    severity="HIGH",
                    message=f"Dangerous sink '{sink}' called with helper function '{helper}(...)'",
                    score=4,
                )
            )

        # Unresolved variable/expression passed to dangerous sink
        unresolved_sink_args = re.findall(
            r"\b(system|popen|execl|execv|execvp|execve|WinExec|ShellExecute|CreateProcess)\s*\(\s*([A-Za-z_]\w*(?:\[[^\]]+\])?)\s*[,\)]",
            source_text,
        )
        for sink, arg in unresolved_sink_args:
            # Skip obvious string literals; this regex only catches vars, so fine.
            issues.append(
                SecurityIssue(
                    severity="HIGH",
                    message=f"Unresolved argument '{arg}' passed to dangerous sink '{sink}'",
                    score=4,
                )
            )

        # Infinite-loop / DoS heuristics
        if re.search(r"\bwhile\s*\(\s*1\s*\)\s*\{", source_text):
            issues.append(
                SecurityIssue(
                    severity="LOW",
                    message="Potential infinite loop detected: while(1){...}",
                    score=2,
                )
            )

        if re.search(r"\bfor\s*\(\s*;\s*;\s*\)\s*\{", source_text):
            issues.append(
                SecurityIssue(
                    severity="LOW",
                    message="Potential infinite loop detected: for(;;){...}",
                    score=2,
                )
            )

        return issues