import pickle
import joblib
import json
import os
import pandas as pd
from werkzeug.security import safe_str_cmp
from flask import Blueprint, url_for, render_template, redirect, request, flash
from flask_login import login_required
from hdps import db
from hdps.patients.models import Patient
from hdps.patients.forms import PatientForm
from hdps.patients.utils import calculate_age
from hdps import basedir


patients = Blueprint('patients', __name__)


@patients.route('/patients-list')
def patients_list():
    patients = Patient.query.all()
    return render_template('patients/patients_list.html', patients=patients)


@patients.route('/patient/add-patient', methods=['GET', 'POST'])
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(name=form.name.data, date_of_birth=form.date_of_birth.data, gender=form.gender.data, height=form.height.data, weight=form.weight.data, chest_pain=form.chest_pain.data, trestbps=form.trestbps.data,
                          chol=form.chol.data, fbs=form.fbs.data, restecg=form.restecg.data, thalach=form.thalach.data, exang=form.exang.data, oldpeak=form.oldpeak.data, slope=form.slope.data, that=form.that.data, ca=form.ca.data)
        db.session.add(patient)
        db.session.commit()
        flash('Patient have been Added!', 'success')
        return redirect(url_for('patients.patients_list'))

    return render_template('patients/new_patient.html', form=form)


@patients.route('/patient/<int:patient_id>/details', methods=['GET', 'POST'])
@login_required
def patients_details(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = PatientForm()
    if form.validate_on_submit():
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
        form.heart_disease.data = "Yes" if patient.prediction == 1 else "No"
    return render_template('patients/patient_details.html', form=form, id=patient_id)


@patients.route('/patient/<int:id>/edit')
def patients_edit(id):
    patient = Patient.query.get_or_404(patient_id)


@patients.route('/patient/<int:id>/delete')
def patients_delete(id):
    patient = Patient.query.get_or_404(patient_id)


@patients.route('/patient/<int:patient_id>/prediction')
def patients_prediction(patient_id):
    data = {}
    patient = Patient.query.get_or_404(patient_id)
    if patient:
        data.update(age=calculate_age(patient.date_of_birth))
        data.update(sex=1 if safe_str_cmp(patient.gender, "Male") else 0)
        data.update(trestbps=patient.trestbps)
        data.update(chol=patient.chol)
        data.update(fbs_1=1 if patient.fbs == 1 else 0)
        data.update(restecg_1=1 if patient.restecg == 1 else 0)
        data.update(restecg_2=1 if patient.restecg == 2 else 0)
        data.update(thalach=patient.thalach)
        data.update(exang_1=1 if patient.exang == 1 else 0)
        data.update(oldpeak=patient.oldpeak)
        data.update(slope_2=1 if patient.slope == 2 else 0)
        data.update(slope_3=1 if patient.slope == 3 else 0)
        data.update(ca_1=1 if patient.ca == 1 else 0)
        data.update(ca_2=1 if patient.ca == 2 else 0)
        data.update(ca_3=1 if patient.ca == 3 else 0)
        data.update(thal_6=1 if patient.that == 6 else 0)
        data.update(thal_7=1 if patient.that == 7 else 0)
        data.update(cp_3=1 if patient.chest_pain == 3 else 0)
        data.update(cp_4=1 if patient.chest_pain == 4 else 0)
        data.update(cp_2=1 if patient.chest_pain == 2 else 0)

        patient_data = json.dumps(data)

        if os.path.getsize(basedir+"/patients/SVM_model.pkl") > 0:
            with open(basedir+"/patients/SVM_model.pkl", 'rb') as f:
                classifier = joblib.load(f)
                query_df = pd.DataFrame([data])
                # print(query_df)
                # print(query_df)
                # query_df = pd.get_dummies(query_df)
                # print(query_df)
                prediction = classifier.predict(query_df)
                print(prediction)
                # if prediction[0] == 1:
                #     patient.prediction = 1
                #     db.session.commit()
                # else:
                #     patient.prediction = 0
                #     db.session.commit()
                flash("Your prediction restult is ready", 'success')
                return redirect(url_for('patients.patients_details', patient_id=patient_id))

    return redirect(url_for('patients.patients_details', patient_id=patient_id))
