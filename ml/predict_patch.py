import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from peft import PeftModel

BASE_MODEL_NAME = "Salesforce/codet5-base"
ADAPTER_DIR = os.getenv("CD_PATCH_ADAPTER_DIR", "models/adapter_v2")

MAX_SOURCE_LEN = 256
MAX_NEW_TOKENS = 16


class PatchPredictor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if not os.path.isdir(ADAPTER_DIR):
            raise FileNotFoundError(
                f"Adapter folder not found at '{ADAPTER_DIR}'. "
                f"Set env CD_PATCH_ADAPTER_DIR or place adapter at models/adapter_v2."
            )

        self.tokenizer = AutoTokenizer.from_pretrained(ADAPTER_DIR)
        base = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL_NAME)
        self.model = PeftModel.from_pretrained(base, ADAPTER_DIR)

        self.model.to(self.device)
        self.model.eval()

    def predict_patch_cmd(self, prompt: str) -> str:
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=MAX_SOURCE_LEN,
        ).to(self.device)

        with torch.no_grad():
            out = self.model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                num_beams=1,
                do_sample=False,
                early_stopping=True,
            )

        return self.tokenizer.decode(out[0], skip_special_tokens=True).strip()