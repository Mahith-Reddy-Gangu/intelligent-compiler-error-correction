let editor;
let currentDecorations = [];
let suppressHighlightClearOnce = false;

const openFiles = {};
let openTabs = [];
let currentFilename = "main.c";
let repairOriginalCode = null;

require.config({
    paths: {
        vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs"
    }
});

require(["vs/editor/editor.main"], function () {
    editor = monaco.editor.create(document.getElementById("editor"), {
        value: `int main() {\n    int a = 10\n    return 0;\n}`,
        language: "c",
        theme: "vs",
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 15,
        lineNumbers: "on",
        roundedSelection: false,
        scrollBeyondLastLine: false,
        glyphMargin: true
    });

    openFiles["main.c"] = editor.getValue();
    openTabs = ["main.c"];
    currentFilename = "main.c";
    renderTabs();

    editor.onDidChangeModelContent(() => {
        openFiles[currentFilename] = editor.getValue();

        if (suppressHighlightClearOnce) {
            suppressHighlightClearOnce = false;
            return;
        }

        clearChangedLineHighlights();
    });

    refreshExamples();
});

/* -------------------------------------------------- */
/* Utilities                                          */
/* -------------------------------------------------- */

function fillList(id, items, formatter = null) {
    const el = document.getElementById(id);
    if (!el) return;

    el.innerHTML = "";

    if (!items || items.length === 0) {
        const li = document.createElement("li");
        li.innerText = "None";
        el.appendChild(li);
        return;
    }

    items.forEach(item => {
        const li = document.createElement("li");
        li.innerText = formatter ? formatter(item) : item;
        el.appendChild(li);
    });
}

function renderStats(stats) {
    const box = document.getElementById("stats");
    if (!box) return;

    box.innerHTML = "";

    if (!stats) {
        box.innerText = "No stats";
        return;
    }

    const rows = [
        `Lexical fixes: ${stats.lex_fixes ?? 0}`,
        `Rule fixes: ${stats.rule_fixes ?? 0}`,
        `AI fixes: ${stats.ai_fixes ?? 0}`,
        `Symbol fixes: ${stats.sym_fixes ?? 0}`,
        `Iterations: ${stats.iterations ?? 0}`
    ];

    rows.forEach(text => {
        const div = document.createElement("div");
        div.className = "statrow";
        div.innerText = text;
        box.appendChild(div);
    });
}

/* -------------------------------------------------- */
/* Line highlights                                    */
/* -------------------------------------------------- */

function highlightLines(changedLines, securityLines) {
    if (!editor) return;

    currentDecorations = editor.deltaDecorations(currentDecorations, []);

    const changed = changedLines || [];
    const security = new Set(securityLines || []);
    const allLines = [...new Set([...changed, ...(securityLines || [])])];

    if (allLines.length === 0) return;

    const decorations = allLines.map(line => ({
        range: new monaco.Range(line, 1, line, 1),
        options: {
            isWholeLine: true,
            className: security.has(line) ? "securityHighlight" : "normalHighlight",
            glyphMarginClassName: security.has(line) ? "securityGlyph" : "changedGlyph"
        }
    }));

    currentDecorations = editor.deltaDecorations([], decorations);
}

function clearChangedLineHighlights() {
    if (!editor) return;
    currentDecorations = editor.deltaDecorations(currentDecorations, []);
}

/* -------------------------------------------------- */
/* Status / Progress                                  */
/* -------------------------------------------------- */

function setStatus(statusText) {
    const el = document.getElementById("status");
    if (!el) return;

    el.innerText = statusText || "Unknown";
    el.className = "";

    if (statusText === "SUCCESS") el.classList.add("status-success");
    else if (statusText === "UNFIXABLE" || statusText === "STOPPED") el.classList.add("status-danger");
}

function setProgress(percent, text) {
    const bar = document.getElementById("repairProgressBar");
    const label = document.getElementById("repairProgressText");

    if (bar) {
        const safe = Math.max(0, Math.min(100, percent || 0));
        bar.style.width = `${safe}%`;
    }

    if (label) label.innerText = text || "Running...";
}

function resetProgress() {
    setProgress(0, "Idle");
}

function resetPanels() {
    fillList("steps", []);
    fillList("errors", []);
    fillList("security", []);

    renderStats({
        lex_fixes: 0,
        rule_fixes: 0,
        ai_fixes: 0,
        sym_fixes: 0,
        iterations: 0
    });

    clearChangedLineHighlights();
    resetProgress();
}

/* -------------------------------------------------- */
/* Tab management                                     */
/* -------------------------------------------------- */

function renderTabs() {
    const tabbar = document.getElementById("tabbar");
    if (!tabbar) return;

    tabbar.innerHTML = "";

    openTabs.forEach(filename => {
        const tab = document.createElement("div");
        tab.className = "filetab" + (filename === currentFilename ? " active" : "");
        tab.onclick = () => switchTab(filename);

        const name = document.createElement("span");
        name.innerText = filename.split("/").pop();

        const close = document.createElement("span");
        close.className = "filetab-close";
        close.innerText = "×";
        close.onclick = (e) => {
            e.stopPropagation();
            closeTab(filename);
        };

        tab.appendChild(name);
        tab.appendChild(close);
        tabbar.appendChild(tab);
    });

    const label = document.getElementById("active-file-label");
    if (label) label.innerText = currentFilename;
}

function switchTab(filename) {
    if (!editor || !openFiles.hasOwnProperty(filename)) return;

    openFiles[currentFilename] = editor.getValue();
    currentFilename = filename;

    suppressHighlightClearOnce = true;
    editor.setValue(openFiles[filename] ?? "");
    renderTabs();
    resetPanels();
    setStatus("Switched tab");
}

function closeTab(filename) {
    if (openTabs.length === 1) return;

    const idx = openTabs.indexOf(filename);
    if (idx !== -1) openTabs.splice(idx, 1);
    delete openFiles[filename];

    if (currentFilename === filename) {
        currentFilename = openTabs[Math.max(0, idx - 1)] || openTabs[0];
        suppressHighlightClearOnce = true;
        editor.setValue(openFiles[currentFilename] ?? "");
    }

    renderTabs();
    resetPanels();
}

function openFileInTab(filename, code) {
    if (!openTabs.includes(filename)) openTabs.push(filename);

    openFiles[filename] = code;
    currentFilename = filename;

    suppressHighlightClearOnce = true;
    editor.setValue(code);
    renderTabs();
    resetPanels();
}

function newFile() {
    location.reload();
}

/* -------------------------------------------------- */
/* Repair result rendering                            */
/* -------------------------------------------------- */

function computeChangedLines(beforeCode, afterCode) {
    const before = (beforeCode || "").split("\n");
    const after = (afterCode || "").split("\n");
    const maxLen = Math.max(before.length, after.length);
    const changed = [];

    for (let i = 0; i < maxLen; i++) {
        if ((before[i] || "") !== (after[i] || "")) changed.push(i + 1);
    }

    return changed;
}

function renderRepairResult(data) {
    const beforeCode = repairOriginalCode ?? "";
    const afterCode = data.corrected_code || editor.getValue();

    suppressHighlightClearOnce = true;
    editor.setValue(afterCode);
    openFiles[currentFilename] = afterCode;

    setStatus(data.status || "Unknown");

    fillList("steps", data.applied_steps || []);
    fillList("errors", data.errors || []);
    fillList("security", data.security_warnings || []);
    renderStats(data.stats || {});

    const changedLines = computeChangedLines(beforeCode, afterCode);
    highlightLines(changedLines, data.security_changed_lines || []);

    repairOriginalCode = null;
}

/* -------------------------------------------------- */
/* Repair (streaming)                                 */
/* -------------------------------------------------- */

async function runRepair() {
    if (!editor) return;

    repairOriginalCode = editor.getValue();
    openFiles[currentFilename] = repairOriginalCode;

    resetPanels();
    setStatus("RUNNING");
    setProgress(2, "Starting repair...");

    const response = await fetch("/api/repair_stream", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            code: repairOriginalCode,
            filename: currentFilename
        })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const chunks = buffer.split("\n\n");
        buffer = chunks.pop();

        for (const chunk of chunks) {
            if (!chunk.startsWith("data: ")) continue;

            const data = JSON.parse(chunk.slice(6));

            if (data.type === "start") {
                setProgress(3, data.message || "Started...");
            }

            if (data.type === "detect") {
                const iter = data.stats?.iterations ?? 0;
                const percent = Math.min(85, 5 + iter);
                setProgress(percent, data.message || "Error detected...");
                renderStats(data.stats || {});
                fillList("steps", data.applied_steps || []);
            }

            if (data.type === "fix") {
                const totalRepairs = data.total_repairs ?? 0;
                const percent = Math.min(95, 8 + totalRepairs);
                setProgress(percent, data.message || "Applied fix...");
                renderStats(data.stats || {});
                fillList("steps", data.applied_steps || []);
            }

            if (data.type === "done") {
                setProgress(100, `Done — ${data.total_repairs || 0} repairs`);
                renderRepairResult(data);
            }
        }
    }
}

/* -------------------------------------------------- */
/* Examples sidebar                                   */
/* -------------------------------------------------- */

async function refreshExamples() {
    const listRes = await fetch("/api/examples");
    const files = await listRes.json();

    const tree = document.getElementById("file-tree");
    if (!tree) return;

    tree.innerHTML = "";

    files.forEach(filename => {
        const item = document.createElement("div");
        item.className = "file-item";
        item.innerText = filename;
        item.dataset.filename = filename;

        item.onclick = async () => {
            const res = await fetch("/api/example/" + encodeURIComponent(filename));
            const data = await res.json();
            openFileInTab(data.filename || filename, data.code || "");
        };

        tree.appendChild(item);
    });
}