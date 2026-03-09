import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class StringFlowIssue:
    severity: str
    message: str
    score: int


class StringFlowChecker:
    def check(self, source_text: str) -> List[StringFlowIssue]:
        issues: List[StringFlowIssue] = []

        # Heuristic: command construction before dangerous sink
        if re.search(r"\bsprintf\s*\(", source_text) and re.search(r"\bsystem\s*\(", source_text):
            issues.append(
                StringFlowIssue(
                    severity="HIGH",
                    message="Heuristic warning: command string may be constructed via sprintf before system() call",
                    score=3,
                )
            )

        if re.search(r"\bstrcat\s*\(", source_text) and re.search(r"\bsystem\s*\(", source_text):
            issues.append(
                StringFlowIssue(
                    severity="HIGH",
                    message="Heuristic warning: command string may be constructed via strcat before system() call",
                    score=3,
                )
            )

        if re.search(r"\bstrcpy\s*\(", source_text) and re.search(r"\bsystem\s*\(", source_text):
            issues.append(
                StringFlowIssue(
                    severity="HIGH",
                    message="Heuristic warning: command string may be copied via strcpy before system() call",
                    score=3,
                )
            )

        # Constant string reconstruction for simple char arrays / pointers
        string_values: Dict[str, str] = {}

        # char a[] = "rm";
        literal_assigns = re.findall(
            r'\bchar\s+\*?\s*([A-Za-z_]\w*)\s*(?:\[[^\]]*\])?\s*=\s*"([^"]*)"\s*;',
            source_text,
        )
        for name, value in literal_assigns:
            string_values[name] = value

        # Simple sprintf(cmd,"%s%s%s",a,b,c)
        sprintf_matches = re.findall(
            r'\bsprintf\s*\(\s*([A-Za-z_]\w*)\s*,\s*"([^"]*)"\s*,\s*([A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*)\s*\)',
            source_text,
        )
        for dest, fmt, args_blob in sprintf_matches:
            if "%s" in fmt:
                args = [a.strip() for a in args_blob.split(",")]
                pieces: List[str] = []
                resolvable = True
                for arg in args:
                    if arg in string_values:
                        pieces.append(string_values[arg])
                    else:
                        resolvable = False
                        break
                if resolvable:
                    string_values[dest] = "".join(pieces)

        # Simple strcat(cmd, a)
        strcat_matches = re.findall(
            r'\bstrcat\s*\(\s*([A-Za-z_]\w*)\s*,\s*([A-Za-z_]\w*)\s*\)',
            source_text,
        )
        for dest, src in strcat_matches:
            if dest in string_values and src in string_values:
                string_values[dest] = string_values[dest] + string_values[src]

        # strcpy(cmd, a)
        strcpy_matches = re.findall(
            r'\bstrcpy\s*\(\s*([A-Za-z_]\w*)\s*,\s*([A-Za-z_]\w*)\s*\)',
            source_text,
        )
        for dest, src in strcpy_matches:
            if src in string_values:
                string_values[dest] = string_values[src]

        # If reconstructed variable is passed to system/popen, inspect content
        for sink in ["system", "popen", "WinExec", "ShellExecute", "CreateProcess"]:
            sink_var_matches = re.findall(
                rf"\b{re.escape(sink)}\s*\(\s*([A-Za-z_]\w*)\s*[,\)]",
                source_text,
            )
            for var in sink_var_matches:
                val = string_values.get(var)
                if not val:
                    continue

                lowered = val.lower()
                if "rm -rf /" in lowered or "del /s /q" in lowered or "rmdir /s /q" in lowered:
                    issues.append(
                        StringFlowIssue(
                            severity="CRITICAL",
                            message=f"Reconstructed dangerous command '{val}' passed to '{sink}' via variable '{var}'",
                            score=5,
                        )
                    )
                elif "powershell" in lowered or "curl " in lowered or "wget " in lowered:
                    issues.append(
                        StringFlowIssue(
                            severity="HIGH",
                            message=f"Reconstructed suspicious command '{val}' passed to '{sink}' via variable '{var}'",
                            score=4,
                        )
                    )

        return issues