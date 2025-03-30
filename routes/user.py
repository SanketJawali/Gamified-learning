from flask import render_template, redirect, url_for,session,request,flash
from models.models import User
from models.database import db

def profile_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    return render_template('profile.html', user=user)

def contact_support_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    return render_template('contact_support.html', user=user)

def select_level_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if request.method == 'POST':
        level = request.form['level']
        if level in ['Beginner', 'Intermediate', 'Advanced']:
            user.level = level
            db.session.commit()
            return redirect(url_for('lessons'))
        flash('Invalid level selected.')
    return render_template('select_level.html', user=user)