from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import User, Patient, Appointment
from app.main.forms import PatientRegistrationForm, AppointmentForm
from datetime import datetime

@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/index.html', title='Welcome')

@bp.route('/dashboard')
@login_required
def dashboard():
    stats = get_user_stats()
    recent_activities = get_recent_activities()
    upcoming_events = get_upcoming_events()
    return render_template('main/dashboard.html',
                         title='Dashboard',
                         stats=stats,
                         recent_activities=recent_activities,
                         upcoming_events=upcoming_events)

@bp.route('/dashboard/data')
@login_required
def dashboard_data():
    return {
        'stats': get_user_stats(),
        'activities': get_recent_activities(),
        'events': get_upcoming_events()
    }

def get_user_stats():
    stats = {}
    if current_user.role == 'admin':
        stats['total_patients'] = Patient.query.count()
    
    if current_user.role in ['admin', 'doctor', 'receptionist']:
        today = datetime.now().date()
        stats['today_appointments'] = Appointment.query.filter(
            Appointment.appointment_date.cast(db.Date) == today
        ).count()
    
    if current_user.role == 'pharmacist':
        from app.models import Medication
        stats['low_stock_items'] = Medication.query.filter(
            Medication.quantity <= Medication.reorder_level
        ).count()
    
    if current_user.role == 'lab_technician':
        from app.models import LabTest
        stats['pending_tests'] = LabTest.query.filter_by(status='pending').count()
    
    return stats

def get_recent_activities():
    activities = []
    if current_user.role == 'admin':
        # Get recent patient registrations
        recent_patients = Patient.query.order_by(Patient.created_at.desc()).limit(5).all()
        for patient in recent_patients:
            activities.append({
                'title': 'New Patient Registration',
                'description': f'{patient.first_name} {patient.last_name}',
                'time': patient.created_at.strftime('%Y-%m-%d %H:%M'),
                'user': 'System'
            })
    
    # Get recent appointments
    recent_appointments = Appointment.query
    if current_user.role == 'doctor':
        recent_appointments = recent_appointments.filter_by(doctor_id=current_user.id)
    recent_appointments = recent_appointments.order_by(Appointment.created_at.desc()).limit(5).all()
    
    for appointment in recent_appointments:
        activities.append({
            'title': 'New Appointment',
            'description': f'Appointment scheduled for {appointment.patient.first_name} {appointment.patient.last_name}',
            'time': appointment.created_at.strftime('%Y-%m-%d %H:%M'),
            'user': f'Dr. {appointment.doctor.first_name} {appointment.doctor.last_name}'
        })
    
    return activities

def get_upcoming_events():
    events = []
    today = datetime.now().date()
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.query
    if current_user.role == 'doctor':
        upcoming_appointments = upcoming_appointments.filter_by(doctor_id=current_user.id)
    upcoming_appointments = upcoming_appointments.filter(
        Appointment.appointment_date > datetime.now()
    ).order_by(Appointment.appointment_date).limit(5).all()
    
    for appointment in upcoming_appointments:
        events.append({
            'title': 'Appointment',
            'description': f'Patient: {appointment.patient.first_name} {appointment.patient.last_name}',
            'date': appointment.appointment_date.strftime('%Y-%m-%d'),
            'time': appointment.appointment_date.strftime('%H:%M')
        })
    
    return events


@bp.route('/register_patient', methods=['GET', 'POST'])
@login_required
def register_patient():
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            blood_group=form.blood_group.data,
            phone=form.phone.data,
            email=form.email.data,
            address=form.address.data
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient registered successfully!', 'success')
        return redirect(url_for('main.view_patient', patient_id=patient.id))
    return render_template('main/register_patient.html', title='Register Patient', form=form)

@bp.route('/patient/<int:patient_id>')
@login_required
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    appointments = Appointment.query.filter_by(patient_id=patient_id).order_by(Appointment.appointment_date.desc()).all()
    return render_template('main/view_patient.html', title='Patient Details', patient=patient, appointments=appointments)

@bp.route('/schedule_appointment/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def schedule_appointment(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = AppointmentForm()
    
    # Only load doctors for the form choices
    doctors = User.query.filter_by(role='doctor').all()
    form.doctor_id.choices = [(d.id, f'Dr. {d.first_name} {d.last_name}') for d in doctors]
    
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=form.doctor_id.data,
            appointment_date=form.appointment_date.data,
            notes=form.notes.data
        )
        db.session.add(appointment)
        db.session.commit()
        
        # TODO: Send email notification
        
        flash('Appointment scheduled successfully!', 'success')
        return redirect(url_for('main.view_patient', patient_id=patient.id))
    
    return render_template('main/schedule_appointment.html', 
                         title='Schedule Appointment',
                         form=form,
                         patient=patient)

@bp.route('/search_patients')
@login_required
def search_patients():
    query = request.args.get('query', '')
    if query:
        patients = Patient.query.filter(
            (Patient.first_name.ilike(f'%{query}%')) |
            (Patient.last_name.ilike(f'%{query}%')) |
            (Patient.phone.ilike(f'%{query}%'))
        ).all()
    else:
        patients = []
    return render_template('main/search_patients.html', 
                         title='Search Patients',
                         patients=patients,
                         query=query)