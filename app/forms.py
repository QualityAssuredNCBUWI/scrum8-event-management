from flask_wtf import FlaskForm
from wtforms import SelectField, PasswordField, StringField, DateTimeField, TextAreaField,FormField
from wtforms.fields.html5 import DateField
from wtforms.fields.simple import FileField
from wtforms.validators import InputRequired, Email, Optional, EqualTo, DataRequired
from datetime import datetime


class LoginForm(FlaskForm):
    email = StringField('Email' , validators=[InputRequired()])
    password = PasswordField('Password')

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm',message='Must be the same as previous')])
    confirm = PasswordField('Repeat Password')
    profile_photo = FileField('Profile Photo', validators=[InputRequired()])

class CreateEvent(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    start_date = DateField('Start Date', validators=[InputRequired()], format="%d-%m-%Y", default=datetime.now())
    end_date = DateField('End Date', validators=[InputRequired()], format="%d-%m-%Y", default=datetime.now())
    description = TextAreaField('Description', validators=[InputRequired()])
    venue = StringField('Venue', validators=[InputRequired()])
    websiteurl = StringField('Web Site URL', [Optional()])
    group = SelectField('Group', description = 'Select a group', validators=[DataRequired()])
    images = FileField('Images', validators=[InputRequired()])

class CreateGroup(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
