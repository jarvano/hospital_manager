from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FieldList, FormField, IntegerField
from wtforms.validators import DataRequired, Length, Optional

class MedicationEntryForm(FlaskForm):
    medication_id = SelectField('Medication', coerce=int, validators=[DataRequired()])
    dosage = StringField('Dosage', validators=[DataRequired(), Length(max=50)])
    frequency = SelectField('Frequency', choices=[
        ('once_daily', 'Once Daily'),
        ('twice_daily', 'Twice Daily'),
        ('thrice_daily', 'Three Times Daily'),
        ('four_times_daily', 'Four Times Daily'),
        ('as_needed', 'As Needed (PRN)'),
        ('before_bed', 'Before Bed'),
        ('with_meals', 'With Meals')
    ], validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired(), Length(max=50)])
    instructions = TextAreaField('Special Instructions', validators=[Optional(), Length(max=200)])

class PrescriptionForm(FlaskForm):
    diagnosis = TextAreaField('Diagnosis', validators=[DataRequired(), Length(max=500)])
    medications = FieldList(FormField(MedicationEntryForm), min_entries=1)
    notes = TextAreaField('Additional Notes', validators=[Optional(), Length(max=500)])

class DiagnosisForm(FlaskForm):
    notes = TextAreaField('Diagnosis Notes', validators=[DataRequired(), Length(max=1000)])
    follow_up_days = IntegerField('Follow-up After (Days)', validators=[Optional()])
    lab_tests_required = TextAreaField('Required Lab Tests', validators=[Optional(), Length(max=500)])
    recommendations = TextAreaField('Recommendations', validators=[Optional(), Length(max=500)])