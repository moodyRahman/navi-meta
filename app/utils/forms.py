from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import *


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm = PasswordField(
        'confirm',
        validators=[
            DataRequired(), 
            EqualTo('password', message='Passwords do not match')
        ]
    )

# WIP
# Form to add college to user's list?    