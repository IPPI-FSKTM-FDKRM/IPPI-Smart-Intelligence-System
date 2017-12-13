from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    first_name = StringField('first name', validators=[InputRequired(), Length(min=1, max=50)])
    last_name = StringField('last name', validators=[InputRequired(),Length(min=1, max=50)])

class LoginForm(FlaskForm):
    usernameLogin = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    passwordLogin = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class ChangePassword(FlaskForm):
    password1 = PasswordField('password1', validators=[InputRequired(), Length(min=8, max=80)])
    #password2 = PasswordField('password2', validators=[InputRequired(), Length(min=8, max=80)])

