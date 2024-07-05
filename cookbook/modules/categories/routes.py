
from flask import flash, redirect, url_for, request, render_template, abort

from cookbook.core.security.decorators import is_granted
from cookbook.modules.categories import bp
from cookbook.modules.categories.forms import CreateCategoryForm, EditCategoryForm
from cookbook.modules.categories.models import Category
from cookbook.modules.categories.repositories import CategoryRepository


@bp.route('/')
def list_all():
    if 'search' in request.args:
        categories = CategoryRepository.find_all_by_name_like(request.args['search'])
    else:
        categories = CategoryRepository.find_all()

    return render_template('categories/list.html', categories=categories)


@bp.route('/view/<int:category_id>')
def view(category_id):
    category = CategoryRepository.find_by_id(category_id) or abort(404)

    return render_template(
        'categories/view.html',
        category=category
    )


@bp.route('/create', methods=('GET', 'POST'))
@is_granted('ROLE_ADMIN')
def create():
    category = Category()
    form = CreateCategoryForm(obj=category)

    if form.validate_on_submit():
        form.populate_obj(category)

        try:
            CategoryRepository.save(category)
            flash('Category created.')

            return redirect(url_for('categories.list_all'))
        except Exception as err:
            flash(str(err))

    return render_template('categories/create.html', form=form)


@bp.route('/edit/<int:category_id>', methods=('GET', 'POST'))
@is_granted('ROLE_ADMIN')
def edit(category_id):
    category = CategoryRepository.find_by_id(category_id) or abort(404)
    form = EditCategoryForm(obj=category)

    if form.validate_on_submit():
        form.populate_obj(category)

        try:
            CategoryRepository.save(category)
            flash('Category saved.')

            return redirect(url_for('categories.edit', category_id=category_id))
        except Exception as err:
            flash(str(err))

    return render_template('categories/edit.html', form=form)


@bp.route('/delete/<int:category_id>', methods=('POST',))
@is_granted('ROLE_ADMIN')
def delete(category_id):
    category = CategoryRepository.find_by_id(category_id) or abort(404)

    try:
        CategoryRepository.delete(category)
        flash('Category deleted.')
    except Exception as err:
        flash(str(err))

    return redirect(url_for('categories.list_all'))
