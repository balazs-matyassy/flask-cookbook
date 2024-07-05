import io

from flask import flash, redirect, url_for, request, render_template, abort, g, send_file
from werkzeug.utils import secure_filename

from cookbook.core.security.decorators import is_granted
from cookbook.core.security.utils import deny_access_unless_owner_or_granted
from cookbook.modules.recipes import bp
from cookbook.modules.recipes.forms import CreateRecipeForm, EditRecipeForm, CreateIngredientForm, EditIngredientForm
from cookbook.modules.recipes.models import Recipe, Ingredient, Image
from cookbook.modules.recipes.repositories import RecipeRepository, IngredientRepository, ImageRepository


@bp.route('/')
def list_all():
    if 'search' in request.args:
        recipes = RecipeRepository.find_all_by_name_like(request.args['search'])
    else:
        recipes = RecipeRepository.find_all()

    return render_template('recipes/list.html', recipes=recipes)


@bp.route('/view/<int:recipe_id>')
def view(recipe_id):
    recipe = RecipeRepository.find_by_id(recipe_id) or abort(404)

    return render_template(
        'recipes/view.html',
        recipe=recipe
    )


@bp.route('/create', methods=('GET', 'POST'))
@is_granted('ROLE_ADMIN', 'ROLE_MODERATOR', 'ROLE_EDITOR')
def create():
    recipe = Recipe()
    form = CreateRecipeForm(obj=recipe)

    if form.validate_on_submit():
        form.populate_obj(recipe)
        recipe.owned_by = g.user.id

        try:
            RecipeRepository.save(recipe)
            flash('Recipe created.')

            return redirect(url_for('recipes.list_all'))
        except Exception as err:
            flash(str(err))

    return render_template(
        'recipes/create.html',
        form=form
    )


@bp.route('/edit/<int:recipe_id>', methods=('GET', 'POST'))
@is_granted('ROLE_ADMIN', 'ROLE_MODERATOR', 'ROLE_EDITOR')
def edit(recipe_id):
    recipe = RecipeRepository.find_by_id(recipe_id) or abort(404)
    deny_access_unless_owner_or_granted(recipe, 'ROLE_ADMIN', 'ROLE_MODERATOR')

    form = EditRecipeForm(obj=recipe)

    if form.validate_on_submit():
        form.populate_obj(recipe)

        try:
            RecipeRepository.save(recipe)
            flash('Recipe saved.')

            return redirect(url_for('recipes.edit', recipe_id=recipe_id))
        except Exception as err:
            flash(str(err))

    return render_template(
        'recipes/edit.html',
        form=form,
        recipe=recipe
    )


@bp.route('/delete/<int:recipe_id>', methods=('POST',))
@is_granted('ROLE_ADMIN', 'ROLE_MODERATOR', 'ROLE_EDITOR')
def delete(recipe_id):
    recipe = RecipeRepository.find_by_id(recipe_id) or abort(404)
    deny_access_unless_owner_or_granted(recipe, 'ROLE_ADMIN', 'ROLE_MODERATOR')

    try:
        RecipeRepository.delete(recipe)
        flash('Recipe deleted.')
    except Exception as err:
        flash(str(err))

    return redirect(url_for('recipes.list_all'))


@bp.route('/create-ingredient/<int:recipe_id>', methods=('GET', 'POST'))
@is_granted('ROLE_ADMIN', 'ROLE_MODERATOR', 'ROLE_EDITOR')
def create_ingredient(recipe_id):
    recipe = RecipeRepository.find_by_id(recipe_id) or abort(404)
    deny_access_unless_owner_or_granted(recipe, 'ROLE_ADMIN', 'ROLE_MODERATOR')

    ingredient = Ingredient()
    ingredient.quantity = 0
    form = CreateIngredientForm(obj=ingredient)

    if form.validate_on_submit():
        form.populate_obj(ingredient)
        ingredient.recipe = recipe

        try:
            IngredientRepository.save(ingredient)
            flash('Ingredient created.')

            return redirect(url_for('recipes.create_ingredient', recipe_id=recipe_id))
        except Exception as err:
            flash(str(err))

    return render_template(
        'recipes/create_ingredient.html',
        form=form,
        recipe=recipe
    )


@bp.route('/edit-ingredient/<int:recipe_id>/<int:ingredient_id>', methods=('GET', 'POST'))
@is_granted('ROLE_ADMIN', 'ROLE_MODERATOR', 'ROLE_EDITOR')
def edit_ingredient(recipe_id, ingredient_id):
    ingredient = IngredientRepository.find_by_id_and_recipe_id(ingredient_id, recipe_id) or abort(404)
    recipe = ingredient.recipe
    deny_access_unless_owner_or_granted(recipe, 'ROLE_ADMIN', 'ROLE_MODERATOR')

    form = EditIngredientForm(obj=ingredient)

    if form.validate_on_submit():
        form.populate_obj(ingredient)
        ingredient.recipe = recipe

        try:
            IngredientRepository.save(ingredient)
            flash('Ingredient saved.')

            return redirect(url_for(
                'recipes.edit_ingredient',
                recipe_id=recipe_id,
                ingredient_id=ingredient_id
            ))
        except Exception as err:
            flash(str(err))

    return render_template(
        'recipes/edit_ingredient.html',
        form=form,
        recipe=recipe,
        ingredient_id=ingredient_id
    )


@bp.route('/delete-ingredient/<int:recipe_id>/<int:ingredient_id>', methods=('POST',))
@is_granted('ROLE_ADMIN', 'ROLE_MODERATOR', 'ROLE_EDITOR')
def delete_ingredient(recipe_id, ingredient_id):
    ingredient = IngredientRepository.find_by_id_and_recipe_id(ingredient_id, recipe_id) or abort(404)
    recipe = ingredient.recipe
    deny_access_unless_owner_or_granted(recipe, 'ROLE_ADMIN', 'ROLE_MODERATOR')

    try:
        IngredientRepository.delete(ingredient)
        flash('Ingredient deleted.')
    except Exception as err:
        flash(str(err))

    return redirect(url_for('recipes.edit', recipe_id=recipe_id))


@bp.route('/download-image/<int:recipe_id>/<int:image_id>')
def download_image(recipe_id, image_id):
    image = ImageRepository.find_by_id_and_recipe_id(image_id, recipe_id) or abort(404)

    return send_file(
        io.BytesIO(image.content),
        mimetype=image.mimetype,
        as_attachment=False,
        download_name=image.filename
    )


@bp.route('/upload-image/<int:recipe_id>', methods=('POST',))
@is_granted('ROLE_ADMIN', 'ROLE_MODERATOR', 'ROLE_EDITOR')
def upload_image(recipe_id):
    recipe = RecipeRepository.find_by_id(recipe_id) or abort(404)
    deny_access_unless_owner_or_granted(recipe, 'ROLE_ADMIN', 'ROLE_MODERATOR')

    image = Image()
    image.recipe = recipe
    file = request.files.get('file')

    if file and file.filename:
        image.filename = secure_filename(file.filename)
        image.mimetype = file.content_type
        image.content = file.stream.read()

        try:
            ImageRepository.save(image)
            flash('Image uploaded.')
        except Exception as err:
            flash(str(err))

    return redirect(url_for('recipes.edit', recipe_id=recipe_id))


@bp.route('/delete-image/<int:recipe_id>/<int:image_id>', methods=('POST',))
@is_granted('ROLE_ADMIN', 'ROLE_MODERATOR', 'ROLE_EDITOR')
def delete_image(recipe_id, image_id):
    image = ImageRepository.find_by_id_and_recipe_id(image_id, recipe_id) or abort(404)
    recipe = image.recipe
    deny_access_unless_owner_or_granted(recipe, 'ROLE_ADMIN', 'ROLE_MODERATOR')

    try:
        ImageRepository.delete(image)
        flash('Image deleted.')
    except Exception as err:
        flash(str(err))

    return redirect(url_for('recipes.edit', recipe_id=recipe_id))
