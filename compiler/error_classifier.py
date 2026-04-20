from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ErrorClassification:
    fixable: bool
    category: str
    reason: str


def classify_error_message(msg: str) -> ErrorClassification:
    lower = (msg or "").lower().strip()

    # missing rhs
    if (
        "mismatched input ';' expecting" in lower
        and (
            "identifier" in lower
            or "integer" in lower
            or "float_literal" in lower
            or "char_literal" in lower
            or "string_literal" in lower
        )
    ):
        return ErrorClassification(True, "MISSING_OPERAND", "missing_rhs")

    # token families
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

    if "expecting '('" in lower and "main" in lower:
        return ErrorClassification(True, "MISSING_TOKEN", "main_lparen_expected")

    # comma heuristics from parser phrasing
    if "extraneous input" in lower and "expecting ')'" in lower:
        return ErrorClassification(True, "MISSING_TOKEN", "missing_comma_args")

    if "mismatched input 'int' expecting ')'" in lower:
        return ErrorClassification(True, "MISSING_TOKEN", "missing_comma_params")

    if "extraneous input 'int' expecting identifier" in lower:
        return ErrorClassification(True, "MISSING_TOKEN", "missing_comma_params")

    # generic extra token
    if "extraneous input" in lower:
        return ErrorClassification(True, "EXTRA_TOKEN", "extraneous_token")

    # lexer
    if "token recognition error" in lower:
        return ErrorClassification(True, "ILLEGAL_TOKEN", "illegal_token")

    # structural
    if "no viable alternative" in lower:
        return ErrorClassification(True, "STRUCTURAL_ERROR", "no_viable_alternative")

    if "mismatched input" in lower:
        return ErrorClassification(True, "MISMATCHED_TOKEN", "mismatched_token")

    if "input mismatch" in lower:
        return ErrorClassification(True, "MISMATCHED_TOKEN", "mismatched_token")

    if "failed predicate" in lower:
        return ErrorClassification(False, "PREDICATE_ERROR", "failed_predicate")

    if "unexpected token" in lower:
        return ErrorClassification(True, "STRUCTURAL_ERROR", "unexpected_token")

    return ErrorClassification(False, "STRUCTURAL_ERROR", "unknown")