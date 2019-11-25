from flask_wtf import FlaskForm
from wtforms.fields import StringField, BooleanField, RadioField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from hdps.users.models import User


class SignInForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class SignUpForm(FlaskForm):
    first_name = StringField('First name', validators=[
                             DataRequired()])
    last_name = StringField('Last name', validators=[
        DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Password', validators=[DataRequired(), EqualTo('password')])
    user_type = RadioField('Who are you?', choices=[(
        'Doctor', 'Doctor'), ('Nurse', 'Nurse')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is already taken. Please use a different one.')
