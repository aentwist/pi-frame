from . import app, images
from .forms import UploadForm, CreateFolderForm

from flask import request, Response, render_template, render_template_string,\
        redirect, url_for, abort, flash, send_from_directory
from werkzeug.utils import secure_filename

import os
import subprocess


upload_folder = app.config["UPLOADS_DEFAULT_DEST"]
results_per_page = app.config["RESULTS_PER_PAGE"]


@app.route("/")
def root():
    return redirect(url_for("index"))


@app.route("/folder/", methods=["GET", "POST"])
@app.route("/folder/<path:rel_path>", methods=["GET", "POST"])
def index(rel_path=""):
    abs_path = os.path.join(upload_folder, rel_path)
    page = 1 if "page" not in request.args else int(request.args["page"])

    # Handle the page's folder manipulation forms.
    create_folder_form = CreateFolderForm()
    if create_folder_form.create_folder_submit.data and create_folder_form.validate():
        folder_path = os.path.join(abs_path, create_folder_form.folder_name.data)
        os.mkdir(folder_path)
        return redirect(url_for("index", rel_path=rel_path, page=page))

    # Display the contents of the current directory.
    if not os.path.isdir(abs_path):
        abort(404)
    _, dirs, files = next(os.walk(abs_path))
    file_count = len(files)
    page_start = (page - 1) * results_per_page
    page_end = min(page * results_per_page, file_count)

    return render_template("index.html", rel_path=rel_path, dirs=dirs,
            files=files[page_start:page_end], file_count=file_count,
            page=page, results_per_page=results_per_page,
            upload_form=UploadForm(), create_folder_form=create_folder_form)


@app.route("/file/get/<path:rel_fp>")
def get_file(rel_fp):
    rel_path, fname = os.path.split(rel_fp)
    abs_path = os.path.join(upload_folder, rel_path)
    return send_from_directory(abs_path, fname)


@app.route("/file/post/", methods=["POST"])
@app.route("/file/post/<path:rel_path>", methods=["POST"])
# TODO: Reload the current slideshow after uploading to its domain.
def post_files(rel_path=""):
    page = request.args["page"] if request.args["page"] else 1

    form = UploadForm()
    if form.validate():
        for f in form.files.data:
            fname = secure_filename(f.filename)
            images.save(f, rel_path, fname)
        flash("Files uploaded successfully")
        # Redirect to follow the post, redirect, get pattern.
        return redirect(url_for("index", rel_path=rel_path, page=page))


@app.route("/file/delete/<path:rel_fp>", methods=["DELETE"])
# TODO: Use safe_filename?
def delete_file(rel_fp):
    abs_fp = os.path.join(upload_folder, rel_fp)
    if not os.path.isfile(abs_fp):
        return Response("Error: File not found", 404, mimetype="text/plain")
    os.remove(abs_fp)
    return Response("File deleted successfully", 200, mimetype="text/plain")


slide_t = "10"
quiet = True
subcontents = False


@app.route("/slideshow/start/")
@app.route("/slideshow/start/<path:rel_path>")
# TODO: Support slideshow customization rather than all images in directory.
def start_slideshow(rel_path=""):
    # Use * for all subfolder contents.
    global fim
    fim = subprocess.Popen([
        "/usr/bin/fim", "-T", "9", "-o", "fb", "-q" if quiet else "", "-c",
        f"'while (1) {{ display; sleep {slide_t}; next; }}'",
        os.path.join(upload_folder, rel_path, "*" if subcontents else "")
    ])
    # if start_result.stderr:
    #     response_text = start_result.stderr
    #     response_code = 500
    # else:
    response_text = f"Slideshow of /{rel_path + '/' if rel_path else ''} started"
    response_code = 200
    return Response(response_text, response_code, mimetype="text/plain")


@app.route("/slideshow/stop")
def stop_slideshow():
    response_text = "Slideshow stopped"
    response_code = 200

    global fim
    if not fim:
        response_text = "No slideshow"
        response_code = 500
    else:
        fim.kill()
        # Clear the framebuffer (assume the default framebuffer device fb0). This
        # will always produce a no space left on device error as the zeros device
        # zero has infinite bytes.
        subprocess.run(
            "sudo cp /dev/zero /dev/fb0",
            shell=True
        )
        # if stop_result.stderr:
        #     response_text = stop_result.stderr
        #     response_code = 500

    return Response(response_text, response_code, mimetype="text/plain")
