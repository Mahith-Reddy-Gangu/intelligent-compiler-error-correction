let editor;
let currentDecorations = [];
let currentFilename = "main.c";
let suppressHighlightClearOnce = false;

require.config({
    paths: {
        vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs"
    }
});

require(["vs/editor/editor.main"], function () {
    editor = monaco.editor.create(document.getElementById("editor"), {
        value: `int main(){
    int a = 10
    return 0;
}`,
        language: "c",
        theme: "vs-dark",
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 15,
        lineNumbers: "on",
        roundedSelection: false,
        scrollBeyondLastLine: false,
        glyphMargin: true
    });

    editor.onDidChangeModelContent(() => {
        if (suppressHighlightClearOnce) {
            suppressHighlightClearOnce = false;
            return;
        }
        clearChangedLineHighlights();
    });
});
function fillList(id, items, formatter = null) {
    const el = document.getElementById(id);
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
    box.innerHTML = "";

    if (!stats) {
        box.innerText = "No stats";
        return;
    }

    const rows = [
        `Lexical fixes: ${stats.lex_fixes ?? 0}`,
        `Deterministic fixes: ${stats.rule_fixes ?? 0}`,
        `AI fixes: ${stats.ai_fixes ?? 0}`,
        `Symbol fixes: ${stats.sym_fixes ?? 0}`,
        `Semantic fixes: ${stats.sem_fixes ?? 0}`,
        `Iterations: ${stats.iterations ?? 0}`
    ];

    rows.forEach(text => {
        const div = document.createElement("div");
        div.className = "statrow";
        div.innerText = text;
        box.appendChild(div);
    });
}

function applyChangedLineHighlights(lines) {
    if (!editor) return;

    currentDecorations = editor.deltaDecorations(currentDecorations, []);

    if (!lines || lines.length === 0) {
        return;
    }

    const decorations = lines.map(line => ({
        range: new monaco.Range(line, 1, line, 1),
        options: {
            isWholeLine: true,
            className: "changedLineDecoration",
            glyphMarginClassName: "changedGlyph"
        }
    }));

    currentDecorations = editor.deltaDecorations([], decorations);
}

function clearChangedLineHighlights() {
    if (!editor) return;
    currentDecorations = editor.deltaDecorations(currentDecorations, []);
}

function setStatus(statusText) {
    const el = document.getElementById("status");
    el.innerText = statusText || "Unknown";

    el.className = "";
    if (statusText === "SUCCESS") el.classList.add("status-success");
    else if (statusText === "SUCCESS_WITH_WARNINGS") el.classList.add("status-warning");
    else if (statusText === "BLOCKED_SECURITY") el.classList.add("status-danger");
    else if (statusText === "SEM_ISSUES") el.classList.add("status-warning");
    else if (statusText === "UNFIXABLE" || statusText === "STOPPED") el.classList.add("status-danger");
}

async function runRepair() {
    if (!editor) return;

    const code = editor.getValue();

    const response = await fetch("/api/repair", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            code: code,
            filename: currentFilename
        })
    });

    const data = await response.json();

    suppressHighlightClearOnce = true;
    editor.setValue(data.corrected_code || code);
    setStatus(data.status || "Unknown");

    fillList("steps", data.applied_steps || []);
    fillList("errors", data.errors || []);
    fillList(
        "semantic",
        data.semantic_issues || [],
        (item) => {
            const kind = item.kind || "issue";
            const line = item.line ?? "?";
            const col = item.col ?? "?";
            const msg = item.msg || "";
            const name = item.name ? ` (${item.name})` : "";
            return `${kind}${name} at L${line}:${col} -> ${msg}`;
        }
    );
    fillList("security", data.security_warnings || []);
    fillList("logs", data.logs || []);
    renderStats(data.stats || {});

    applyChangedLineHighlights(data.changed_lines || []);
}

async function loadExample() {
    const listRes = await fetch("/api/examples");
    const files = await listRes.json();

    if (!files || files.length === 0) {
        alert("No example files found.");
        return;
    }

    const chosen = prompt(
        "Available examples:\n\n" + files.join("\n") + "\n\nType exact filename to load:",
        files[0]
    );

    if (!chosen) return;

    const res = await fetch("/api/example/" + encodeURIComponent(chosen));
    if (!res.ok) {
        alert("Could not load that example.");
        return;
    }

    const data = await res.json();
    currentFilename = data.filename || chosen;
    document.getElementById("active-file-label").innerText = currentFilename;

    suppressHighlightClearOnce = true;
    editor.setValue(data.code || "");
    setStatus("Example loaded");

    fillList("steps", []);
    fillList("errors", []);
    fillList("semantic", []);
    fillList("security", []);
    fillList("logs", []);
    renderStats({
        lex_fixes: 0,
        rule_fixes: 0,
        ai_fixes: 0,
        sym_fixes: 0,
        sem_fixes: 0,
        iterations: 0
    });
    applyChangedLineHighlights([]);
}

function newFile() {
    currentFilename = "main.c";
    document.getElementById("active-file-label").innerText = currentFilename;
    suppressHighlightClearOnce = true;
    editor.setValue("");
    setStatus("New file");

    fillList("steps", []);
    fillList("errors", []);
    fillList("semantic", []);
    fillList("security", []);
    fillList("logs", []);
    renderStats({
        lex_fixes: 0,
        rule_fixes: 0,
        ai_fixes: 0,
        sym_fixes: 0,
        sem_fixes: 0,
        iterations: 0
    });
    applyChangedLineHighlights([]);
}

const style = document.createElement("style");
style.innerHTML = `
.changedLineDecoration {
    background: rgba(100, 255, 100, 0.16);
}
.changedGlyph {
    background: #7CFC00;
    width: 6px !important;
    margin-left: 3px;
}
.status-success {
    color: #7CFC00;
    font-weight: bold;
}
.status-warning {
    color: #ffd166;
    font-weight: bold;
}
.status-danger {
    color: #ff6b6b;
    font-weight: bold;
}
`;
document.head.appendChild(style);