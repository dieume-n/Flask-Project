from flask import Blueprint, url_for, render_template, redirect, request, flash
from flask_login import login_required
from hdps import db
from hdps.patients.models import Patient
from hdps.patients.forms import PatientForm


patients = Blueprint('patients', __name__)


@patients.route('/patients-list')
def patients_list():
    patients = Patient.query.all()
    return render_template('patients/patients_list.html', patients=patients)


@patients.route('/patient/add-patient')
def add_patient():
    return render_template('patients/new_patient.html')


@patients.route('/patient/<int:patient_id>/details', methods=['GET', 'POST'])
@login_required
def patients_details(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    print("First")
    form = PatientForm()
    if form.validate_on_submit():
        print('Second')
        patient.name = form.name.data
        patient.date_of_birth = form.date_of_birth.data
        patient.gender = form.gender.data
        patient.height = form.height.data
        patient.weight = form.weight.data
        patient.chest_pain = form.chest_pain.data
        patient.trestbps = form.trestbps.data
        patient.chol = form.chol.data
        patient.fbs = form.fbs.data
        patient.restecg = form.restecg.data
        patient.thalach = form.thalach.data
        patient.exang = form.exang.data
        patient.oldpeak = form.oldpeak.data
        patient.slope = form.slope.data
        patient.ca = form.ca.data
        patient.that = form.that.data
        db.session.commit()
        flash('Patient Information has been updated!', 'success')
        return redirect(url_for('patients.patients_details', patient_id=patient.id))
    else:
        print('something is wrong')

    if request.method == 'GET':
        form.name.data = patient.name
        form.date_of_birth.data = patient.date_of_birth
        form.gender.data = patient.gender
        form.height.data = patient.height
        form.weight.data = patient.weight
        form.chest_pain.data = patient.chest_pain
        form.trestbps.data = patient.trestbps
        form.chol.data = patient.chol
        form.fbs.data = patient.fbs
        form.restecg.data = patient.restecg
        form.thalach.data = patient.thalach
        form.exang.data = patient.exang
        form.oldpeak.data = patient.oldpeak
        form.slope.data = patient.slope
        form.ca.data = patient.ca
        form.that.data = patient.that
    return render_template('patients/patient_details.html', form=form)


@patients.route('/patient/<int:id>/edit')
def patients_edit(id):
    patient = Patient.query.get_or_404(patient_id)


@patients.route('/patient/<int:id>/delete')
def patients_delete(id):
    patient = Patient.query.get_or_404(patient_id)
