from . import app
from .forms import CreateFolderForm

from flask import request, render_template, redirect, url_for, abort, flash 
from werkzeug.utils import secure_filename

import os
import subprocess


FRAME_HOST = "pi@192.168.1.31"
slide_t = "1"
blend_t = "2"

upload_folder = app.config["UPLOAD_FOLDER"]


@app.route("/", methods=["GET", "POST"])  ###
@app.route("/<path:path>", methods=["GET", "POST"])
def index(path=""):
    create_folder_form = CreateFolderForm()

    if create_folder_form.validate_on_submit():
        folder_path = os.path.join(upload_folder, path, create_folder_form.folder_name.data)
        os.mkdir(folder_path)
        # Redirect to follow the post, redirect, get pattern.
        return redirect(url_for("index", path=path))

    fp = os.path.join(upload_folder, path)
    if not os.path.isdir(fp):
        abort(404)
    _, dirs, files = next(os.walk(fp))
    root_path = os.path.join("/", path)

    return render_template("index.html", path=root_path, dirs=dirs, files=files,
            create_folder_form=create_folder_form)


# @app.route("/start")
def start():
    subprocess.run(["ssh", "-T", FRAME_HOST, "sudo", "fbi", "-T", "1", "-t", slide_t,
            "--blend", blend_t, "--readahead", "-a", "--noverbose", "*"])  # -l fname


# @app.route("/stop")
def stop():
    subprocess.run(["ssh", "-T", FRAME_HOST, "sudo", "kill", "$(pgrep fbi)"])
