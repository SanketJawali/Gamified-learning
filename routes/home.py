from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import re
from models.models import User, Course
from models.database import db

def home_page():
    # if 'user_id' in session:
    #     user = db.session.get(User, session['user_id'])
    #     if user is None:
    #         session.pop('user_id', None)
    #         return redirect(url_for('login'))
    #     if user.is_admin:
    #         return redirect(url_for('admin_courses'))
    #     return redirect(url_for('courses'))
    return render_template('home.html')
