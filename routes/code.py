from flask import Flask, render_template, request, redirect, url_for, flash, session
from routes.helpers import *
from models.models import User
from models.database import db

def code_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if user.is_admin:
        return redirect(url_for('admin_courses'))

    return render_template('code.html', user=user)



