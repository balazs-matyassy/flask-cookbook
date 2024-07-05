
from flask import flash, redirect, url_for, request, render_template, abort

from cookbook.core.security.decorators import is_granted
from cookbook.modules.users import bp
from cookbook.modules.users.forms import CreateUserForm, EditUserForm
from cookbook.modules.users.models import User
from cookbook.modules.users.repositories import UserRepository


@bp.route('/')
@is_granted('ROLE_ADMIN')
def list_all():
    if 'search' in request.args:
        users = UserRepository.find_all_by_username_like(request.args['search'])
    else:
        users = UserRepository.find_all()

    return render_template('users/list.html', users=users)


@bp.route('/create', methods=('GET', 'POST'))
@is_granted('ROLE_ADMIN')
def create():
    user = User()
    form = CreateUserForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)

        try:
            UserRepository.save(user)
            flash('User created.')

            return redirect(url_for('users.list_all'))
        except Exception as err:
            flash(str(err))

    return render_template('users/create.html', form=form)


@bp.route('/edit/<int:user_id>', methods=('GET', 'POST'))
@is_granted('ROLE_ADMIN')
def edit(user_id):
    user = UserRepository.find_by_id(user_id) or abort(404)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)

        try:
            UserRepository.save(user)
            flash('User saved.')

            return redirect(url_for('users.edit', user_id=user_id))
        except Exception as err:
            flash(str(err))

    return render_template('users/edit.html', form=form)


@bp.route('/delete/<int:user_id>', methods=('POST',))
@is_granted('ROLE_ADMIN')
def delete(user_id):
    user = UserRepository.find_by_id(user_id) or abort(404)

    try:
        UserRepository.delete(user)
        flash('User deleted.')
    except Exception as err:
        flash(str(err))

    return redirect(url_for('users.list_all'))
