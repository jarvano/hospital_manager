from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.pharmacy import bp
from app.pharmacy.forms import MedicationForm, DispenseMedicationForm, StockUpdateForm
from app.models import Medication, Prescription, PrescriptionMedication
from app.utils.decorators import pharmacist_required
from datetime import datetime

@bp.route('/dashboard')
@login_required
@pharmacist_required
def dashboard():
    # Get low stock medications (less than 10 units)
    low_stock = Medication.query.filter(Medication.stock_quantity < 10).all()
    
    # Get pending prescriptions
    pending_prescriptions = Prescription.query.filter_by(status='pending').order_by(
        Prescription.prescription_date.desc()).limit(5).all()
    
    # Get recently dispensed prescriptions
    recent_dispensed = Prescription.query.filter_by(status='dispensed').order_by(
        Prescription.updated_at.desc()).limit(5).all()
    
    return render_template('pharmacy/dashboard.html',
                         title='Pharmacy Dashboard',
                         low_stock=low_stock,
                         pending_prescriptions=pending_prescriptions,
                         recent_dispensed=recent_dispensed)

@bp.route('/medications')
@login_required
@pharmacist_required
def medications():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Medication.query
    if search:
        query = query.filter(Medication.name.ilike(f'%{search}%'))
    
    medications = query.order_by(Medication.name).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    
    return render_template('pharmacy/medications.html',
                         title='Medications',
                         medications=medications,
                         search=search)

@bp.route('/medication/add', methods=['GET', 'POST'])
@login_required
@pharmacist_required
def add_medication():
    form = MedicationForm()
    if form.validate_on_submit():
        medication = Medication(name=form.name.data,
                              description=form.description.data,
                              unit_price=form.unit_price.data,
                              stock_quantity=form.stock_quantity.data,
                              category=form.category.data,
                              manufacturer=form.manufacturer.data)
        db.session.add(medication)
        db.session.commit()
        flash('Medication added successfully.', 'success')
        return redirect(url_for('pharmacy.medications'))
    return render_template('pharmacy/add_medication.html',
                         title='Add Medication',
                         form=form)

@bp.route('/medication/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@pharmacist_required
def edit_medication(id):
    medication = Medication.query.get_or_404(id)
    form = MedicationForm(obj=medication)
    if form.validate_on_submit():
        medication.name = form.name.data
        medication.description = form.description.data
        medication.unit_price = form.unit_price.data
        medication.stock_quantity = form.stock_quantity.data
        medication.category = form.category.data
        medication.manufacturer = form.manufacturer.data
        db.session.commit()
        flash('Medication updated successfully.', 'success')
        return redirect(url_for('pharmacy.medications'))
    return render_template('pharmacy/edit_medication.html',
                         title='Edit Medication',
                         form=form,
                         medication=medication)

@bp.route('/prescriptions')
@login_required
@pharmacist_required
def prescriptions():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')
    
    query = Prescription.query
    if status != 'all':
        query = query.filter_by(status=status)
    
    prescriptions = query.order_by(Prescription.prescription_date.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    
    return render_template('pharmacy/prescriptions.html',
                         title='Prescriptions',
                         prescriptions=prescriptions,
                         status=status)

@bp.route('/prescription/<int:id>/dispense', methods=['GET', 'POST'])
@login_required
@pharmacist_required
def dispense_prescription(id):
    prescription = Prescription.query.get_or_404(id)
    if prescription.status == 'dispensed':
        flash('This prescription has already been dispensed.', 'warning')
        return redirect(url_for('pharmacy.prescriptions'))
    
    form = DispenseMedicationForm()
    
    if form.validate_on_submit():
        # Update medication stock and mark prescription as dispensed
        for med in prescription.medications:
            medication = med.medication
            if medication.stock_quantity < med.quantity:
                flash(f'Insufficient stock for {medication.name}', 'danger')
                return redirect(url_for('pharmacy.dispense_prescription', id=id))
            medication.stock_quantity -= med.quantity
        
        prescription.status = 'dispensed'
        prescription.dispensed_by = current_user.id
        prescription.dispensed_at = datetime.now()
        prescription.dispensing_notes = form.notes.data
        
        db.session.commit()
        flash('Prescription dispensed successfully.', 'success')
        return redirect(url_for('pharmacy.prescriptions'))
    
    return render_template('pharmacy/dispense_prescription.html',
                         title='Dispense Prescription',
                         prescription=prescription,
                         form=form)

@bp.route('/stock/update', methods=['GET', 'POST'])
@login_required
@pharmacist_required
def update_stock():
    form = StockUpdateForm()
    if form.validate_on_submit():
        medication = Medication.query.get(form.medication_id.data)
        if medication:
            if form.operation.data == 'add':
                medication.stock_quantity += form.quantity.data
            else:  # subtract
                if medication.stock_quantity >= form.quantity.data:
                    medication.stock_quantity -= form.quantity.data
                else:
                    flash('Insufficient stock quantity.', 'danger')
                    return redirect(url_for('pharmacy.update_stock'))
            
            db.session.commit()
            flash('Stock updated successfully.', 'success')
            return redirect(url_for('pharmacy.medications'))
    
    return render_template('pharmacy/update_stock.html',
                         title='Update Stock',
                         form=form)