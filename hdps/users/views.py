from flask import Blueprint, redirect, render_template, url_for

users = Blueprint('users', __name__)


@users.route('/users/dashboard')
def user_dashboard():
    pass


@users.route('/users/account')
def user_acccount():
    pass
