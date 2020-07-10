import os

from flask import Flask, render_template, redirect, url_for, abort


app = Flask(__name__)

upload_folder = "/var/www/full-frame/uploads"
if app.config["ENV"] == "production":
    upload_folder = "/mnt/hdd/shared"
elif not os.path.isdir(upload_folder):
    os.mkdir(upload_folder)
app.config["UPLOAD_FOLDER"] = upload_folder
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


@app.route("/")
@app.route("/<path>")
def index(path=""):
    fp = os.path.join(upload_folder, path)
    if not os.path.isdir(fp):
        abort(404)
    _, dirs, files = next(os.walk(fp))
    root_path = os.path.join("/", path)
    return render_template("index.html", path=root_path, dirs=dirs, files=files)
