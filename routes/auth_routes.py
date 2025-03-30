from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import re
from models.models import User, Course
from models.database import db

def register_page():
    errors = {}
    if request.method == 'POST':
        name = request.form['name'].strip()
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        mobile = request.form['mobile'].strip()
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
        if not re.match(r"^[0-9]{10}$", mobile):
            errors['mobile'] = 'Mobile number must be exactly 10 digits.'
        if User.query.filter_by(mobile=mobile).first():
            errors['mobile'] = 'Mobile number already exists!'
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
                mobile=mobile,
                stream=stream,
                year=year,
                password=password,
                is_admin=False
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        return render_template('register.html', errors=errors)
    return render_template('register.html', errors=None)

def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # if not user.is_verified:
            #     flash('Please verify your email before logging in.')
            #     return redirect(url_for('login'))
            session['user_id'] = user.id
            if user.is_admin:
                return redirect(url_for('admin_courses'))
            return redirect(url_for('courses'))
        flash('Invalid credentials!')
    return render_template('login.html')

def logout_page():
    session.pop('user_id', None)
    return redirect(url_for('login'))