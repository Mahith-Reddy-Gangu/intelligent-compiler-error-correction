# AI-Augmented C-Compiler with Real-Time Vulnerability Auto-Fixing

An intelligent compiler pipeline that blends traditional deterministic parsing (ANTLR-based AST manipulation) with a cutting-edge **Dual-LoRA AI fallback** to autonomously repair unrecoverable syntax and logic errors in C code. 

Built with a high-performance Flask **Server-Sent Events (SSE)** streaming backend, this project provides a live, iteration-by-iteration visualization of the compilation and repair process. It also features a multi-stage security analysis pipeline to track taint flows and a custom **Green Computing Profiler** to evaluate algorithmic energy efficiency.

---

## 🚀 Key Features

* **Hybrid Deterministic-AI Architecture:** Utilizes robust AST-based semantic and lexical rules for immediate corrections. When deterministic methods fail, it falls back to an AI agent for context-aware mutation patches.
* **Dual-LoRA Model Engineering:** Uses HuggingFace PEFT (Parameter-Efficient Fine-Tuning) on `Salesforce/codet5-base`. 
  * **Adapter 1 (`codet5_patch_adapter`):** Predicts precise line-column offset operations (Insert/Delete/Replace) for syntax trees.
  * **Adapter 2 (`codet5_security_adapter`):** Dedicated entirely to rewriting and remediating security vulnerabilities.
* **Real-Time SSE Streaming Backend:** Features a highly responsive Flask backend that uses Server-Sent Events to stream live AI "thoughts" and code mutations directly to the frontend GUI.
* **Static Analysis & Taint Tracking:** Proactively detects format string vulnerabilities, buffer overflow risks, and untrusted taint flows. It dynamically computes threat scores and blocks insecure execution.
* **Green Computing Profiler:** A custom runtime tracking system (`GreenMetrics`) that evaluates AI vs. Deterministic resource overhead, generates an algorithmic "Green Score," and pinpoints phase-level execution bottlenecks.

---

## 🛠️ Tech Stack

* **Backend / Compiler:** Python 3, ANTLR4
* **AI / Machine Learning:** PyTorch, Transformers (HuggingFace), PEFT (LoRA), CodeT5
* **Web Integration:** Flask, Server-Sent Events (SSE)
* **Frontend:** HTML, CSS, Vanilla JS, Monaco Editor
* **Profiling:** CodeCarbon (Energy Tracking), Custom Python Profilers

---

## ⚙️ Installation & Setup

### Prerequisites
Make sure you have Python 3.9+ installed and a CUDA-capable GPU (optional, but highly recommended for fast AI inference).

### 1. Clone the repository
\`\`\`bash
git clone <your-repo-url>
cd intelligent-compiler-error-correction
\`\`\`

### 2. Install dependencies
While there is no explicitly locked requirements file, you will need the following core packages:
\`\`\`bash
pip install flask torch transformers peft antlr4-python3-runtime codecarbon
\`\`\`
*(Note: If you are regenerating the ANTLR grammar, you will also need the ANTLR4 Java tool).*

### 3. Verify Models
Ensure your locally trained LoRA adapters are located in the `models/` directory:
* `models/codet5_patch_adapter/`
* `models/codet5_security_adapter/`

*(If missing, you can re-run the training script via `python ml/train_codet5_lora.py --train <path> --val <path>`)*

---

## 🏃 How to Run the Project

The primary interface for this project is the real-time web dashboard.

1. **Start the Flask Server**
   From the root directory (`Implementation/`), run:
   \`\`\`bash
   python app.py
   \`\`\`

2. **Access the Dashboard**
   The application will automatically attempt to open your default web browser. If it does not, manually navigate to:
   \`\`\`text
   http://127.0.0.1:5000
   \`\`\`

3. **Using the Interface**
   * Select a test case from the **Examples** sidebar.
   * Modify the code to introduce syntax errors, undefined variables, or security vulnerabilities (like an unsafe `sprintf`).
   * Click **Run Repair** and watch the SSE stream provide live updates on Lexical fixes, Symbol repairs, AI fallbacks, and Security rewrites!
   * Check the **Green Compiler** panel to see your execution efficiency score.

---

## 📂 Project Architecture

* **`compiler/`**: The core logic engine. Contains the lexical/semantic deterministic fixers, the security/taint analysis scripts, the Green computing profiler, and the `gui_bridge.py` linking the compiler to the frontend.
* **`gui/`**: Contains the frontend interface. `templates/` holds the HTML, and `static/` contains the `app.js` responsible for handling the SSE stream and the Monaco Editor instance.
* **`ml/`**: Machine learning scripts used to format datasets, test inferences, and fine-tune the CodeT5 model using LoRA.
* **`models/`**: The directory holding the fine-tuned adapter weights.
* **`grammar/` & `generated/`**: ANTLR4 grammar definitions and the generated lexer/parser/listener python files.
* **`app.py`**: The Flask entry point that routes the API endpoints and SSE connections.

---
*Created by Mahith Reddy Gangu*
