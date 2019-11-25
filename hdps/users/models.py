from datetime import datetime
import uuid
from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean
from flask_login import UserMixin
from hdps import db, bcrypt, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    public_id = Column(String, nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    user_type = Column(String(20))
    image_file = Column(
        String(255), nullable=False, default='default.jpg')
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, first_name, last_name, email, password, user_type):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.public_id = str(uuid.uuid1())
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.user_type = user_type

    def check_password(self, password):
        if bcrypt.check_password_hash(self.password, password):
            return True
        else:
            return False

    def get_role(self):
        return self.user_type


class UserData(db.Model):
    id = Column(Integer, primary_key=True)
    height = Column(Float)
    weight = Column(Float)
    active = Column(Boolean)
    smoke = Column(Boolean)
    alchohol = Column(Boolean)


class UserActivity(db.Model):
    id = Column(Integer, primary_key=True)
    step = Column(Integer)
    cal = Column(Float)
    distance = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
