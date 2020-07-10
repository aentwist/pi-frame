import os

from flask import Flask


UPLOAD_FOLDER = "/var/www/full-frame/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/<path>")
def index(path):
    _, dirs, files = next(os.walk(f"./{path}"))
    return render_template("index", path, dirs, files)
