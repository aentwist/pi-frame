from . import app, images
from .forms import UploadForm, CreateFolderForm

from flask import request, render_template, render_template_string, redirect,\
        url_for, abort, flash, send_from_directory

import os
import subprocess


upload_folder = app.config["UPLOADS_DEFAULT_DEST"]


@app.route("/", methods=["GET", "POST"])
@app.route("/<path:rel_path>", methods=["GET", "POST"])
def index(rel_path=""):
    # If the request is hitting the wrong route, redirect it.
    if len(rel_path) >= 5 and rel_path[0:4] == "util/":
        rel_fp = rel_path
        return redirect(url_for("file", rel_fp=rel_fp))

    abs_path = os.path.join(upload_folder, rel_path)
    root_path = os.path.join("/", rel_path)

    # Handle the page's forms.
    upload_form = UploadForm()
    create_folder_form = CreateFolderForm()

    if upload_form.submit.data and upload_form.validate():
        images.save(request.files["f"], rel_path)  # rel_path is fp here
        rel_path, fname = os.path.split(rel_path)
        flash(f"Successfully uploaded file {fname}")
        # Redirect to follow the post, redirect, get pattern.
        return redirect(url_for("index", rel_path=rel_path))

    if create_folder_form.submit.data and create_folder_form.validate():
        folder_path = os.path.join(abs_path, create_folder_form.folder_name.data)
        os.mkdir(folder_path)
        return redirect(url_for("index", rel_path=rel_path))

    # Display the contents of the current directory.
    if not os.path.isdir(abs_path):
        abort(404)
    _, dirs, files = next(os.walk(abs_path))

    return render_template("index.html", root_path=root_path, dirs=dirs, files=files,
            upload_form=upload_form, create_folder_form=create_folder_form)


@app.route("/util/file/<path:rel_fp>")
def file(rel_fp):
    rel_path, fname = os.path.split(rel_fp)
    abs_path = os.path.join(upload_folder, rel_path)
    return send_from_directory(abs_path, fname)


slide_t = "1"
blend_t = "2"


@app.route("/util/start")
def start():
    subprocess.run(["ssh", "-T", FRAME_HOST, "sudo", "fbi", "-T", "1", "-t", slide_t,
            "--blend", blend_t, "--readahead", "-a", "--noverbose", "*"])  # -l fname


@app.route("/util/stop")
def stop():
    subprocess.run(["ssh", "-T", FRAME_HOST, "sudo", "kill", "$(pgrep fbi)"])
