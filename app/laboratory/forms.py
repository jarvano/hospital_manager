from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, Optional

class LabTestForm(FlaskForm):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    test_type = SelectField('Test Type', choices=[
        ('blood_test', 'Blood Test'),
        ('urine_test', 'Urine Test'),
        ('x_ray', 'X-Ray'),
        ('ultrasound', 'Ultrasound'),
        ('ct_scan', 'CT Scan'),
        ('mri', 'MRI'),
        ('ecg', 'ECG'),
        ('endoscopy', 'Endoscopy'),
        ('biopsy', 'Biopsy'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    doctor_id = IntegerField('Referring Doctor ID', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency')
    ], default='routine')
    notes = TextAreaField('Additional Notes', validators=[
        Optional(),
        Length(max=500)
    ])
    sample_type = StringField('Sample Type', validators=[
        Optional(),
        Length(max=100)
    ])
    fasting_required = SelectField('Fasting Required', choices=[
        ('yes', 'Yes'),
        ('no', 'No')
    ], default='no')

class TestResultForm(FlaskForm):
    results = TextAreaField('Test Results', validators=[
        DataRequired(),
        Length(max=1000)
    ])
    normal_range = StringField('Normal Range', validators=[
        Optional(),
        Length(max=100)
    ])
    remarks = TextAreaField('Remarks', validators=[
        Optional(),
        Length(max=500)
    ])
    performed_by = StringField('Test Performed By', validators=[
        Optional(),
        Length(max=100)
    ])
    verified_by = StringField('Results Verified By', validators=[
        Optional(),
        Length(max=100)
    ])
    equipment_used = StringField('Equipment Used', validators=[
        Optional(),
        Length(max=100)
    ])
    methodology = StringField('Test Methodology', validators=[
        Optional(),
        Length(max=200)
    ])
    attachments = StringField('Attachments/Images', validators=[
        Optional(),
        Length(max=200)
    ])

class TestSearchForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[
        Optional(),
        Length(max=100)
    ])
    test_type = SelectField('Test Type', choices=[
        ('', 'All'),
        ('blood_test', 'Blood Test'),
        ('urine_test', 'Urine Test'),
        ('x_ray', 'X-Ray'),
        ('ultrasound', 'Ultrasound'),
        ('ct_scan', 'CT Scan'),
        ('mri', 'MRI'),
        ('ecg', 'ECG'),
        ('endoscopy', 'Endoscopy'),
        ('biopsy', 'Biopsy'),
        ('other', 'Other')
    ])
    status = SelectField('Status', choices=[
        ('', 'All'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
    date_from = DateTimeField('Date From', format='%Y-%m-%d', validators=[Optional()])
    date_to = DateTimeField('Date To', format='%Y-%m-%d', validators=[Optional()])