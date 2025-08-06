from flask import render_template, redirect, url_for, flash, request, current_app, send_file
from flask_login import login_required, current_user
from app import db
from app.laboratory import bp
from app.laboratory.forms import LabTestForm, TestResultForm
from app.models import LabTest, Patient
from app.utils.decorators import lab_technician_required
from app.utils.helpers import generate_lab_report_pdf
from datetime import datetime

@bp.route('/dashboard')
@login_required
@lab_technician_required
def dashboard():
    # Get pending tests
    pending_tests = LabTest.query.filter_by(status='pending').order_by(
        LabTest.requested_date.desc()).limit(5).all()
    
    # Get today's completed tests
    today = datetime.now().date()
    completed_today = LabTest.query.filter(
        LabTest.status == 'completed',
        db.func.date(LabTest.completed_date) == today
    ).all()
    
    # Get recent test results
    recent_results = LabTest.query.filter_by(status='completed').order_by(
        LabTest.completed_date.desc()).limit(5).all()
    
    return render_template('laboratory/dashboard.html',
                         title='Laboratory Dashboard',
                         pending_tests=pending_tests,
                         completed_today=completed_today,
                         recent_results=recent_results)

@bp.route('/tests')
@login_required
@lab_technician_required
def tests():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')
    
    query = LabTest.query
    if status != 'all':
        query = query.filter_by(status=status)
    
    tests = query.order_by(LabTest.requested_date.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    
    return render_template('laboratory/tests.html',
                         title='Lab Tests',
                         tests=tests,
                         status=status)

@bp.route('/test/new', methods=['GET', 'POST'])
@login_required
@lab_technician_required
def new_test():
    form = LabTestForm()
    if form.validate_on_submit():
        test = LabTest(patient_id=form.patient_id.data,
                      test_type=form.test_type.data,
                      doctor_id=form.doctor_id.data,
                      notes=form.notes.data,
                      requested_by=current_user.id,
                      status='pending')
        db.session.add(test)
        db.session.commit()
        flash('Lab test request created successfully.', 'success')
        return redirect(url_for('laboratory.tests'))
    return render_template('laboratory/new_test.html',
                         title='New Lab Test',
                         form=form)

@bp.route('/test/<int:id>', methods=['GET', 'POST'])
@login_required
@lab_technician_required
def view_test(id):
    test = LabTest.query.get_or_404(id)
    form = TestResultForm(obj=test)
    
    if form.validate_on_submit():
        test.results = form.results.data
        test.normal_range = form.normal_range.data
        test.status = 'completed'
        test.completed_date = datetime.now()
        test.completed_by = current_user.id
        test.remarks = form.remarks.data
        
        db.session.commit()
        flash('Test results updated successfully.', 'success')
        return redirect(url_for('laboratory.tests'))
    
    return render_template('laboratory/view_test.html',
                         title='View Test',
                         test=test,
                         form=form)

@bp.route('/test/<int:id>/report')
@login_required
@lab_technician_required
def generate_report(id):
    test = LabTest.query.get_or_404(id)
    if test.status != 'completed':
        flash('Cannot generate report for incomplete test.', 'warning')
        return redirect(url_for('laboratory.view_test', id=id))
    
    # Generate PDF report
    filename = generate_lab_report_pdf(test)
    return send_file(filename,
                     as_attachment=True,
                     download_name=f'lab_report_{test.id}.pdf')

@bp.route('/patient/<int:patient_id>/history')
@login_required
@lab_technician_required
def patient_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    tests = LabTest.query.filter_by(patient_id=patient_id).order_by(
        LabTest.requested_date.desc()).all()
    
    return render_template('laboratory/patient_history.html',
                         title='Patient Test History',
                         patient=patient,
                         tests=tests)