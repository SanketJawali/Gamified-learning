from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import re
from models.models import User, Course
from models.database import db

def register_page():
    if not request.headers.get('HX-Request'):
        return 
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user is None:
            session.pop('user_id', None)
            return redirect(url_for('home'))

        if user.is_admin:
            return '', 302, {'HX-Redirect': url_for('admin_courses')}
        return '', 302, {'HX-Redirect': url_for('courses')}  # HTMX client-side redirect

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
                is_admin=False
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return '', 302, {'HX-Redirect': url_for('login')}  # HTMX client-side redirect
        return render_template('register.html', errors=errors)

    # Get request
    return render_template('register.html', errors=None)

def login_page():
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user is None:
            session.pop('user_id', None)
            return redirect(url_for('home'))

        if request.headers.get('HX-Request'):  # Check if HTMX request
            if user.is_admin:
                return '', 302, {'HX-Redirect': url_for('admin_courses')}
            return '', 302, {'HX-Redirect': url_for('courses')}  # HTMX client-side redirect
        else:
            return redirect(url_for('home'))

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

            if request.headers.get('HX-Request'):  # Check if HTMX request
                if user.is_admin:
                    return redirect(url_for('admin_courses'))
                return '', 302, {'HX-Redirect': url_for('courses')}  # HTMX client-side redirect
        flash('Invalid credentials!', 'error')

    # Get Request
    return render_template('login.html')

def logout_page():
    session.pop('user_id', None)
    return redirect(url_for('home'))
