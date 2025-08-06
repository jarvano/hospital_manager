from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.admin.forms import UserEditForm, SystemSettingsForm
from app.models import User, Patient, Appointment, Bill
from app.utils.decorators import admin_required
from datetime import datetime, timedelta

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get statistics for dashboard
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    total_doctors = User.query.filter_by(role='doctor').count()
    
    # Get today's appointments
    today = datetime.now().date()
    today_appointments = Appointment.query.filter(
        db.func.date(Appointment.appointment_date) == today
    ).all()
    
    # Get recent bills
    recent_bills = Bill.query.order_by(Bill.bill_date.desc()).limit(5).all()
    
    # Calculate revenue for the last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    monthly_revenue = db.session.query(db.func.sum(Bill.total_amount)).filter(
        Bill.bill_date >= thirty_days_ago,
        Bill.payment_status == 'paid'
    ).scalar() or 0
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         total_patients=total_patients,
                         total_appointments=total_appointments,
                         total_doctors=total_doctors,
                         today_appointments=today_appointments,
                         recent_bills=recent_bills,
                         monthly_revenue=monthly_revenue)

@bp.route('/users')
@login_required
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    return render_template('admin/manage_users.html',
                         title='Manage Users',
                         users=users)

@bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)
    
    if form.validate_on_submit():
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.role = form.role.data
        user.is_active = form.is_active.data
        
        if form.password.data:
            user.set_password(form.password.data)
        
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/edit_user.html',
                         title='Edit User',
                         form=form,
                         user=user)

@bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.manage_users'))

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def system_settings():
    form = SystemSettingsForm()
    if form.validate_on_submit():
        # Update system settings
        # TODO: Implement settings storage
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('admin.system_settings'))
    return render_template('admin/settings.html',
                         title='System Settings',
                         form=form)

@bp.route('/reports')
@login_required
@admin_required
def reports():
    report_type = request.args.get('type', 'revenue')
    start_date = request.args.get('start_date', 
                                (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    
    # Generate report based on type
    if report_type == 'revenue':
        data = generate_revenue_report(start_date, end_date)
    elif report_type == 'appointments':
        data = generate_appointment_report(start_date, end_date)
    else:
        data = {}
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(data)
    
    return render_template('admin/reports.html',
                         title='Reports',
                         report_type=report_type,
                         start_date=start_date,
                         end_date=end_date,
                         data=data)

def generate_revenue_report(start_date, end_date):
    # TODO: Implement revenue report generation
    return {}

def generate_appointment_report(start_date, end_date):
    # TODO: Implement appointment report generation
    return {}