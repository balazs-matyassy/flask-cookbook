from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length, Optional
from wtforms_sqlalchemy.fields import QuerySelectField

from cookbook.modules.users.repositories import RoleRepository


class CreateUserForm(FlaskForm):
    username = StringField('Name', validators=(
        InputRequired(message='Name missing'),
        Length(max=180, message='Name is too long')
    ))
    password = PasswordField('Password', validators=(
        InputRequired(message='Password missing'),
        Length(min=8, message='Password too short')
    ))
    role = QuerySelectField(query_factory=RoleRepository.find_all, get_label='name')
    submit = SubmitField('Create')


class EditUserForm(FlaskForm):
    username = StringField('Name', validators=(
        InputRequired(message='Name missing'),
        Length(max=180, message='Name is too long')
    ))
    password = PasswordField('Password', validators=(
        Optional(),
        Length(min=8, message='Password too short'),
    ))
    role = QuerySelectField(query_factory=RoleRepository.find_all, get_label='name')
    submit = SubmitField('Save')
