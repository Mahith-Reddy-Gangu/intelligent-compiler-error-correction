import os
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    from peft import PeftModel
except Exception:
    torch = None
    AutoTokenizer = None
    AutoModelForSeq2SeqLM = None
    PeftModel = None


@dataclass
class AutoFixResult:
    source: str
    applied_steps: List[str]


class SecurityAutoFixer:
    """
    Hybrid security auto-fixer.

    Design:
      1. Runs ONLY after security warnings are already detected by SecurityEngine.
      2. Uses the trained security LoRA adapter for supported local one-line repairs.
      3. Falls back to deterministic safe rewrites if the model is unavailable
         or returns an invalid patch.
      4. Never attempts deep semantic or dangerous automatic rewrites.

    We do NOT auto-fix:
      - tainted system()/exec() flows
      - hardcoded secrets
      - path traversal
      - memory ownership/lifetime issues
      - anything requiring deep semantic reasoning
    """

    MODEL_NAME = "Salesforce/codet5-base"
    ADAPTER_PATH = os.path.join("models", "codet5_security_adapter", "adapter")

    def __init__(self):
        self._tokenizer = None
        self._model = None
        self._device = None
        self._model_load_attempted = False

    # ------------------------------------------------------------------
    # Public entrypoint
    # ------------------------------------------------------------------
    def apply_fixes(self, source: str) -> AutoFixResult:
        fixed = source
        steps: List[str] = []

        # 1) AI-backed repairs for families the adapter was trained on
        fixed, ai_steps = self._apply_ai_security_fixes(fixed)
        steps.extend(ai_steps)

        # 2) Deterministic fallback / extra local safe rewrites
        #    Keep these because they are useful even beyond the trained set.
        fixed, det_steps = self._apply_deterministic_fixes(fixed)
        steps.extend(det_steps)

        return AutoFixResult(source=fixed, applied_steps=steps)

    # ------------------------------------------------------------------
    # AI-backed fixing
    # ------------------------------------------------------------------
    def _apply_ai_security_fixes(self, source: str) -> Tuple[str, List[str]]:
        """
        Apply line-local AI repairs for categories that the adapter was trained on:
          - gets(...)                -> fgets(..., sizeof(...), stdin)
          - strcpy(dst, src)         -> snprintf(dst, sizeof(dst), "%s", src)
          - strcat(dst, src)         -> strncat(dst, src, sizeof(dst) - strlen(dst) - 1)
          - sprintf(buf, ...)        -> snprintf(buf, sizeof(buf), ...)
          - scanf("%s", buf)         -> scanf("%Ns", buf)

        The model expects the FULL source plus CATEGORY and LINE.
        """
        model_bundle = self._load_security_model()
        if model_bundle is None:
            return source, []

        fixed = source
        steps: List[str] = []

        # We repeatedly scan the current source so line numbers remain accurate
        # after each accepted patch.
        candidates = self._find_ai_fix_candidates(fixed)

        for line_no, category in candidates:
            patch = self._generate_patch(fixed, line_no, category)
            if patch is None:
                continue

            new_fixed = self._apply_replace_line_patch(fixed, patch)
            if new_fixed is None or new_fixed == fixed:
                continue

            fixed = new_fixed
            steps.append(f"AISEC: {category} at line {line_no} -> {patch}")

        return fixed, steps

    def _find_ai_fix_candidates(self, source: str) -> List[Tuple[int, str]]:
        """
        Returns a list of (1-based line number, category) pairs.
        Only returns patterns the trained adapter knows.
        """
        candidates: List[Tuple[int, str]] = []
        lines = source.splitlines()

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            if not stripped:
                continue

            # gets(buf)
            if re.search(r"\bgets\s*\(\s*[A-Za-z_]\w*\s*\)", stripped):
                candidates.append((idx, "UNSAFE_INPUT"))
                continue

            # strcpy(dst, src)
            if re.search(
                r"\bstrcpy\s*\(\s*[A-Za-z_]\w*\s*,\s*[A-Za-z_]\w*\s*\)",
                stripped,
            ):
                candidates.append((idx, "UNBOUNDED_COPY"))
                continue

            # strcat(dst, src)
            if re.search(
                r"\bstrcat\s*\(\s*[A-Za-z_]\w*\s*,\s*[A-Za-z_]\w*\s*\)",
                stripped,
            ):
                candidates.append((idx, "UNBOUNDED_CONCAT"))
                continue

            # sprintf(buf, ...)
            if re.search(r"\bsprintf\s*\(\s*[A-Za-z_]\w*\s*,", stripped):
                candidates.append((idx, "UNBOUNDED_FORMAT"))
                continue

            # scanf("%s", buf)
            if re.search(
                r'\bscanf\s*\(\s*"%s"\s*,\s*[A-Za-z_]\w*\s*\)',
                stripped,
            ):
                candidates.append((idx, "UNBOUNDED_INPUT"))
                continue

        return candidates

    def _load_security_model(self):
        """
        Lazy-load tokenizer + base model + LoRA adapter.
        Returns None if unavailable, so deterministic fallback can still work.
        """
        if self._tokenizer is not None and self._model is not None:
            return self._tokenizer, self._model

        if self._model_load_attempted:
            return None

        self._model_load_attempted = True

        if (
            torch is None
            or AutoTokenizer is None
            or AutoModelForSeq2SeqLM is None
            or PeftModel is None
        ):
            return None

        if not os.path.isdir(self.ADAPTER_PATH):
            return None

        try:
            self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

            self._tokenizer = AutoTokenizer.from_pretrained(self.ADAPTER_PATH)

            base_model = AutoModelForSeq2SeqLM.from_pretrained(self.MODEL_NAME)
            self._model = PeftModel.from_pretrained(base_model, self.ADAPTER_PATH)
            self._model.to(self._device)
            self._model.eval()

            return self._tokenizer, self._model

        except Exception:
            self._tokenizer = None
            self._model = None
            return None

    def _build_model_input(self, source: str, line_no: int, category: str) -> str:
        return (
            f"SECURITY_FIX\n"
            f"CATEGORY {category}\n"
            f"LINE {line_no}\n\n"
            f"<CODE>\n{source}\n</CODE>"
        )

    def _generate_patch(self, source: str, line_no: int, category: str) -> Optional[str]:
        bundle = self._load_security_model()
        if bundle is None:
            return None

        tokenizer, model = bundle
        prompt = self._build_model_input(source, line_no, category)

        try:
            inputs = tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=256,
            )

            if self._device is not None:
                inputs = {k: v.to(self._device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_length=64,
                    num_beams=1,
                )

            pred = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
            if not pred.startswith("REPLACE_LINE"):
                return None

            return pred

        except Exception:
            return None

    def _apply_replace_line_patch(self, source: str, patch: str) -> Optional[str]:
        """
        Patch format:
          REPLACE_LINE <line_no> <new line text>
        """
        m = re.match(r"^REPLACE_LINE\s+(\d+)\s+(.*)$", patch.strip())
        if not m:
            return None

        line_no = int(m.group(1))
        new_line = m.group(2)

        lines = source.splitlines()
        if line_no < 1 or line_no > len(lines):
            return None

        old_line = lines[line_no - 1]

        # Preserve original indentation if the model emitted a normalized line.
        old_indent_match = re.match(r"^(\s*)", old_line)
        old_indent = old_indent_match.group(1) if old_indent_match else ""

        if new_line and not new_line.startswith((" ", "\t")):
            new_line = old_indent + new_line

        if new_line == old_line:
            return None

        lines[line_no - 1] = new_line
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Deterministic fallback / additional safe rewrites
    # ------------------------------------------------------------------
    def _apply_deterministic_fixes(self, source: str) -> Tuple[str, List[str]]:
        fixed = source
        steps: List[str] = []

        # gets(buf) -> fgets(buf, sizeof(buf), stdin)
        pattern = re.compile(r"\bgets\s*\(\s*([A-Za-z_]\w*)\s*\)")
        new_fixed = pattern.sub(r"fgets(\1, sizeof(\1), stdin)", fixed)
        if new_fixed != fixed:
            fixed = new_fixed
            steps.append("AUTOSEC: gets -> fgets(buffer, sizeof(buffer), stdin)")

        # strcpy(dst, src) -> strncpy(dst, src, sizeof(dst))
        pattern = re.compile(
            r"\bstrcpy\s*\(\s*([A-Za-z_]\w*)\s*,\s*([A-Za-z_]\w*)\s*\)"
        )
        new_fixed = pattern.sub(r"strncpy(\1, \2, sizeof(\1))", fixed)
        if new_fixed != fixed:
            fixed = new_fixed
            steps.append("AUTOSEC: strcpy -> strncpy(dst, src, sizeof(dst))")

        # strcat(dst, src) -> strncat(dst, src, sizeof(dst))
        pattern = re.compile(
            r"\bstrcat\s*\(\s*([A-Za-z_]\w*)\s*,\s*([A-Za-z_]\w*)\s*\)"
        )
        new_fixed = pattern.sub(r"strncat(\1, \2, sizeof(\1))", fixed)
        if new_fixed != fixed:
            fixed = new_fixed
            steps.append("AUTOSEC: strcat -> strncat(dst, src, sizeof(dst))")

        # sprintf(buf, ...) -> snprintf(buf, sizeof(buf), ...)
        pattern = re.compile(r"\bsprintf\s*\(\s*([A-Za-z_]\w*)\s*,")
        new_fixed = pattern.sub(r"snprintf(\1, sizeof(\1),", fixed)
        if new_fixed != fixed:
            fixed = new_fixed
            steps.append("AUTOSEC: sprintf -> snprintf(buf, sizeof(buf), ...)")

        # vsprintf(buf, ...) -> vsnprintf(buf, sizeof(buf), ...)
        pattern = re.compile(r"\bvsprintf\s*\(\s*([A-Za-z_]\w*)\s*,")
        new_fixed = pattern.sub(r"vsnprintf(\1, sizeof(\1),", fixed)
        if new_fixed != fixed:
            fixed = new_fixed
            steps.append("AUTOSEC: vsprintf -> vsnprintf(buf, sizeof(buf), ...)")

        # printf(user_input) -> printf("%s", user_input)
        pattern = re.compile(r"\bprintf\s*\(\s*([A-Za-z_]\w*)\s*\)")
        new_fixed = pattern.sub(r'printf("%s", \1)', fixed)
        if new_fixed != fixed:
            fixed = new_fixed
            steps.append('AUTOSEC: printf(var) -> printf("%s", var)')

        # scanf("%s", buf) -> scanf("%99s", buf)
        pattern = re.compile(
            r'\bscanf\s*\(\s*"%s"\s*,\s*([A-Za-z_]\w*)\s*\)'
        )
        new_fixed = pattern.sub(r'scanf("%99s", \1)', fixed)
        if new_fixed != fixed:
            fixed = new_fixed
            steps.append('AUTOSEC: scanf("%s", buf) -> scanf("%99s", buf)')

        return fixed, steps