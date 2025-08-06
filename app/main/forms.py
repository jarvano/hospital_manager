from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional
from datetime import datetime

class PatientRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=64)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=64)
    ])
    date_of_birth = DateField('Date of Birth', validators=[
        DataRequired()
    ])
    gender = SelectField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    blood_group = SelectField('Blood Group', choices=[
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-')
    ], validators=[Optional()])
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Length(min=10, max=20)
    ])
    email = StringField('Email', validators=[
        Optional(),
        Email(),
        Length(max=120)
    ])
    address = TextAreaField('Address', validators=[
        DataRequired(),
        Length(max=200)
    ])

class AppointmentForm(FlaskForm):
    doctor_id = SelectField('Doctor', coerce=int, validators=[
        DataRequired()
    ])
    appointment_date = DateTimeField('Appointment Date and Time', 
        format='%Y-%m-%d %H:%M',
        validators=[DataRequired()],
        default=datetime.now
    )
    notes = TextAreaField('Notes', validators=[
        Optional(),
        Length(max=500)
    ])

class SearchPatientForm(FlaskForm):
    query = StringField('Search by name or phone', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])

class BillingForm(FlaskForm):
    service_type = SelectField('Service Type', choices=[
        ('consultation', 'Consultation'),
        ('medication', 'Medication'),
        ('lab_test', 'Laboratory Test'),
        ('procedure', 'Medical Procedure')
    ], validators=[DataRequired()])
    quantity = IntegerField('Quantity', default=1, validators=[
        DataRequired()
    ])
    unit_price = IntegerField('Unit Price', validators=[
        DataRequired()
    ])
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=200)
    ])