from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature  # Add itsdangerous imports

import re
from models.models import User, Course
from models.database import db

# Initialize itsdangerous serializer
def get_serializer():
    from app import app  # Import app here to avoid circular import
    return URLSafeTimedSerializer(app.secret_key)

# Generate verification token
def generate_verification_token(email):
    serializer = get_serializer()
    return serializer.dumps(email, salt='email-verify-salt')

# Confirm verification token
def confirm_token(token, expiration=3600):
    serializer = get_serializer()
    try:
        email = serializer.loads(token, salt='email-verify-salt', max_age=expiration)
        return email
    except (SignatureExpired, BadSignature):
        return False

# Send verification email
def send_verification_email(email):
    from app import app, mail  # Import app and mail here to avoid circular import
    token = generate_verification_token(email)
    link = url_for('verify_email', token=token, _external=True)
    msg = Message('Verify Your Email', recipients=[email])
    msg.body = f'Welcome to the World of Gamified Learning !!! \n\nClick the link to verify your email: {link}\n\nThis link will expire in 1 hour.'
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def register_page():
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user is None:
            session.pop('user_id', None)
            return redirect(url_for('login'))
        if user.is_admin:
            return redirect(url_for('admin_courses'))
        return redirect(url_for('courses'))

    errors = {}
    if request.method == 'POST':
        name = request.form['name'].strip()
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        stream = request.form['stream'].strip()
        year = request.form['year'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not name or len(name) < 2:
            errors['name'] = 'Name must be at least 2 characters long.'
        if not username or len(username) < 3:
            errors['username'] = 'Username must be at least 3 characters long.'
        if User.query.filter_by(username=username).first():
            errors['username'] = 'Username already exists!'
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors['email'] = 'Invalid email format.'
        if User.query.filter_by(email=email).first():
            errors['email'] = 'Email already exists!'
        if not stream:
            errors['stream'] = 'Stream is required.'
        if not year:
            errors['year'] = 'Year is required.'
        if len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters long.'
        if password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match!'

        if not errors:
            new_user = User(
                name=name,
                username=username,
                email=email,
                stream=stream,
                year=year,
                password=password,
                is_admin=False,
                is_verified=False
            )
            db.session.add(new_user)
            db.session.commit()

            # Send verification email
            if send_verification_email(email):
                flash('Registration successful! Please check your email to verify your account.', 'success')
            else:
                flash('Registration successful, but failed to send verification email. Please contact support.', 'warning')

            return redirect(url_for('login'))
        return render_template('register.html', errors=errors)

    # Get request
    return render_template('register.html', errors=None)

def login_page():
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user is None:
            session.pop('user_id', None)
            return redirect(url_for('login'))
        if user.is_admin:
            return redirect(url_for('admin_courses'))
        return redirect(url_for('courses'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # if not user.is_verified:
            #     flash('Please verify your email before logging in.')
            #     return redirect(url_for('login'))
            session['user_id'] = user.id
            session['user_level'] = user.level
            session['user_points'] = user.points
            if user.is_admin:
                return redirect(url_for('admin_courses'))
            return redirect(url_for('courses'))
        flash('Invalid credentials!', 'error')

    # Get Request
    return render_template('login.html')

def verify_email():
    token = request.args.get('token')
    if not token:
        flash('Invalid verification link.', 'error')
        return redirect(url_for('login'))

    email = confirm_token(token)
    if email:
        user = User.query.filter_by(email=email).first()
        if user:
            if user.is_verified:
                flash('Your email is already verified.', 'info')
            else:
                user.is_verified = True
                db.session.commit()
                flash('Email verified successfully! Please log in.', 'success')
            return render_template('login.html')
        flash('User not found.', 'error')
    else:
        flash('Verification link is invalid or has expired.', 'error')
    return redirect(url_for('login'))

def logout_page():
    session.pop('user_id', None)
    return redirect(url_for('login'))
