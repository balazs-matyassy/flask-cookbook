from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField

from cookbook.modules.categories.repositories import CategoryRepository


class RecipeMixin:
    category = QuerySelectField(query_factory=CategoryRepository.find_all, get_label='name')
    name = StringField('Name', validators=(
        InputRequired(message='Name missing'),
        Length(max=180, message='Name is too long')
    ))
    description = TextAreaField('description')
    difficulty = SelectField('Difficulty', choices=[
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★')
    ])


class CreateRecipeForm(FlaskForm, RecipeMixin):
    submit = SubmitField('Create')


class EditRecipeForm(FlaskForm, RecipeMixin):
    submit = SubmitField('Save')


class IngredientMixin:
    name = StringField('Name', validators=(
        InputRequired(message='Name missing'),
        Length(max=180, message='Name is too long')
    ))
    quantity = IntegerField('Quantity', validators=(
        NumberRange(min=0, message='Quantity is less than zero'),
    ))
    unit = StringField('Unit', validators=(
        Length(max=180, message='Unit is too long'),
    ))


class CreateIngredientForm(FlaskForm, IngredientMixin):
    submit = SubmitField('Create')


class EditIngredientForm(FlaskForm, IngredientMixin):
    submit = SubmitField('Save')
