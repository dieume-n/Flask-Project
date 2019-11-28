from flask import Blueprint, render_template, redirect, url_for

pages = Blueprint('pages', __name__)


@pages.route('/')
def home():
    return redirect(url_for('auth.sign_in'))
    # return render_template('pages/index.html')


@pages.route('/about')
def about():
    return "About Page"
