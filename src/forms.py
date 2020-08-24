from . import images

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class UploadForm(FlaskForm):
    f = FileField("File", validators=[FileRequired(), FileAllowed(images, "Image file type not supported.")])
    submit = SubmitField("Upload")


class CreateFolderForm(FlaskForm):
    folder_name = StringField("Name", validators=[InputRequired()])
    submit = SubmitField("Create")
