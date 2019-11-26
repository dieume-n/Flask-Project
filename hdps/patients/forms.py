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
    trestbps = IntegerField('Resting Blood Pressure',
                            validators=[DataRequired()])
    chol = StringField('Serum Cholesterol', validators=[DataRequired()])
    fbs = IntegerField('Fasting Blood Pressure', validators=[DataRequired()])
    restecg = StringField('Resting Electrocardiogram',
                          validators=[DataRequired()])
    thalach = StringField('Max Heart rate', validators=[DataRequired()])
    exang = StringField('Exercise Induced Angina', validators=[DataRequired()])
    oldpeak = StringField('ST Depression', validators=[DataRequired()])
    slope = StringField('Slope of Peak Exercise', validators=[DataRequired()])
    ca = SelectField('# Colored Vessels', coerce=int, choices=[(
        0, 'None'), (1, 'One'), (2, 'Two'), (3, 'Three')], validators=[DataRequired()])
    that = SelectField('Defect Type', coerce=int, choices=[(
        3, 'Normal'), (6, 'Fixed'), (7, 'Reversible')], validators=[DataRequired()])
    submit = SubmitField('Save ')
