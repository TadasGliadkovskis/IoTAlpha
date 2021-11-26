from flask_wtf import FlaskForm
from wtforms import  BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired, ValidationError
from greenhouse.models import users as User

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
    def validateUsername(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("username taken, choose another one")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Repeat Password')
    confirm_Password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')



