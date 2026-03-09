from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ErrorClassification:
    fixable: bool
    category: str
    reason: str


def classify_error_message(msg: str) -> ErrorClassification:
    """
    Classify ANTLR lexer/parser error messages into coarse repair categories.

    IMPORTANT MEANING OF "fixable" HERE:
    - True does NOT mean deterministic rule always exists.
    - True means the pipeline should attempt repair
      (deterministic and/or AI).
    - False means very low-confidence / unknown case.

    This works better with the hybrid pipeline:
      lexical cleanup -> deterministic syntax fix -> AI fallback.
    """
    lower = (msg or "").lower().strip()

    # ---------------------------------------------------------
    # Missing tokens (good deterministic candidates)
    # ---------------------------------------------------------
    if re.search(r"missing\s+';'", lower) or re.search(r"expecting\s+';'", lower):
        return ErrorClassification(True, "MISSING_TOKEN", "missing_semicolon")

    if re.search(r"missing\s+'\}'", lower) or re.search(r"expecting\s+'\}'", lower):
        return ErrorClassification(True, "MISSING_TOKEN", "missing_rbrace")

    if re.search(r"missing\s+'\{'", lower) or re.search(r"expecting\s+'\{'", lower):
        return ErrorClassification(True, "MISSING_TOKEN", "missing_lbrace")

    if re.search(r"missing\s+'\)'", lower) or re.search(r"expecting\s+'\)'", lower):
        return ErrorClassification(True, "MISSING_TOKEN", "missing_rparen")

    if re.search(r"missing\s+'\('", lower) or re.search(r"expecting\s+'\('", lower):
        return ErrorClassification(True, "MISSING_TOKEN", "missing_lparen")

    # Special legacy/main-header style message support
    if "expecting '('" in lower and "main" in lower:
        return ErrorClassification(True, "MISSING_TOKEN", "main_lparen_expected")

    # ---------------------------------------------------------
    # Extra token
    # ---------------------------------------------------------
    if "extraneous input" in lower:
        return ErrorClassification(True, "EXTRA_TOKEN", "extraneous_token")

    # ---------------------------------------------------------
    # Lexer-level illegal token
    # Let AI attempt these after lexical cleanup fails.
    # ---------------------------------------------------------
    if "token recognition error" in lower:
        return ErrorClassification(True, "ILLEGAL_TOKEN", "illegal_token")

    # ---------------------------------------------------------
    # Broader structural parse failures
    # Deterministic rules may not help, but AI should still try.
    # ---------------------------------------------------------
    if "no viable alternative" in lower:
        return ErrorClassification(True, "STRUCTURAL_ERROR", "no_viable_alternative")

    if "mismatched input" in lower:
        return ErrorClassification(True, "MISMATCHED_TOKEN", "mismatched_token")

    # Some ANTLR variants use phrasing like:
    # "input mismatch" / "failed predicate" / etc.
    if "input mismatch" in lower:
        return ErrorClassification(True, "MISMATCHED_TOKEN", "mismatched_token")

    if "failed predicate" in lower:
        return ErrorClassification(False, "PREDICATE_ERROR", "failed_predicate")

    if "unexpected token" in lower:
        return ErrorClassification(True, "STRUCTURAL_ERROR", "unexpected_token")

    # ---------------------------------------------------------
    # Fallback unknown
    # ---------------------------------------------------------
    return ErrorClassification(False, "STRUCTURAL_ERROR", "unknown")