from flask import Flask
from .config import DevConfig, TestConfig, ProdConfig
from flask_uploads import configure_uploads, UploadSet, IMAGES

import os


app = Flask(__name__)

# Create the app configuration.
env = app.config["ENV"]
if env == "production":
    app.config.from_object(ProdConfig)
elif env == "test":
    app.config.from_object(TestConfig)
else:
    app.config.from_object(DevConfig)

# Define configuration for all environments. Set the DESTs before
# configure_uploads is called.
images = UploadSet("images", IMAGES)
uploads_default_dest = app.config["UPLOADS_DEFAULT_DEST"]
app.config["UPLOADED_IMAGES_DEST"] = uploads_default_dest
configure_uploads(app, images)

if not os.path.isdir(uploads_default_dest):
    os.mkdir(uploads_default_dest)

# Define configuration for specific environments.
if env == "production":
    pass
elif env == "test":
    pass
else:
    pass


#from .app import app
