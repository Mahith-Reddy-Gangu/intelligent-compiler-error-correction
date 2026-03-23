let editor;
let currentDecorations = [];
let suppressHighlightClearOnce = false;

const openFiles = {};
let openTabs = [];
let currentFilename = "main.c";

require.config({
    paths: {
        vs: "https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs"
    }
});

require(["vs/editor/editor.main"], function () {
    editor = monaco.editor.create(document.getElementById("editor"), {
        value: `int main() {
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
    initSidebarResize();
    initRightPanelResize();
    initBottomResize();
    initTestcaseResize();
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

function highlightLines(changedLines, securityLines) {
    if (!editor) return;

    currentDecorations = editor.deltaDecorations(currentDecorations, []);

    if (!changedLines || changedLines.length === 0) {
        return;
    }

    const securitySet = new Set(securityLines || []);

    const decorations = changedLines.map(line => ({
        range: new monaco.Range(line, 1, line, 1),
        options: {
            isWholeLine: true,
            className: securitySet.has(line) ? "securityHighlight" : "normalHighlight",
            glyphMarginClassName: securitySet.has(line) ? "securityGlyph" : "changedGlyph"
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

function resetPanels() {
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

function renderTabs() {
    const tabbar = document.getElementById("tabbar");
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

    document.getElementById("active-file-label").innerText = currentFilename;
    highlightActiveFileInSidebar();
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
    if (openTabs.length === 1) {
        return;
    }

    const idx = openTabs.indexOf(filename);
    if (idx !== -1) {
        openTabs.splice(idx, 1);
    }

    delete openFiles[filename];

    if (currentFilename === filename) {
        currentFilename = openTabs[Math.max(0, idx - 1)] || openTabs[0];
        suppressHighlightClearOnce = true;
        editor.setValue(openFiles[currentFilename] ?? "");
    }

    renderTabs();
    resetPanels();
    setStatus("Tab closed");
}

function openFileInTab(filename, code) {
    if (!openTabs.includes(filename)) {
        openTabs.push(filename);
    }

    openFiles[filename] = code;
    currentFilename = filename;

    suppressHighlightClearOnce = true;
    editor.setValue(code);
    renderTabs();
    resetPanels();
    setStatus("File loaded");
}

async function runRepair() {
    if (!editor) return;

    openFiles[currentFilename] = editor.getValue();

    const response = await fetch("/api/repair", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            code: editor.getValue(),
            filename: currentFilename
        })
    });

    const data = await response.json();

    suppressHighlightClearOnce = true;
    editor.setValue(data.corrected_code || editor.getValue());
    openFiles[currentFilename] = editor.getValue();

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

    highlightLines(
        data.changed_lines || [],
        data.security_changed_lines || []
    );
}

async function runTestCase() {
    const input = document.getElementById("testcase-input").value;
    const output = document.getElementById("testcase-output");

    output.value = "Running...";

    const response = await fetch("/api/testcase", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            code: input,
            filename: "test_case.c"
        })
    });

    const data = await response.json();

    output.value =
        `STATUS: ${data.status || "Unknown"}\n\n` +
        `CORRECTED CODE:\n${data.corrected_code || ""}\n\n` +
        `STEPS:\n${(data.applied_steps || []).join("\n")}\n\n` +
        `ERRORS:\n${(data.errors || []).join("\n")}\n\n` +
        `SECURITY:\n${(data.security_warnings || []).join("\n")}`;
}

async function refreshExamples() {
    const listRes = await fetch("/api/examples");
    const files = await listRes.json();

    const tree = document.getElementById("file-tree");
    tree.innerHTML = "";

    if (!files || files.length === 0) {
        const empty = document.createElement("div");
        empty.className = "file-item";
        empty.innerText = "No example files found";
        tree.appendChild(empty);
        return;
    }

    files.forEach(filename => {
        const item = document.createElement("div");
        item.className = "file-item";
        item.innerText = filename;
        item.dataset.filename = filename;
        item.onclick = async () => {
            const res = await fetch("/api/example/" + encodeURIComponent(filename));
            if (!res.ok) {
                alert("Could not load example.");
                return;
            }
            const data = await res.json();
            openFileInTab(data.filename || filename, data.code || "");
        };
        tree.appendChild(item);
    });

    highlightActiveFileInSidebar();
}

function highlightActiveFileInSidebar() {
    const items = document.querySelectorAll(".file-item");
    items.forEach(item => {
        if (item.dataset.filename === currentFilename) {
            item.classList.add("active");
        } else {
            item.classList.remove("active");
        }
    });
}

function newFile() {
    let base = "untitled.c";
    let name = base;
    let counter = 1;

    while (openFiles.hasOwnProperty(name)) {
        name = `untitled_${counter}.c`;
        counter++;
    }

    openTabs.push(name);
    openFiles[name] = "";
    currentFilename = name;

    suppressHighlightClearOnce = true;
    editor.setValue("");
    renderTabs();
    resetPanels();
    setStatus("New file");
}

function initSidebarResize() {
    const sidebar = document.getElementById("sidebar");
    const resizer = document.getElementById("sidebar-resizer");

    let isResizing = false;

    resizer.addEventListener("mousedown", () => {
        isResizing = true;
        document.body.style.cursor = "col-resize";
    });

    document.addEventListener("mousemove", (e) => {
        if (!isResizing) return;

        const newWidth = Math.min(420, Math.max(180, e.clientX));
        sidebar.style.width = `${newWidth}px`;
    });

    document.addEventListener("mouseup", () => {
        if (!isResizing) return;
        isResizing = false;
        document.body.style.cursor = "default";
    });
}

function initRightPanelResize() {
    const editorPanel = document.getElementById("editorpanel");
    const resultPanel = document.getElementById("resultpanel");
    const resizer = document.getElementById("rightpanel-resizer");
    const container = document.querySelector(".editor-and-side");

    let isResizing = false;

    resizer.addEventListener("mousedown", () => {
        isResizing = true;
        document.body.style.cursor = "col-resize";
    });

    document.addEventListener("mousemove", (e) => {
        if (!isResizing) return;

        const rect = container.getBoundingClientRect();
        let leftWidth = e.clientX - rect.left;
        const total = rect.width;

        leftWidth = Math.max(220, Math.min(total - 240, leftWidth));
        const rightWidth = total - leftWidth - resizer.offsetWidth;

        editorPanel.style.width = `${leftWidth}px`;
        resultPanel.style.width = `${rightWidth}px`;
    });

    document.addEventListener("mouseup", () => {
        if (!isResizing) return;
        isResizing = false;
        document.body.style.cursor = "default";
    });
}

function initBottomResize() {
    const topSection = document.getElementById("top-section");
    const testcasePanel = document.getElementById("testcase-panel");
    const resizer = document.getElementById("bottom-resizer");
    const mainPanel = document.querySelector(".mainpanel");
    const tabbar = document.getElementById("tabbar");

    let isResizing = false;

    resizer.addEventListener("mousedown", () => {
        isResizing = true;
        document.body.style.cursor = "row-resize";
    });

    document.addEventListener("mousemove", (e) => {
        if (!isResizing) return;

        const rect = mainPanel.getBoundingClientRect();
        const tabbarHeight = tabbar.offsetHeight;
        const usableTop = rect.top + tabbarHeight;
        const totalHeight = rect.height - tabbarHeight - resizer.offsetHeight;

        let newTopHeight = e.clientY - usableTop;
        newTopHeight = Math.max(180, Math.min(totalHeight - 120, newTopHeight));
        const newBottomHeight = totalHeight - newTopHeight;

        topSection.style.height = `${newTopHeight}px`;
        testcasePanel.style.height = `${newBottomHeight}px`;
    });

    document.addEventListener("mouseup", () => {
        if (!isResizing) return;
        isResizing = false;
        document.body.style.cursor = "default";
    });
}

function initTestcaseResize() {
    const leftBox = document.getElementById("testcase-input-box");
    const rightBox = document.getElementById("testcase-output-box");
    const resizer = document.getElementById("testcase-resizer");
    const container = document.getElementById("testcase-grid");

    let isResizing = false;

    resizer.addEventListener("mousedown", () => {
        isResizing = true;
        document.body.style.cursor = "col-resize";
    });

    document.addEventListener("mousemove", (e) => {
        if (!isResizing) return;

        const rect = container.getBoundingClientRect();
        let leftWidth = e.clientX - rect.left;
        const total = rect.width;

        leftWidth = Math.max(120, Math.min(total - 120, leftWidth));
        const rightWidth = total - leftWidth - resizer.offsetWidth;

        leftBox.style.width = `${leftWidth}px`;
        rightBox.style.width = `${rightWidth}px`;
    });

    document.addEventListener("mouseup", () => {
        if (!isResizing) return;
        isResizing = false;
        document.body.style.cursor = "default";
    });
}