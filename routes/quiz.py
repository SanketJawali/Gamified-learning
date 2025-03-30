from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import re
from models.models import User, Course
from models.database import db

def quiz_page(lesson_id=None):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if not user.level:
        return redirect(url_for('select_level'))

    quizzes = {
        'Beginner': {
            1: {'question': 'What is Python?', 'answer': 'programming language', 'points': 10},
            2: {'question': 'How do you assign a value?', 'answer': '=', 'points': 15},
            3: {'question': 'Which loop repeats a block?', 'answer': 'for', 'points': 20}
        },
        'Intermediate': {
            1: {'question': 'What keyword defines a function?', 'answer': 'def', 'points': 20},
            2: {'question': 'How do you create a list?', 'answer': '[]', 'points': 25},
            3: {'question': 'What checks a condition?', 'answer': 'if', 'points': 30}
        },
        'Advanced': {
            1: {'question': 'What is a class?', 'answer': 'blueprint', 'points': 30},
            2: {'question': 'What modifies a function?', 'answer': 'decorator', 'points': 35},
            3: {'question': 'What yields values one at a time?', 'answer': 'generator', 'points': 40}
        }
    }
    if request.method == 'POST':
        answer = request.form['answer'].lower()
        if answer == quizzes[user.level][lesson_id]['answer']:
            user.points += quizzes[user.level][lesson_id]['points']
            completed = user.completed_lessons + f",{lesson_id}" if user.completed_lessons else str(lesson_id)
            user.completed_lessons = completed
            db.session.commit()
            flash(f'Correct! Earned {quizzes[user.level][lesson_id]["points"]} points!')
        else:
            flash('Wrong answer! Try again.')
        return redirect(url_for('lessons'))
    return render_template('quiz.html', user=user, quiz=quizzes[user.level][lesson_id])
