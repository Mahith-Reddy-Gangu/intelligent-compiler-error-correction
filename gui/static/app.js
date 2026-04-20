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
        value: `int main() {
    int a = 10
    return 0;
}`,
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
    initSidebarResize();
    initRightPanelResize();
    initBottomResize();
    initTestcaseResize();
});

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
        `Syntax repairs: ${stats.rule_fixes ?? 0}`,
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

/* -------------------------------------------------- */
/* GREEN REPORT PANEL */
/* -------------------------------------------------- */
function ensureGreenPanel() {
    let panel = document.getElementById("greenPanel");
    if (panel) return panel;

    const resultPanel = document.getElementById("resultpanel");
    if (!resultPanel) return null;

    panel = document.createElement("div");
    panel.id = "greenPanel";
    panel.className = "panelbox";
    panel.style.marginTop = "14px";
    panel.style.padding = "14px";
    panel.style.borderRadius = "10px";
    panel.style.background = "#ffffff";
    panel.style.color = "#111111";
    panel.style.border = "1px solid #d9d9d9";
    panel.style.boxShadow = "0 2px 8px rgba(0,0,0,0.08)";

    resultPanel.appendChild(panel);
    return panel;
}

function renderGreenReport(report) {
    const panel = ensureGreenPanel();
    if (!panel) return;

    if (!report || Object.keys(report).length === 0) {
        panel.innerHTML = `
            <div style="font-size:24px;font-weight:700;margin-bottom:10px;">Green Compiler</div>
            <div>No green metrics yet.</div>
        `;
        return;
    }

    const score = report.green_score ?? 0;
    const runtime = report.total_runtime_ms ?? 0;
    const hotspot = report.hotspot ?? "unknown";
    const suggestion = report.suggestion ?? "No recommendation.";
    const phase = report.phase_ms || {};
    const values = report.values || {};

    const co2 = values.co2_kg;
    const cpu = values.cpu_percent;
    const memory = values.memory_mb;
    const peakMemory = values.peak_memory_mb;

    let color = "#16a34a";
    if (score < 70) color = "#d97706";
    if (score < 45) color = "#dc2626";

    const scorePercent = Math.max(0, Math.min(100, score));

    const rankedPhases = Object.entries(phase)
        .filter(([k]) => k !== "total")
        .sort((a, b) => Number(b[1]) - Number(a[1]));

    const maxPhase = rankedPhases.length > 0 ? Number(rankedPhases[0][1]) : 1;

    const phaseBars = rankedPhases.map(([name, value]) => {
        const v = Number(value) || 0;
        const pct = maxPhase > 0 ? (v / maxPhase) * 100 : 0;
        const isHotspot = name === hotspot;

        return `
            <div style="margin:8px 0;">
                <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:3px;">
                    <span>${name}${isHotspot ? " 🔥" : ""}</span>
                    <span>${v.toFixed(2)} ms</span>
                </div>
                <div style="height:10px;background:#e5e7eb;border-radius:999px;overflow:hidden;">
                    <div style="
                        width:${pct}%;
                        height:100%;
                        background:${isHotspot ? "#ff8c42" : "#2ecc71"};
                    "></div>
                </div>
            </div>
        `;
    }).join("");

    const metricBars = [
        {
            label: "CPU",
            value: cpu == null ? null : Number(cpu),
            max: 100,
            unit: "%"
        },
        {
            label: "Memory",
            value: memory == null ? null : Number(memory),
            max: peakMemory && peakMemory > 0 ? Number(peakMemory) : (memory || 1),
            unit: " MB"
        },
        {
            label: "Peak Memory",
            value: peakMemory == null ? null : Number(peakMemory),
            max: peakMemory && peakMemory > 0 ? Number(peakMemory) : 1,
            unit: " MB"
        }
    ].map(item => {
        if (item.value == null) {
            return `
                <div style="margin:8px 0;">
                    <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:3px;">
                        <span>${item.label}</span>
                        <span>N/A</span>
                    </div>
                    <div style="height:10px;background:#e5e7eb;border-radius:999px;"></div>
                </div>
            `;
        }

        const pct = item.max > 0 ? Math.max(0, Math.min(100, (item.value / item.max) * 100)) : 0;

        return `
            <div style="margin:8px 0;">
                <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:3px;">
                    <span>${item.label}</span>
                    <span>${item.value.toFixed(2)}${item.unit}</span>
                </div>
                <div style="height:10px;background:#e5e7eb;border-radius:999px;overflow:hidden;">
                    <div style="
                        width:${pct}%;
                        height:100%;
                        background:#4da3ff;
                    "></div>
                </div>
            </div>
        `;
    }).join("");

    panel.innerHTML = `
    <div style="font-size:24px;font-weight:700;margin-bottom:12px;">
        Green Compiler
    </div>

    <div style="font-size:32px;font-weight:800;color:${color};margin-bottom:8px;">
        ${score}/100
    </div>

    <div style="margin-bottom:10px;">
        <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
            <span>Green Score</span>
            <span>${scorePercent.toFixed(0)}%</span>
        </div>
        <div style="height:14px;background:#e5e7eb;border-radius:999px;overflow:hidden;">
            <div style="
                width:${scorePercent}%;
                height:100%;
                background:${color};
            "></div>
        </div>
    </div>

    <div style="margin-bottom:6px;">Runtime: ${Number(runtime).toFixed(2)} ms</div>
    <div style="margin-bottom:6px;">CO₂: ${co2 == null ? "N/A" : Number(co2).toExponential(3)} kg</div>
    <div style="margin-bottom:6px;">Hotspot: <b>${hotspot}</b></div>

    <div style="margin-bottom:12px;">
        <b>Suggestion:</b><br>${suggestion}
    </div>

    <div style="margin-top:16px;margin-bottom:6px;font-size:18px;font-weight:700;">
        System Metrics Graph
    </div>
    ${metricBars}
`;
}

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

function setStatus(statusText) {
    const el = document.getElementById("status");
    if (!el) return;

    el.innerText = statusText || "Unknown";

    el.className = "";
    if (statusText === "SUCCESS") el.classList.add("status-success");
    else if (statusText === "SUCCESS_WITH_WARNINGS") el.classList.add("status-warning");
    else if (statusText === "BLOCKED_SECURITY") el.classList.add("status-danger");
    else if (statusText === "SEM_ISSUES") el.classList.add("status-warning");
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

    renderGreenReport({});
    clearChangedLineHighlights();
    resetProgress();
}

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
    renderGreenReport(data.green_report || {});

    const changedLines = computeChangedLines(beforeCode, afterCode);
    highlightLines(changedLines, data.security_changed_lines || []);

    repairOriginalCode = null;
}

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
                setProgress(100, `Done - ${data.total_repairs || 0} repairs`);
                renderRepairResult(data);
            }
        }
    }
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
        `GREEN SCORE: ${data.green_report?.green_score ?? "NA"}\n\n`;
}

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

/* Keep your resize functions unchanged */
function newFile(){ location.reload(); }
function initSidebarResize(){}
function initRightPanelResize(){}
function initBottomResize(){}
function initTestcaseResize(){}