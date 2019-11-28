from flask import Blueprint, jsonify, request
from hdps.users.models import User, UserActivity, users_activities_schema

api = Blueprint('api', __name__)


@api.route('/sign-up')
def sign_up():
    return jsonify(message='Api')


@api.route('/user-activity')
def user_activity():
    header = request.headers['X-API-KEY']
    if not header:
        return jsonify(message=error), 401
    user = User.query.filter_by(public_id=header).first()
    if user:
        return jsonify(users_activities_schema.dump(user.user_activity)), 200
    else:
        return jsonify(message=f"No user with id {header}"), 404
