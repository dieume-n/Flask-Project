from flask import Flask
from hdps.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_compress import Compress

db = SQLAlchemy()
bcrypt = Bcrypt()
compress = Compress()
login_manager = LoginManager()
login_manager.login_message_category = "info"
login_manager.login_view = "auth.sign_in"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    compress.init_app(app)

    from hdps.pages.views import pages
    from hdps.users.views import users
    from hdps.auth.views import auth
    from hdps.admin.views import admin

    app.register_blueprint(pages)
    app.register_blueprint(users)
    app.register_blueprint(auth)
    app.register_blueprint(admin)

    return app


def setup_db(app):
    from datetime import date
    from hdps.users.models import User, UserData, UserActivity
    from hdps.patients.models import Patient

    with app.app_context():
        db.create_all()

        patient = Patient(name="John Snow", date_of_birth=date.today)

        if not User.query.filter_by(email="admin@hdps.com").first():
            user = User(first_name="John", last_name="Doe",
                        email="admin@hdps.com", password="secret", user_type="Admin")
            db.session.add(user)

        if not User.query.filter_by(email="nurse@hdps.com").first():
            nurse = User(first_name="Jane", last_name="Doe",
                         email="nurse@hdps.com", password="secret", user_type="Nurse")
            db.session.add(nurse)
            db.session.commit()

        if not User.query.filter_by(email="doctor@hdps.com").first():
            doctor = User(first_name="Robert", last_name="Lane",
                          email="doctor@hdps.com", password="secret", user_type="Doctor")
            db.session.add(doctor)
            db.session.commit()

        if not User.query.filter_by(email="movile@hdps.com").first():
            mobile = User(first_name="Damien", last_name="Wayne",
                          email="mobile@hdps.com", password="secret", user_type="Mobile")

            user_data = UserData(
                height=175, weight=75, gender='Male', smoke=False, alco=False, user=mobile)
            user_activity = UserActivity(
                steps=4000, cal=30, distance=300, activity=mobile)

            db.session.add(mobile)
            db.session.add(user_data)
            db.session.add(user_activity)
            db.session.commit()
