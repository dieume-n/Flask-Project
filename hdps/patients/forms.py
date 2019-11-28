from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired, Length


class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[(
        "Male", 'Male'), ("Female", 'Female')], validators=[DataRequired()])
    height = IntegerField('Heigt in Cm', validators=[DataRequired()])
    weight = StringField('Weigt in Kg', validators=[DataRequired()])
    chest_pain = SelectField('Chest Pain Type', coerce=int, choices=[(
        1, 'Typical'), (2, 'Angina'), (3, 'Non Angina'), (4, 'Asymptomatic')], validators=[DataRequired()], default=None)
    trestbps = IntegerField('Resting Blood Pressure in mm Hg on admission to the hospital',
                            validators=[DataRequired()])
    chol = StringField('Serum Cholesterol  in mg/dl',
                       validators=[DataRequired()])
    fbs = SelectField('Fasting Blood Pressure > 120 mg/dl', coerce=int, choices=[(
        0, 'No'), (1, 'Yes')])
    restecg = SelectField('Resting electrocardiographic results', coerce=int, choices=[(
        0, 'Normal'), (1, 'ST-T wave abnormal'), (2, 'Shows probable or definite left ventricular hypertrophy')])
    thalach = StringField('Max Heart rate', validators=[DataRequired()])
    exang = SelectField('Exercise Induced Angina', coerce=int, choices=[(
        0, 'No'), (1, 'Yes')])
    oldpeak = StringField(
        'ST depression induced by exercise relative to rest', validators=[DataRequired()])
    slope = SelectField('Slope of Peak Exercise', coerce=int, choices=[(
        1, 'Upsloping'), (2, 'Flat'), (3, 'Downsloping')], validators=[DataRequired()])
    ca = SelectField('# Colored Vessels', coerce=int, choices=[(
        0, 'None'), (1, 'One'), (2, 'Two'), (3, 'Three')])
    that = SelectField('Defect Type', coerce=int, choices=[(
        3, 'Normal'), (6, 'Fixed'), (7, 'Reversible')], validators=[DataRequired()])
    heart_disease = StringField('Heart disease')
    submit = SubmitField('Save ')
