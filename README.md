# AI-Assisted C Syntax Error Corrector

An intelligent C compiler error-correction pipeline that combines deterministic rule-based
fixes with an optional fine-tuned **CodeT5 AI model** (via LoRA adapters) to automatically
repair syntax errors and flag security vulnerabilities in C code.

Built with a Flask **Server-Sent Events (SSE)** streaming backend and a Monaco Editor
frontend for live, step-by-step visualization of every repair.

---

## Key Features

- **Hybrid Deterministic + AI Architecture** — Rule-based fixes handle common, predictable
  errors (missing semicolons, mismatched braces, etc.). When rules fail, a fine-tuned
  CodeT5 model predicts precise Insert / Delete / Replace patch commands.
- **3-Phase Repair Pipeline**
  1. **Lexical** — Normalize Unicode punctuation, token misspellings, keyword typos
  2. **Syntax** — ANTLR4 parse → deterministic rules → AI patch fallback (iterative)
  3. **Security** — Regex-based static analysis for dangerous APIs, memory issues,
     hardcoded secrets, format-string vulnerabilities
- **Fine-Tuned LoRA Adapters** — Two separate adapters on `Salesforce/codet5-base`:
  - `codet5_patch_adapter` — syntax repair (Insert/Delete/Replace at line:col)
  - `codet5_security_adapter` — security vulnerability rewriting
- **Security Analysis** — The running GUI uses the local regex-based `SecurityChecker` for
  read-only warnings. The security adapter is a training asset, not part of the Flask path.
- **Real-Time SSE Streaming** — Every repair event (detect → fix → done) is streamed
  live to the frontend so you can watch the model think
- **Monaco Editor GUI** — Full-featured code editor with changed-line highlighting

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Parser | ANTLR4, antlr4-python3-runtime |
| AI | PyTorch, HuggingFace Transformers, PEFT (LoRA), CodeT5 |
| Frontend | HTML, Vanilla JS, Monaco Editor |

---

## Project Structure

```
Implementation/
├── app.py                        # Flask entry point — API routes + SSE
├── test_parser.py                # ANTLR4 parse driver + symbol builder
│
├── compiler/                     # Core pipeline
│   ├── lexical_corrector.py      # Phase 1: character + token + keyword normalization
│   ├── error_classifier.py       # Classifies ANTLR error messages into repair families
│   ├── error_corrector.py        # Phase 2a: deterministic rule-based fixes
│   ├── identifier_corrector.py   # Phase 2b: Damerau-Levenshtein symbol typo fix
│   ├── ai_error_corrector.py     # Phase 2c: CodeT5 patch candidate generation
│   ├── security_checker.py       # Phase 3: regex-based security static analysis
│   └── gui_bridge.py             # Glues the 3 phases, drives streaming output
│
├── grammar/
│   └── SimpleC.g4                # ANTLR4 grammar for the C subset
├── generated/                    # ANTLR4-generated lexer/parser/listener (Python)
│
├── gui/
│   ├── templates/index.html      # Single-page app shell
│   └── static/
│       ├── app.js                # SSE client + Monaco editor logic
│       └── style.css
│
├── ml/                           # Training pipeline
│   ├── cd-codet5.ipynb           # Jupyter notebook: full CodeT5 LoRA training proof
│   ├── train_codet5_lora.py      # Training script (CLI)
│   ├── dataset_loader.py         # JSONL dataset loader
│   ├── format_dataset.py         # Formats raw data into model input/target pairs
│   ├── predict_patch.py          # Inference: model → patch command
│   ├── apply_patch.py            # Applies patch command to source text
│   └── quick_infer_test.py       # Quick smoke-test for the loaded model
│
├── scripts/
│   ├── build_security_repair_dataset.py   # Generates security patch JSONL dataset
│   └── security-adapter-training.ipynb   # Jupyter notebook: security adapter training
│
├── tools/                        # Dataset engineering + audit scripts
│   ├── make_synthetic_dataset.py          # Generates syntax-error training corpus
│   ├── generate_seed_corpus.py            # Seed C programs for mutation
│   ├── audit_seed_programs.py             # Feature coverage audit on seed programs
│   ├── audit_synth_dataset.py             # Validates synthetic dataset quality
│   ├── check_duplicates.py                # Detects exact duplicate records
│   ├── check_split_leakage.py             # Checks train/val leakage
│   ├── check_pair_leakage_norm.py         # Normalised pair leakage check
│   ├── check_skeleton_diversity.py        # Structural diversity of programs
│   ├── check_patch_types.py               # Distribution of patch operation types
│   ├── check_program_length.py            # Token length statistics
│   ├── check_seed_lengths.py              # Seed program length audit
│   ├── dataset_uniqueness_audit.py        # Full uniqueness report
│   ├── inspect_seed_vs_dataset.py         # Seed overlap vs. dataset
│   ├── inspect_seed_vs_dataset_fuzzy.py   # Fuzzy version of above
│   ├── canonicalize_by_input.py           # Dedup by canonical input form
│   ├── find_clean_inputs.py               # Finds already-valid inputs
│   ├── make_dataset_from_logs.py          # Builds dataset from run logs
│   ├── make_ml_test_cases.py              # Generates ML evaluation test cases
│   ├── make_demo_long.py                  # Long-form demo examples
│   ├── manual_split_verify.py             # Manual split verification
│   ├── resplit_by_src_disjoint.py         # Re-splits ensuring source disjointness
│   ├── seed_shingle_overlap.py            # Shingle-based overlap detection
│   ├── split_dataset.py                   # Train/val split utility
│   ├── verify_seeds.py                    # Validates seed programs parse cleanly
│   └── write_manifest.py                  # Writes dataset manifest file
│
├── models/                       # Optional local LoRA adapter weights (not in repo)
│   ├── codet5_patch_adapter/     # Used by AI syntax-repair fallback
│   └── codet5_security_adapter/  # Optional training/inference asset
│
├── data/                         # Training datasets (JSONL)
└── examples/                     # Sample buggy .c files for the GUI
```

---

## Setup & Installation

### Prerequisites
- Python 3.9+
- Java (only needed if regenerating the ANTLR grammar)
- CUDA GPU (optional — CPU works, just slower for AI inference)

### 1. Install dependencies

```bash
python -m pip install flask torch transformers peft sentencepiece antlr4-python3-runtime
```

### 2. Configure the optional AI adapter

The web app can start without model files. Deterministic repairs and security checks work
without the adapter. To enable AI fallback, place the patch adapter at either:

```
models/codet5_patch_adapter/
models/codet5_patch_adapter/adapter/
```

You can use a different location with `CD_PATCH_ADAPTER_DIR`.

The base model, `Salesforce/codet5-base`, is downloaded from Hugging Face the first time
AI repair is needed. Set `HF_TOKEN` if authenticated Hub access is required.

If you need to retrain, see [`ml/cd-codet5.ipynb`](ml/cd-codet5.ipynb) for the full
training walkthrough.

---

## How to Run

### Run the web app

From the repository root (`Implementation/`):

```bash
python app.py
```

Open **http://127.0.0.1:5000** if the browser does not open automatically. Keep the
terminal running while using the app; press `Ctrl+C` to stop it.

- Pick an example from the sidebar, or type/paste any broken C code
- Click **Run Repair**
- Watch the SSE stream update each panel live: Repair Steps, Errors, Security Warnings

### Windows PowerShell

```powershell
cd "C:\Users\<your-user>\OneDrive\Desktop\CD project\Implementation"
python -m pip install flask torch transformers peft sentencepiece antlr4-python3-runtime
python app.py
```

### API endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/repair_stream` | POST | Streaming SSE repair (used by the GUI) |
| `/api/repair` | POST | Non-streaming repair, returns JSON |
| `/api/examples` | GET | List example `.c` files |
| `/api/example/<name>` | GET | Load a specific example file |

Request body for `/api/repair` and `/api/repair_stream`:
```json
{ "code": "<your C source>", "filename": "main.c" }
```

Example with PowerShell:

```powershell
$body = @{ code = "int main() { return 0; }"; filename = "main.c" } | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:5000/api/repair -Method Post -ContentType "application/json" -Body $body
```

### Smoke test

Run this from the repository root to verify the import path and repair endpoint without
starting a browser:

```bash
python -c "from app import app; response = app.test_client().post('/api/repair', json={'code': 'int main() { return 0; }', 'filename': 'main.c'}); print(response.status_code); print(response.get_json()['status'])"
```

---

## Dataset Pipeline (how the training data was built)

```
generate_seed_corpus.py        → seed C programs
    ↓
make_synthetic_dataset.py      → inject errors → (buggy, fixed) pairs
    ↓
tools/audit_*.py               → quality audits (duplicates, leakage, diversity)
    ↓
split_dataset.py               → train / val split
    ↓
ml/format_dataset.py           → format for CodeT5 input/target
    ↓
ml/train_codet5_lora.py        → fine-tune with LoRA
```

Security dataset follows the same flow starting from
`scripts/build_security_repair_dataset.py` with training proof in
`scripts/security-adapter-training.ipynb`.

## Notes

- AI model downloads can be large and require network access the first time they run.
- The generated ANTLR files under `generated/` are already included, so Java and the ANTLR
  tool are not needed for normal application use.
- Launch the Flask app from the repository root so relative paths to `examples/`, `models/`,
  and `generated/` resolve correctly.

---

*Created by Mahith Reddy Gangu*
