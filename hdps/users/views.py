from datetime import date
from werkzeug.security import safe_str_cmp
from flask import Blueprint, redirect, render_template, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from hdps import db
from hdps.users.forms import UserAccountForm, MobileAccountForm
from hdps.users.models import User
from hdps.users.utils import save_picture

users = Blueprint('users', __name__)


@users.route('/users/dashboard')
@login_required
def user_dashboard():
    today = date.today().strftime("%B %d, %Y")
    # return render_template('users/users-dashboard.html', today=today)
    return render_template('users/dashboard.html', today=today)


@users.route('/users/account', methods=['GET', 'POST'])
@login_required
def user_account():
    form = MobileAccountForm() if safe_str_cmp(
        current_user.get_role(), 'Mobile') else UserAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            print('picture')
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        if safe_str_cmp(current_user.get_role(), "Mobile"):
            current_user.user_data.height = form.height.data
            current_user.user_data.weight = form.weight.data
        db.session.commit()
        flash('Your account information has been updated!', 'success')
        return redirect(url_for('users.user_account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        if safe_str_cmp(current_user.get_role(), 'Mobile'):
            form.height.data = current_user.user_data.height
            form.weight.data = current_user.user_data.weight
    return render_template('users/account.html', form=form)


@users.route('/users/nurses')
def nurses():
    nurses = User.query.filter_by(user_type="Nurse").all()


@users.route('/users/doctors')
def doctors():
    doctors = User.query.filter_by(user_type="Doctor").all()
