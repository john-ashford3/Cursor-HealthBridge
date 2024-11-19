from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.auth import auth
from app.auth.forms import (LoginForm, RegistrationForm, 
                          PhysicianRegistrationForm, RequestResetForm, 
                          ResetPasswordForm)
from app.models.user import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user = User(
            name=form.name.data,
            email=form.email.data.lower(),
            password=hashed_password,
            is_physician=(form.user_type.data == 'physician')
        )
        
        if user.is_physician:
            user.physician_type = form.physician_type.data
            user.specialization = form.specialization.data
            user.license_number = form.license_number.data
        
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/register/physician', methods=['GET', 'POST'])
def register_physician():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = PhysicianRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        physician = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            is_physician=True,
            physician_type=form.physician_type.data,
            specialization=form.specialization.data,
            license_number=form.license_number.data,
            years_of_experience=form.years_of_experience.data
        )
        db.session.add(physician)
        db.session.commit()
        flash('Your physician account has been created! You are now able to log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_physician.html', title='Register as Physician', form=form)
