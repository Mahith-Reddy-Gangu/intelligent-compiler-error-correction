from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from compiler.gui_bridge import repair_source_for_gui, repair_source_for_gui_stream
import os
import threading
import webbrowser
import json

app = Flask(
    __name__,
    template_folder="gui/templates",
    static_folder="gui/static"
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/repair", methods=["POST"])
def repair():
    data = request.json or {}
    code = data.get("code", "")
    filename = data.get("filename", "main.c")

    result = repair_source_for_gui(code, filename)
    return jsonify(result)


@app.route("/api/repair_stream", methods=["POST"])
def repair_stream():
    data = request.json or {}
    code = data.get("code", "")
    filename = data.get("filename", "main.c")

    @stream_with_context
    def generate():
        for event in repair_source_for_gui_stream(code, filename):
            yield f"data: {json.dumps(event)}\n\n"

    return Response(generate(), mimetype="text/event-stream")

@app.route("/api/testcase", methods=["POST"])
def testcase():
    data = request.json or {}
    code = data.get("code", "")
    filename = data.get("filename", "test_case.c")

    result = repair_source_for_gui(code, filename)
    return jsonify(result)


@app.route("/api/examples")
def examples():
    example_root = "examples"
    files = []

    if os.path.exists(example_root):
        for root, _, filenames in os.walk(example_root):
            for f in filenames:
                if f.endswith(".c"):
                    rel_path = os.path.relpath(os.path.join(root, f), example_root)
                    files.append(rel_path.replace("\\", "/"))

    files.sort()
    return jsonify(files)


@app.route("/api/example/<path:name>")
def load_example(name):
    path = os.path.join("examples", name)

    if not os.path.exists(path):
        return jsonify({"error": "Example not found"}), 404

    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    return jsonify({"code": code, "filename": name})


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True, use_reloader=False)