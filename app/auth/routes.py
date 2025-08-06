from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        if not user.is_active:
            flash('Your account has been deactivated. Please contact admin.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            if user.role == 'admin':
                next_page = url_for('admin.dashboard')
            elif user.role == 'doctor':
                next_page = url_for('doctor.dashboard')
            elif user.role == 'pharmacist':
                next_page = url_for('pharmacy.dashboard')
            elif user.role == 'lab_technician':
                next_page = url_for('laboratory.dashboard')
            else:
                next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.role == 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.email = form.email.data
        user.set_password(form.password.data)
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.role = form.role.data
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {user.email} has been registered successfully.', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('auth/register.html', title='Register User', form=form)