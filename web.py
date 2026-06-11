#!/usr/bin/env python3
import os, sys, glob, shutil, uuid, subprocess
from flask import Flask, request, send_file, render_template, after_this_request

sys.path.insert(0, os.path.dirname(__file__))
from downloader import find_ytdlp, YT_MENU, SC_MENU, SEPARATOR

app = Flask(__name__)
TMPDIR = "/tmp/ytdlp-web"

YT_FORMATS = [item for item in YT_MENU if item is not SEPARATOR]
SC_FORMATS = [item for item in SC_MENU if item is not SEPARATOR]

ALL_FORMATS = {}
for i, (label, args) in enumerate(YT_FORMATS):
    ALL_FORMATS[f"yt_{i}"] = {"label": label, "args": args, "source": "YouTube"}
for i, (label, args) in enumerate(SC_FORMATS):
    ALL_FORMATS[f"sc_{i}"] = {"label": label, "args": args, "source": "SoundCloud"}


@app.route("/")
def index():
    yt = [(k, v["label"]) for k, v in ALL_FORMATS.items() if v["source"] == "YouTube"]
    sc = [(k, v["label"]) for k, v in ALL_FORMATS.items() if v["source"] == "SoundCloud"]
    return render_template("index.html", yt_formats=yt, sc_formats=sc)


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url", "").strip()
    fmt_key = request.form.get("format", "")

    if not url or fmt_key not in ALL_FORMATS:
        return "Невірні дані", 400

    ytdlp = find_ytdlp()
    if not ytdlp:
        return "yt-dlp не знайдено на сервері", 500

    fmt = ALL_FORMATS[fmt_key]
    session_dir = os.path.join(TMPDIR, str(uuid.uuid4()))
    os.makedirs(session_dir, exist_ok=True)

    cmd = [ytdlp] + fmt["args"] + [
        "--no-check-certificate",
        "-o", os.path.join(session_dir, "%(title)s.%(ext)s"),
        url,
    ]
    result = subprocess.run(cmd, capture_output=True)

    files = [f for f in glob.glob(os.path.join(session_dir, "*")) if not f.endswith(".part")]

    if not files:
        shutil.rmtree(session_dir, ignore_errors=True)
        err = result.stderr.decode(errors="replace")
        return f"<pre>Помилка:\n{err}</pre>", 500

    filepath = files[0]

    @after_this_request
    def cleanup(response):
        shutil.rmtree(session_dir, ignore_errors=True)
        return response

    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
