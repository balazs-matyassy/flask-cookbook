from urllib.parse import urlsplit

from flask import g, redirect, url_for, session, flash, request, render_template

from cookbook.core.security.decorators import is_granted
from cookbook.modules.security.forms import LoginForm, EditProfileForm
from cookbook.modules.security import bp
from cookbook.modules.users.repositories import UserRepository


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user:
        return redirect(url_for('pages.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = UserRepository.find_by_username(form.username.data)

        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Login successful.')

            if (request.args.get('redirect')
                    and not urlsplit(request.args.get('redirect')).netloc):
                return redirect(request.args.get('redirect'))

            return redirect(url_for('pages.home'))
        else:
            flash('Wrong username or password.')

    return render_template('security/login.html', form=form)


@bp.route('/logout')
def logout():
    session.clear()
    flash('Logout successful.')

    return redirect(url_for('pages.home'))


@bp.route('/profile', methods=('GET', 'POST'))
@is_granted('IS_AUTHENTICATED_FULLY')
def profile():
    user = g.user
    form = EditProfileForm()

    if form.validate_on_submit():
        try:
            user.password = form.password.data
            UserRepository.save(user)
            flash('Profile saved.')

            return redirect(url_for('security.profile'))
        except Exception as err:
            flash(str(err))

    return render_template('security/profile.html', user=user, form=form)
