#Author: Rodions Barannikovs
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, ValidationError
from greenhouse.models import users as User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
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
    submitLogin = SubmitField('Log in')

class plantForm(FlaskForm):

    plant_name = StringField("Name")
    date_planted = DateField('Date')
    maxTemp = StringField("Maximum Temperature")
    minTemp = StringField("Minimum Temperature")
    humidity = StringField("humidity")
    soil_moisture = StringField("soil_moisture")
    submit = SubmitField('Send data')
