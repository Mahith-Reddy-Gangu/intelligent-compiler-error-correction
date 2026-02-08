from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorClassification:
    fixable: bool
    category: str
    reason: str


def classify_error_message(msg: str) -> ErrorClassification:
    lower = msg.lower()

    if "missing ';'" in lower or "expecting ';'" in lower:
        return ErrorClassification(True, "MISSING_TOKEN", "missing_semicolon")

    if "expecting '}'" in lower or "missing '}'" in lower:
        return ErrorClassification(True, "MISSING_TOKEN", "missing_rbrace")

    if "mismatched input '{'" in lower and "expecting '('" in lower:
        return ErrorClassification(True, "MISMATCHED_TOKEN", "main_lparen_expected")

    if "token recognition error" in lower or "extraneous input" in lower:
        return ErrorClassification(False, "ILLEGAL_TOKEN", "illegal_token")

    if "no viable alternative" in lower:
        return ErrorClassification(False, "STRUCTURAL_ERROR", "no_viable_alternative")

    if "mismatched input" in lower:
        return ErrorClassification(False, "MISMATCHED_TOKEN", "mismatched_token")

    return ErrorClassification(False, "STRUCTURAL_ERROR", "unknown")
