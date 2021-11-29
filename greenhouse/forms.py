from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, ValidationError
from greenhouse.models import users as User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
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

    plant_name = SelectField(u'name', choices=[('Carrot', 'Carrot'), ('Cucumber', 'Cucumber'), ('Tomato', 'Tomato')])
    plant_id = StringField("plant_id")
    date_planted = DateField('Date')
    temperature = StringField("temperature")
    humidity = StringField("humidity")
    soil_moisture = StringField("soil_moisture")
    submit = SubmitField('Send data')
