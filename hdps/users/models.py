from datetime import datetime, date
import uuid
from flask_login import UserMixin
from hdps import db, bcrypt, login_manager, ma


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    public_id = db.Column(db.String, nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(20))
    image_file = db.Column(
        db.String(255), nullable=False, default='default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_data = db.relationship('UserData', backref='user', uselist=False)
    user_activity = db.relationship('UserActivity', backref='activity')

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

    def is_admin(self):
        if self.user_type == "Admin":
            return True
        else:
            return False

    def is_mobile(self):
        if self.user_type == "Mobile":
            return True
        else:
            return False

    def is_nurse(self):
        if self.user_type == "Nurse":
            return True
        else:
            return False

    def is_medical(self):
        if self.user_type == "Doctor" or self.user_type == "Nurse":
            return True
        else:
            return False

    def get_user_data(self):
        return self.user_data

    def get_user_activity(self):
        return self.user_activity


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.Date)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    gender = db.Column(db.String(10))
    ap_hi = db.Column(db.Integer)
    ap_lo = db.Column(db.Integer)
    cholesterol = db.Column(db.Integer)
    gluc = db.Column(db.Integer)
    smoke = db.Column(db.Boolean)
    alco = db.Column(db.Boolean)
    active = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)


class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.Integer)
    cal = db.Column(db.Float)
    distance = db.Column(db.Float)
    is_sync = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Date, default=date.today)
    day_of_the_week = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class UserSchema(ma.Schema):
    class Meta:
        fields = ('first_name', 'last_name', 'public_id', 'email',
                  'user_type', 'image_file', 'user_data', 'user_activity')


class UserActivitySchema(ma.Schema):
    class Meta:
        fields = ('steps', 'cal', 'distance', 'is_sync',
                  'day_of_the_week')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_activity_schema = UserActivitySchema()
users_activities_schema = UserActivitySchema(many=True)
