from flask import Flask


app = Flask(__name__)
app.config.from_object(config.Config)

upload_folder = app.config["UPLOAD_FOLDER"]
if app.config["ENV"] == "development" and not os.path.isdir(upload_folder):
    os.mkdir(upload_folder)


from app import app
