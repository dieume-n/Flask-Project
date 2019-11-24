from flask import Blueprint, render_template

pages = Blueprint('pages', __name__)


@pages.route('/')
def home():
    return "Home Page"


@pages.route('/about')
def about():
    return "About Page"
