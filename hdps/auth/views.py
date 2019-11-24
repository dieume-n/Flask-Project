from flask import Blueprint, redirect, render_template, url_for


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    pass
