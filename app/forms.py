from flask_wtf import FlaskForm
from wtforms import SelectField, PasswordField, StringField, DateTimeField, TextAreaField
from wtforms.validators import InputRequired, Email, Optional,EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email' , validators=[Email()])
    password = PasswordField('Password')

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired])
    email = StringField('Email', validators=[Email(),InputRequired()])
    password = PasswordField('password', validators=[InputRequired, EqualTo('confirm',message='Must be the same as previous')])
    confirm = PasswordField('Repeat Password')

class CreateEvent(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    start_date = DateTimeField('Start Date', validators=[InputRequired()])
    end_date = DateTimeField ('End Date', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    venue = StringField('Venue', validators=[InputRequired()])
    websiteurl = StringField('Web Site URL', [Optional()])
    status = SelectField('Event Status',choices=[('Pending','Pending'),('Published','Published')],validators=[InputRequired()])

class CreateGroup(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
