from datetime import date
from werkzeug.security import safe_str_cmp
from flask import Blueprint, redirect, render_template, url_for, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from hdps import db
from hdps.users.forms import UserAccountForm, MobileAccountForm
from hdps.users.models import User, UserActivity, users_activities_schema, user_activity_schema, user_schema
from hdps.users.utils import save_picture
from hdps.patients.models import Patient

users = Blueprint('users', __name__)


@users.route('/users/dashboard')
@login_required
def user_dashboard():
    today = date.today().strftime("%B %d, %Y")
    activities = current_user.get_user_activity()
    if current_user.is_nurse():
        return redirect(url_for('patients.patients_list'))
    return render_template('users/dashboard.html', today=today, activities=users_activities_schema.dump(activities))


@users.route('/users/account', methods=['GET', 'POST'])
@login_required
def user_account():
    form = MobileAccountForm() if safe_str_cmp(
        current_user.get_role(), 'Mobile') else UserAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        if safe_str_cmp(current_user.get_role(), "Mobile"):
            current_user.user_data.date_of_birth = form.date_of_birth.data
            current_user.user_data.height = form.height.data
            current_user.user_data.weight = form.weight.data
            current_user.user_data.gender = form.gender.data
            current_user.user_data.ap_hi = form.ap_hi.data
            current_user.user_data.ap_lo = form.ap_lo.data
            current_user.user_data.cholesterol = form.cholesterol.data
            current_user.user_data.gluc = form.glucose.data
            current_user.user_data.smoke = True if safe_str_cmp(
                form.smoke.data, 'Yes') else False
            current_user.user_data.alco = True if safe_str_cmp(
                form.alcohol.data, 'Yes') else False
        db.session.commit()
        flash('Your account information has been updated!', 'success')
        return redirect(url_for('users.user_account'))
    else:
        print(form.errors)

    if request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        if safe_str_cmp(current_user.get_role(), 'Mobile'):
            form.date_of_birth.data = current_user.user_data.date_of_birth
            form.height.data = current_user.user_data.height
            form.weight.data = current_user.user_data.weight
            form.gender.data = current_user.user_data.gender
            form.ap_hi.data = current_user.user_data.ap_hi
            form.ap_lo.data = current_user.user_data.ap_lo
            form.cholesterol.data = current_user.user_data.cholesterol
            form.glucose.data = current_user.user_data.gluc
            print("Alcohol", current_user.user_data.alco)
            form.smoke.data = 'Yes' if current_user.user_data.smoke == True else 'No'
            form.alcohol.data = 'Yes' if current_user.user_data.alco == True else 'No'
    return render_template('users/account.html', form=form)


@users.route('/users/nurses')
def nurses():
    nurses = User.query.filter_by(user_type="Nurse").all()


@users.route('/users/doctors')
def doctors():
    doctors = User.query.filter_by(user_type="Doctor").all()
