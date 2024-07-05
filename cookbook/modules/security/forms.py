from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=(
        InputRequired(message='Username missing'),
    ))
    password = PasswordField('Password', validators=(
        InputRequired(message='Password missing'),
    ))
    submit = SubmitField('Login')


class EditProfileForm(FlaskForm):
    password = PasswordField('Password', validators=(
        InputRequired(message='Password missing'),
        Length(min=8, message='Password too short')
    ))
    confirm_password = PasswordField('Confirm password', validators=(
        InputRequired(message='Password confirmation missing'),
        Length(min=8, message='Password confirmation too short'),
        EqualTo('password', message='Password mismatch')
    ))
    submit = SubmitField('Save')
