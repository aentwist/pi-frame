from . import app
from flask import request, render_template, redirect, url_for, abort, flash 
from werkzeug.utils import secure_filename

import os
import subprocess


FRAME_HOST = "pi@192.168.1.31"
slide_t = "1"
blend_t = "2"

upload_folder = app.config["UPLOAD_FOLDER"]


@app.route("/", methods=["GET", "POST"])
@app.route("/<path>", methods=["GET", "POST"])
def index(path=""):
    if request.method == "POST":
        # do stuff
        false
    fp = os.path.join(upload_folder, path)
    if not os.path.isdir(fp):
        abort(404)
    _, dirs, files = next(os.walk(fp))
    root_path = os.path.join("/", path)
    return render_template("index.html", path=root_path, dirs=dirs, files=files)


@app.route("/create_folder", methods=["POST"])
def create_folder(path, folder_name):
    folder_path = os.path.join(upload_folder, path, folder_name)
    os.mkdir(folder_path)
    redirect("index")


@app.route("/start")
def start():
    subprocess.run(["ssh", "-T", FRAME_HOST, "sudo", "fbi", "-T", "1", "-t", slide_t,
            "--blend", blend_t, "--readahead", "-a", "--noverbose", "*"])  # -l fname


@app.route("/stop")
def stop():
    subprocess.run(["ssh", "-T", FRAME_HOST, "sudo", "kill", "$(pgrep fbi)"])
