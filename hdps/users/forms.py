from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from hdps.users.models import User
from wtforms.fields import StringField, BooleanField, RadioField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length


class UserAccountForm(FlaskForm):
    first_name = StringField('First name', validators=[
        DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name', validators=[
        DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    picture = FileField('Profile Picture', validators=[
                        FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is already taken. Please use a different one.')


class MobileAccountForm(FlaskForm):
    first_name = StringField('First name', validators=[
        DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name', validators=[
        DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    height = FloatField('Height', validators=[
        DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    picture = FileField('Profile Image', validators=[
                        FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is already taken. Please use a different one.')
