from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length


class CategoryMixin:
    name = StringField('Name', validators=(
        InputRequired(message='Name missing'),
        Length(max=180, message='Name is too long')
    ))
    description = TextAreaField('Description')


class CreateCategoryForm(FlaskForm, CategoryMixin):
    submit = SubmitField('Create')


class EditCategoryForm(FlaskForm, CategoryMixin):
    submit = SubmitField('Save')
