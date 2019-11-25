from flask import Flask
from hdps.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_message_category = "info"
login_manager.login_view = "users.login"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from hdps.pages.views import pages
    from hdps.users.views import users
    from hdps.auth.views import auth

    app.register_blueprint(pages)
    app.register_blueprint(users)
    app.register_blueprint(auth)

    return app


def setup_db(app):
    from hdps.users.models import User
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(email="admin@hdps.com").first():
            user = User(first_name="John", last_name="Doe",
                        email="admin@hdps.com", password="secret", user_type="Admin")

            db.session.add(user)
            db.session.commit()
