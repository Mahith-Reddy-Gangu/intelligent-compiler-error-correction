from flask import Flask, render_template, request, jsonify
from compiler.gui_bridge import repair_source_for_gui
import os
import threading
import webbrowser

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


@app.route("/api/examples")
def examples():
    example_dir = "examples"
    files = []

    if os.path.exists(example_dir):
        for f in os.listdir(example_dir):
            if f.endswith(".c"):
                files.append(f)

    files.sort()
    return jsonify(files)


@app.route("/api/example/<name>")
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