from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.doctor import bp
from app.doctor.forms import PrescriptionForm, DiagnosisForm
from app.models import Appointment, Patient, Prescription, PrescriptionMedication, Medication
from app.utils.decorators import doctor_required
from datetime import datetime, timedelta

@bp.route('/dashboard')
@login_required
@doctor_required
def dashboard():
    # Get today's appointments
    today = datetime.now().date()
    today_appointments = Appointment.query.filter(
        Appointment.doctor_id == current_user.id,
        db.func.date(Appointment.appointment_date) == today
    ).order_by(Appointment.appointment_date).all()
    
    # Get recent prescriptions
    recent_prescriptions = Prescription.query.filter(
        Prescription.doctor_id == current_user.id
    ).order_by(Prescription.prescription_date.desc()).limit(5).all()
    
    # Get recent lab results
    recent_lab_results = LabTest.query.filter(
        LabTest.doctor_id == current_user.id,
        LabTest.status == 'completed'
    ).order_by(LabTest.updated_at.desc()).limit(5).all()
    
    # Get statistics
    stats = get_doctor_stats()
    
    return render_template('doctor/dashboard.html',
                         title='Doctor Dashboard',
                         today_appointments=today_appointments,
                         recent_prescriptions=recent_prescriptions,
                         recent_lab_results=recent_lab_results,
                         stats=stats)

@bp.route('/appointments')
@login_required
@doctor_required
def appointments():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'scheduled')
    
    query = Appointment.query.filter(Appointment.doctor_id == current_user.id)
    
    if status != 'all':
        query = query.filter(Appointment.status == status)
    
    appointments = query.order_by(Appointment.appointment_date.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    
    return render_template('doctor/appointments.html',
                         title='My Appointments',
                         appointments=appointments,
                         status=status)

@bp.route('/appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
@doctor_required
def view_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.doctor_id != current_user.id:
        flash('You do not have permission to view this appointment.', 'danger')
        return redirect(url_for('doctor.appointments'))
    
    diagnosis_form = DiagnosisForm()
    prescription_form = PrescriptionForm()
    
    if diagnosis_form.validate_on_submit() and prescription_form.validate_on_submit():
        # Update appointment status and diagnosis
        appointment.status = 'completed'
        appointment.diagnosis = diagnosis_form.diagnosis.data
        appointment.notes = diagnosis_form.notes.data
        
        # Create prescription if medications are provided
        if prescription_form.medications.data:
            prescription = Prescription(
                patient_id=appointment.patient_id,
                doctor_id=current_user.id,
                diagnosis=diagnosis_form.diagnosis.data,
                notes=prescription_form.notes.data
            )
            db.session.add(prescription)
            
            for med_data in prescription_form.medications.data:
                medication = PrescriptionMedication(
                    prescription=prescription,
                    medication_id=med_data['medication_id'],
                    dosage=med_data['dosage'],
                    frequency=med_data['frequency'],
                    duration=med_data['duration']
                )
                db.session.add(medication)
        
        # Create lab tests if requested
        if diagnosis_form.lab_tests.data:
            for test_data in diagnosis_form.lab_tests.data:
                lab_test = LabTest(
                    patient_id=appointment.patient_id,
                    doctor_id=current_user.id,
                    test_type=test_data['test_type'],
                    notes=test_data['notes']
                )
                db.session.add(lab_test)
        
        db.session.commit()
        flash('Consultation completed successfully.', 'success')
        return redirect(url_for('doctor.dashboard'))
    
    # Get patient history
    previous_appointments = Appointment.query.filter(
        Appointment.patient_id == appointment.patient_id,
        Appointment.id != appointment.id,
        Appointment.status == 'completed'
    ).order_by(Appointment.appointment_date.desc()).all()
    
    previous_prescriptions = Prescription.query.filter(
        Prescription.patient_id == appointment.patient_id
    ).order_by(Prescription.prescription_date.desc()).all()
    
    return render_template('doctor/view_appointment.html',
                         title='Appointment Details',
                         appointment=appointment,
                         diagnosis_form=diagnosis_form,
                         prescription_form=prescription_form,
                         previous_appointments=previous_appointments,
                         previous_prescriptions=previous_prescriptions)

@bp.route('/prescriptions')
@login_required
@doctor_required
def prescriptions():
    page = request.args.get('page', 1, type=int)
    prescriptions = Prescription.query.filter_by(doctor_id=current_user.id)\
        .order_by(Prescription.prescription_date.desc())\
        .paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'],
                 error_out=False)
    return render_template('doctor/prescriptions.html',
                         title='My Prescriptions',
                         prescriptions=prescriptions)

@bp.route('/prescription/<int:prescription_id>')
@login_required
@doctor_required
def view_prescription(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    if prescription.doctor_id != current_user.id:
        flash('You do not have permission to view this prescription.', 'danger')
        return redirect(url_for('doctor.prescriptions'))
    return render_template('doctor/view_prescription.html',
                         title='Prescription Details',
                         prescription=prescription)