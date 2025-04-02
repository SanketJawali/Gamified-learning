from flask import render_template, redirect, url_for, session
from models.models import User
from models.database import db

def lessons_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if not user.level:
        return redirect(url_for('select_level'))
    lessons = [
        {'id': 1, 'title': 'Introduction to Python'},
        {'id': 2, 'title': 'Variables and Data Types'},
        {'id': 3, 'title': 'Operators & Expressions'},
        {'id': 4, 'title': 'Conditional Statements'},
        {'id': 5, 'title': 'Loops in Python'},
        {'id': 6, 'title': 'Functions'},
        {'id': 7, 'title': 'Lists, Tuples, and Dictionaries'},
        {'id': 8, 'title': 'File Handling in Python'},
        {'id': 9, 'title': 'Exception Handling'},
        {'id': 10, 'title': 'Python Classes and Objects'},
        {'id': 11, 'title': 'Python Iterators'},
        {'id': 12, 'title': 'Inheritance'},
        {'id': 13, 'title': 'Polymorphism'},
        {'id': 14, 'title': 'Encapsulation'}
    ]
    return render_template('lessons.html', user=user, lessons=lessons)
