from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo
from app.models import User

class UserEditForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(min=6, max=120)
    ])
    password = PasswordField('New Password', validators=[
        Optional(),
        Length(min=6, max=128)
    ])
    password2 = PasswordField('Confirm New Password', validators=[
        Optional(),
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
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('receptionist', 'Receptionist'),
        ('pharmacist', 'Pharmacist'),
        ('lab_technician', 'Lab Technician')
    ], validators=[DataRequired()])
    is_active = BooleanField('Active')

    def __init__(self, original_email=None, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Email address already registered.')

class SystemSettingsForm(FlaskForm):
    hospital_name = StringField('Hospital Name', validators=[
        DataRequired(),
        Length(max=100)
    ])
    address = TextAreaField('Address', validators=[
        DataRequired(),
        Length(max=200)
    ])
    phone = StringField('Phone', validators=[
        DataRequired(),
        Length(max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    consultation_fee = DecimalField('Consultation Fee', validators=[
        DataRequired()
    ])
    currency = SelectField('Currency', choices=[
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('INR', 'Indian Rupee')
    ], validators=[DataRequired()])
    time_zone = SelectField('Time Zone', choices=[
        ('UTC', 'UTC'),
        ('US/Eastern', 'US Eastern'),
        ('US/Central', 'US Central'),
        ('US/Pacific', 'US Pacific'),
        ('Asia/Kolkata', 'India Standard Time')
    ], validators=[DataRequired()])
    appointment_duration = SelectField('Default Appointment Duration (minutes)', 
        choices=[
            ('15', '15 minutes'),
            ('30', '30 minutes'),
            ('45', '45 minutes'),
            ('60', '1 hour')
        ],
        validators=[DataRequired()]
    )
    working_hours_start = SelectField('Working Hours Start',
        choices=[(str(x), f'{x:02d}:00') for x in range(0, 24)],
        validators=[DataRequired()]
    )
    working_hours_end = SelectField('Working Hours End',
        choices=[(str(x), f'{x:02d}:00') for x in range(0, 24)],
        validators=[DataRequired()]
    )
    enable_notifications = BooleanField('Enable Email Notifications')
    maintenance_mode = BooleanField('Maintenance Mode')