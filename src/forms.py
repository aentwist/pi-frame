from . import images

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, SubmitField, MultipleFileField
from wtforms.validators import InputRequired


class UploadForm(FlaskForm):
    # Valdiation for MultipleFileField is currently unsupported.
    # https://github.com/lepture/flask-wtf/issues/337
    # validators=[FilesRequired(), FilesAllowed(images, "Image file type not supported")]
    files = MultipleFileField("Select files")
    upload_submit = SubmitField("Upload")


class CreateFolderForm(FlaskForm):
    folder_name = StringField("Name", validators=[InputRequired()])
    create_folder_submit = SubmitField("Create")
