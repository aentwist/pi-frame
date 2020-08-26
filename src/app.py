from . import app, images
from .forms import UploadForm, CreateFolderForm

from flask import request, Response, render_template, render_template_string,\
        redirect, url_for, abort, flash, send_from_directory
from werkzeug.utils import secure_filename

import os
import subprocess


upload_folder = app.config["UPLOADS_DEFAULT_DEST"]


@app.route("/", methods=["GET", "POST"])
@app.route("/folder/", methods=["GET", "POST"])
@app.route("/folder/<path:rel_path>", methods=["GET", "POST"])
def index(rel_path=""):
    abs_path = os.path.join(upload_folder, rel_path)
    root_path = os.path.join("/", rel_path)

    # Handle the page's forms.
    upload_form = UploadForm()
    create_folder_form = CreateFolderForm()

    if upload_form.upload_submit.data and upload_form.validate():
        for f in upload_form.files.data:
            fname = secure_filename(f.filename)
            images.save(f, rel_path, fname)
        flash("Files uploaded successfully")
        # Redirect to follow the post, redirect, get pattern.
        return redirect(url_for("index", rel_path=rel_path))

    if create_folder_form.create_folder_submit.data and create_folder_form.validate():
        folder_path = os.path.join(abs_path, create_folder_form.folder_name.data)
        os.mkdir(folder_path)
        return redirect(url_for("index", rel_path=rel_path))

    # Display the contents of the current directory.
    if not os.path.isdir(abs_path):
        abort(404)
    _, dirs, files = next(os.walk(abs_path))

    return render_template("index.html", root_path=root_path, dirs=dirs, files=files,
            upload_form=upload_form, create_folder_form=create_folder_form)


@app.route("/file/get/<path:rel_fp>")
def get_file(rel_fp):
    rel_path, fname = os.path.split(rel_fp)
    abs_path = os.path.join(upload_folder, rel_path)
    return send_from_directory(abs_path, fname)


@app.route("/file/delete/<path:rel_fp>", methods=["DELETE"])
# TODO: Use safe_filename?
def delete_file(rel_fp):
    abs_fp = os.path.join(upload_folder, rel_fp)
    if not os.path.isfile(abs_fp):
        return Response("Error: File not found", 404, mimetype="text/plain")
    os.remove(abs_fp)
    return Response("File deleted successfully", 200, mimetype="text/plain")


slide_t = "1"
blend_t = "2"


@app.route("/util/start")
def start():
    subprocess.run(["ssh", "-T", FRAME_HOST, "sudo", "fbi", "-T", "1", "-t", slide_t,
            "--blend", blend_t, "--readahead", "-a", "--noverbose", "*"])  # -l fname


@app.route("/util/stop")
def stop():
    subprocess.run(["ssh", "-T", FRAME_HOST, "sudo", "kill", "$(pgrep fbi)"])
