from flask import Blueprint, redirect, render_template, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from hdps import db
from hdps.auth.forms import SignInForm, SignUpForm
from hdps.users.models import User

auth = Blueprint('auth', __name__)


@auth.route('/sign-out')
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('pages.home'))


@auth.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('users.users_dashboard'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if user.get_role() == "Admin":
                next_page = '/admin/dashboard'
            return redirect(next_page) if next_page else redirect(url_for('users.users_dashboard'))
        else:
            flash("Invalid credentials", 'danger')
    return render_template('auth/sign-in.html', form=form)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('users.users_dashboard'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data.capitalize(),
                    last_name=form.last_name.data.capitalize(), email=form.email.data, password=form.password.data, user_type=form.user_type.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account have been created, Please log in', 'success')
        return redirect(url_for('auth.sign_in'))
    return render_template('auth/sign-up.html', form=form)
