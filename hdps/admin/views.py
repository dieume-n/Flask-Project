from datetime import date
from flask import Blueprint, request, redirect, url_for, render_template
from hdps.users.models import User
from hdps.patients.models import Patient


admin = Blueprint("admin", __name__)


@admin.route('/admin/dashboard')
def admin_dashboard():
    today = date.today().strftime("%B %d, %Y")
    data = {
        "count": {
            "total_users": User.query.filter(User.user_type != "Admin").count(),
            "nurses": User.query.filter_by(user_type="Nurse").count(),
            "mobile_users": User.query.filter_by(user_type="Mobile").count(),
            "doctors": User.query.filter_by(user_type="Doctor").count(),
        }
    }
    return render_template('admin/dashboard.html', today=today, data=data)


@admin.route('/admin/users-list')
def users_list():
    users = User.query.all()
    return render_template('admin/users-list.html', users=users)


@admin.route('/admin/patients-list')
def patients_list():
    patients = Patient.query.all()
    return render_template('admin/patients-list.html', patients=patients)
