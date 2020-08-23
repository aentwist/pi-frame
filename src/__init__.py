from flask import Flask
from .config import DevConfig, TestConfig, ProdConfig

import os


app = Flask(__name__)

if app.config["ENV"] == "production":
    app.config.from_object(ProdConfig)
elif app.config["ENV"] == "test":
    app.config.from_object(TestConfig)
else:
    app.config.from_object(DevConfig)

    upload_folder = app.config["UPLOAD_FOLDER"]
    if not os.path.isdir(upload_folder):
        os.mkdir(upload_folder)


#from .app import app
