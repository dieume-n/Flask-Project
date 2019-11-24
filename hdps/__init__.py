from flask import Flask
from hdps.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    from hdps.pages.views import pages

    app.register_blueprint(pages)

    return app


def setup_db(app):
    with app.app_context():
        pass
