from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, InputRequired,Email 
from flask_wtf.file import FileField, FileRequired, FileAllowed

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name' , validators=[InputRequired, DataRequired])
    lastname = StringField('Last Name' , validators=[InputRequired, DataRequired])
    email = StringField('Email', validators=[DataRequired(), Email()])


class PhotoForm(FlaskForm):
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'Images only!'])
    ])
    