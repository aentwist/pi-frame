from . import app, images
from .forms import UploadForm, CreateFolderForm

from flask import request, Response, render_template, render_template_string,\
        redirect, url_for, abort, flash, send_from_directory
from werkzeug.utils import secure_filename

from PIL import Image

import os
import pexpect
import time


uploads_dir = app.config["UPLOADS_DEFAULT_DEST"]
thumbnail_dir = os.path.join(uploads_dir, "thumbnail")
full_dir = os.path.join(uploads_dir, "full")
if not os.path.isdir(thumbnail_dir):
    os.mkdir(thumbnail_dir) 
if not os.path.isdir(full_dir):
    os.mkdir(full_dir) 
results_per_page = app.config["RESULTS_PER_PAGE"]


@app.route("/")
def root():
    return redirect(url_for("index"))


@app.route("/folder/", methods=["GET", "POST"])
@app.route("/folder/<path:rel_path>", methods=["GET", "POST"])
def index(rel_path=""):
    thumbnail_path = os.path.join(thumbnail_dir, rel_path)
    full_path = os.path.join(full_dir, rel_path)
    page = 1 if "page" not in request.args else int(request.args["page"])

    # Handle the page's folder manipulation forms.
    create_folder_form = CreateFolderForm()
    if create_folder_form.create_folder_submit.data and create_folder_form.validate():
        os.mkdir(os.path.join(thumbnail_path, create_folder_form.folder_name.data))
        os.mkdir(os.path.join(full_path, create_folder_form.folder_name.data))
        return redirect(url_for("index", rel_path=rel_path, page=page))

    # Display the contents of the current directory.
    if not os.path.isdir(full_path):
        abort(404)
    _, dirs, fnames = next(os.walk(full_path))
    files = [{"thumbnail_fname": f"{os.path.splitext(fname)[0]}.webp", "full_fname": fname} for fname in fnames]
    file_count = len(files)
    page_start = (page - 1) * results_per_page
    page_end = min(page * results_per_page, file_count)

    return render_template("index.html", rel_path=rel_path, dirs=dirs,
            files=files[page_start:page_end], file_count=file_count,
            page=page, results_per_page=results_per_page,
            upload_form=UploadForm(), create_folder_form=create_folder_form)


@app.route("/file/get/full/<path:rel_fp>")
def get_file(rel_fp):
    rel_path, fname = os.path.split(rel_fp)
    abs_path = os.path.join(full_dir, rel_path)
    return send_from_directory(abs_path, fname, mimetype="image/jpeg")


@app.route("/file/get/thumbnail/<path:rel_fp>")
def get_thumbnail(rel_fp):
    rel_path, fname = os.path.split(rel_fp)
    abs_path = os.path.join(thumbnail_dir, rel_path)
    return send_from_directory(abs_path, fname, mimetype="image/webp")


@app.route("/file/post/", methods=["POST"])
@app.route("/file/post/<path:rel_path>", methods=["POST"])
# TODO: Reload the current slideshow after uploading to its domain.
def post_files(rel_path=""):
    page = request.args["page"] or 1

    form = UploadForm()
    if form.validate():
        _, full_name = os.path.split(full_dir)
        for f in form.files.data:
            fname = secure_filename(f.filename)
            fname_no_ext, _ = os.path.splitext(fname)
            images.save(f, os.path.join(full_name, rel_path), fname)
            im = Image.open(f)
            im.thumbnail((99999, 540))
            im.save( os.path.join(thumbnail_dir, rel_path, f"{fname_no_ext}.webp"), method=6)
        flash("Files uploaded successfully")
        # Redirect to follow the post, redirect, get pattern.
        return redirect(url_for("index", rel_path=rel_path, page=page))


@app.route("/file/delete/<path:rel_fp>", methods=["DELETE"])
# TODO: Use safe_filename?
def delete_file(rel_fp):
    full_fp = os.path.join(full_dir, rel_fp)
    rel_path, fname = os.path.split(rel_fp)
    fname_no_ext, _ = os.path.splitext(fname)
    thumbnail_fp = os.path.join(thumbnail_dir, rel_path, f"{fname_no_ext}.webp")
    if not os.path.isfile(full_fp) or not os.path.isfile(thumbnail_fp):
        return Response(f"Error: File {fname} not found", 404, mimetype="text/plain")
    os.remove(full_fp)
    os.remove(thumbnail_fp)
    return Response("File deleted successfully", 200, mimetype="text/plain")


slide_t = 10
quiet = True
subcontents = False


@app.route("/slideshow/start/")
@app.route("/slideshow/start/<path:rel_path>")
# TODO: Support slideshow customization rather than all images in directory.
def start_slideshow(rel_path=""):
    # TODO: Check that the slideshow path has images to display.
    # Use * for all subfolder contents.
    fim = pexpect.spawn(
        f'ssh {app.config["FRAME_USERNAME"]}@{app.config["FRAME_HOST"]} "' +
        f"fim -T 8 {'-q ' if quiet else ''}" +
        f"-c 'while (1) {{ display; sleep {slide_t}; next; }}' " +
        os.path.join(full_dir, rel_path, "*" if subcontents else "") +
        '"'
    )
    time.sleep(2)

    response_text = f"Slideshow of /{rel_path or ''} started"
    response_code = 200
    return Response(response_text, response_code, mimetype="text/plain")


@app.route("/slideshow/stop")
def stop_slideshow():
    pexpect.run(
        f'ssh {app.config["FRAME_USERNAME"]}@{app.config["FRAME_HOST"]} "' +
        "pkill fim && " +
        "cp /dev/zero /dev/fb0" +
        '"'
    )

    response_text = "Slideshow stopped"
    response_code = 200
    return Response(response_text, response_code, mimetype="text/plain")
