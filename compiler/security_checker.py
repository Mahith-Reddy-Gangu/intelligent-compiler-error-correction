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
    suggestion: str
    score: int


class SecurityChecker:

    def check(self, source_text: str) -> List[SecurityIssue]:

        issues: List[SecurityIssue] = []

        # ------------------------------------------------
        # Dangerous APIs
        # ------------------------------------------------
        for fn, desc in DANGEROUS_FUNCTIONS.items():

            call_pattern = rf"\b{re.escape(fn)}\s*\((.*?)\)"
            matches = re.finditer(call_pattern, source_text, flags=re.DOTALL)

            for m in matches:
                arg_text = m.group(1).strip()

                if re.fullmatch(r'"[^"\n]*"', arg_text):
                    issues.append(
                        SecurityIssue(
                            severity="WARNING",
                            message=f"Dangerous API used with constant string: {fn} ({desc})",
                            suggestion="Avoid command execution APIs unless absolutely necessary.",
                            score=2,
                        )
                    )
                else:
                    issues.append(
                        SecurityIssue(
                            severity="WARNING",
                            message=f"Dangerous API used with non-constant input: {fn} ({desc})",
                            suggestion="Sanitize and validate input before passing it to command execution APIs.",
                            score=3,
                        )
                    )

        # ------------------------------------------------
        # Unsafe C functions
        # ------------------------------------------------
        for fn, desc in UNSAFE_FUNCTIONS.items():

            if re.search(rf"\b{re.escape(fn)}\s*\(", source_text):

                if fn == "gets":
                    issues.append(
                        SecurityIssue(
                            severity="CRITICAL",
                            message=f"Unsafe function detected: {fn} ({desc})",
                            suggestion="Replace gets with fgets.",
                            score=5,
                        )
                    )
                else:
                    issues.append(
                        SecurityIssue(
                            severity="WARNING",
                            message=f"Unsafe function detected: {fn} ({desc})",
                            suggestion="Use safer alternatives.",
                            score=2,
                        )
                    )

        # ------------------------------------------------
        # Dangerous command patterns
        # ------------------------------------------------
        for pattern in DANGEROUS_COMMAND_PATTERNS:

            if re.search(pattern, source_text, flags=re.IGNORECASE):

                issues.append(
                    SecurityIssue(
                        severity="CRITICAL",
                        message=f"Dangerous command pattern detected: {pattern}",
                        suggestion="Remove destructive command usage.",
                        score=5,
                    )
                )

        # ------------------------------------------------
        # Sensitive path references
        # ------------------------------------------------
        for pattern in SENSITIVE_PATH_PATTERNS:

            if re.search(pattern, source_text, flags=re.IGNORECASE):

                issues.append(
                    SecurityIssue(
                        severity="HIGH",
                        message=f"Sensitive system path referenced: {pattern}",
                        suggestion="Avoid accessing sensitive directories.",
                        score=3,
                    )
                )

        # ------------------------------------------------
        # Path traversal
        # ------------------------------------------------
        if re.search(r"\.\./", source_text):
            issues.append(
                SecurityIssue(
                    severity="HIGH",
                    message="Potential path traversal detected (../)",
                    suggestion="Sanitize file paths.",
                    score=3,
                )
            )

        # ------------------------------------------------
        # Dangerous macros
        # ------------------------------------------------
        for pattern in DANGEROUS_MACRO_PATTERNS:

            if re.search(pattern, source_text, flags=re.IGNORECASE):

                issues.append(
                    SecurityIssue(
                        severity="HIGH",
                        message="Dangerous macro detected",
                        suggestion="Avoid embedding commands in macros.",
                        score=4,
                    )
                )

        # ------------------------------------------------
        # Hardcoded secrets
        # ------------------------------------------------
        secret_patterns = [
            r"(password|passwd|pwd)\s*=\s*\".*\"",
            r"(password|passwd|pwd)\s*=\s*\d+",
            r"(api_key|apikey|token|secret)\s*=\s*\".*\"",
            r"(api_key|apikey|token|secret)\s*=\s*\d+",
        ]

        for pattern in secret_patterns:
            if re.search(pattern, source_text, flags=re.IGNORECASE):
                issues.append(
                    SecurityIssue(
                        severity="HIGH",
                        message="Hardcoded secret detected",
                        suggestion="Store secrets securely (env/config).",
                        score=4,
                    )
                )

        # ------------------------------------------------
        # Memory allocation tracking
        # ------------------------------------------------
        malloc_vars = re.findall(
            r"\b([A-Za-z_]\w*)\s*=\s*(malloc|calloc|realloc)\s*\(",
            source_text,
        )

        for var, _ in malloc_vars:
            if not re.search(rf"\bfree\s*\(\s*{var}\s*\)", source_text):
                issues.append(
                    SecurityIssue(
                        severity="WARNING",
                        message=f"Possible memory leak: '{var}' allocated but not freed",
                        suggestion="Ensure free() is called.",
                        score=3,
                    )
                )

        # ------------------------------------------------
        # Double free
        # ------------------------------------------------
        free_matches = re.findall(
            r"\bfree\s*\(\s*([A-Za-z_]\w*)\s*\)",
            source_text,
        )

        for var in set(free_matches):
            if free_matches.count(var) > 1:
                issues.append(
                    SecurityIssue(
                        severity="CRITICAL",
                        message=f"Double free detected on '{var}'",
                        suggestion="Avoid freeing memory multiple times.",
                        score=5,
                    )
                )

        # ------------------------------------------------
        # Use-after-free (heuristic)
        # ------------------------------------------------
        for var in set(free_matches):
            if re.search(rf"\bfree\s*\(\s*{var}\s*\).*{var}", source_text, flags=re.DOTALL):
                issues.append(
                    SecurityIssue(
                        severity="CRITICAL",
                        message=f"Possible use-after-free of '{var}'",
                        suggestion="Do not use memory after free().",
                        score=5,
                    )
                )

        # ------------------------------------------------
        # Format string vulnerability
        # printf(user_input)
        # ------------------------------------------------
        format_string_matches = re.findall(
            r"\bprintf\s*\(\s*([A-Za-z_]\w*)\s*\)",
            source_text,
        )

        for var in format_string_matches:
            issues.append(
                SecurityIssue(
                    severity="WARNING",
                    message=f"Potential format string vulnerability using variable '{var}'",
                    suggestion='Use printf("%s", variable) instead of printf(variable).',
                    score=3,
                )
            )

        return issues