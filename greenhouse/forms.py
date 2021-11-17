from flask_wtf import FlaskForm
from wtforms import  BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location',  validators=[DataRequired()])
    password = PasswordField('Password')
    confirm_password = PasswordField('Repeat Password', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Repeat Password')
    confirm_Password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')