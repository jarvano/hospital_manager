from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class MedicationForm(FlaskForm):
    name = StringField('Medication Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=500)
    ])
    unit_price = DecimalField('Unit Price', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    stock_quantity = IntegerField('Stock Quantity', validators=[
        DataRequired(),
        NumberRange(min=0)
    ])
    category = SelectField('Category', choices=[
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('cream', 'Cream'),
        ('ointment', 'Ointment'),
        ('drops', 'Drops'),
        ('inhaler', 'Inhaler'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    manufacturer = StringField('Manufacturer', validators=[
        Optional(),
        Length(max=100)
    ])
    reorder_level = IntegerField('Reorder Level', validators=[
        Optional(),
        NumberRange(min=0)
    ])
    storage_location = StringField('Storage Location', validators=[
        Optional(),
        Length(max=50)
    ])

class DispenseMedicationForm(FlaskForm):
    notes = TextAreaField('Dispensing Notes', validators=[
        Optional(),
        Length(max=500)
    ])

class StockUpdateForm(FlaskForm):
    medication_id = SelectField('Medication', coerce=int, validators=[DataRequired()])
    operation = SelectField('Operation', choices=[
        ('add', 'Add Stock'),
        ('subtract', 'Remove Stock')
    ], validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(),
        NumberRange(min=1)
    ])
    batch_number = StringField('Batch Number', validators=[
        Optional(),
        Length(max=50)
    ])
    expiry_date = StringField('Expiry Date', validators=[
        Optional(),
        Length(max=10)
    ])
    notes = TextAreaField('Notes', validators=[
        Optional(),
        Length(max=200)
    ])