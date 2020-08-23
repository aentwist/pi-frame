from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import required


class CreateFolderForm(FlaskForm):
    folder_name = StringField("Name", validators=[required()])
    submit = SubmitField("Create")
