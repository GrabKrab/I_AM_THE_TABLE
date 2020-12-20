from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField


class ImportFzile(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Submit')
