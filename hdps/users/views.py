from datetime import date
from flask import Blueprint, redirect, render_template, url_for

users = Blueprint('users', __name__)


@users.route('/users/dashboard')
def user_dashboard():
    today = date.today().strftime("%B %d, %Y")
    # return render_template('users/users-dashboard.html', today=today)
    return render_template('users/users-dashboard.html', today=today)


@users.route('/users/account')
def user_acccount():
    pass
