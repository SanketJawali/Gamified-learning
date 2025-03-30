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
    lessons = {
        'Beginner': [
            {'id': 1, 'title': 'Python Basics', 'points': 10},
            {'id': 2, 'title': 'Simple Variables', 'points': 15},
            {'id': 3, 'title': 'Basic Loops', 'points': 20}
        ],
        'Intermediate': [
            {'id': 1, 'title': 'Functions', 'points': 20},
            {'id': 2, 'title': 'Lists and Dictionaries', 'points': 25},
            {'id': 3, 'title': 'Conditionals', 'points': 30}
        ],
        'Advanced': [
            {'id': 1, 'title': 'OOP Concepts', 'points': 30},
            {'id': 2, 'title': 'Decorators', 'points': 35},
            {'id': 3, 'title': 'Generators', 'points': 40}
        ]
    }
    return render_template('lessons.html', user=user, lessons=lessons[user.level])