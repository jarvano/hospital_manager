from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(min=6, max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, max=128)
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(min=6, max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, max=128)
    ])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=64)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=64)
    ])
    role = SelectField('Role', choices=[
        ('doctor', 'Doctor'),
        ('receptionist', 'Receptionist'),
        ('pharmacist', 'Pharmacist'),
        ('lab_technician', 'Lab Technician')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address already registered.')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6, max=128)
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(min=6, max=120)
    ])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6, max=128)
    ])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')