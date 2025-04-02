from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
import re
from models.models import User, Course
from models.database import db
from routes.helpers import get_quiz, get_quiz_answers

def quiz_page(lesson_id):
    if 'user_id' not in session:
            return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if not user.level:
        return redirect(url_for('select_level'))

    if request.method == 'POST':
        # Load the quiz answers
        answer_filename = f"answer_{lesson_id}"
        answer_data = get_quiz_answers(answer_filename)
        if not answer_data:
            abort(404, description="Answer key not found")

        # Calculate score
        correct_answers = 0
        answer_key = answer_data.get('answers', {})
        total_questions = len(answer_data['answers'])

        # Check each submitted answer
        for question_id, correct_index in answer_key.items():
            user_answer = request.form.get(question_id, '').strip()

            user_answer_int = int(user_answer)
            correct_index_int = int(correct_index)
            correct_answers += 1

        # Calculate results
        score = (correct_answers / total_questions) * 100
        xp_earned = correct_answers * answer_data['xp_per_question']

        # Update user's points in database
        try:
            user.points += xp_earned

            # Update completed lessons if passing score (e.g., 70%)
            if score >= 70:
                completed_lessons = user.completed_lessons.split(',') if user.completed_lessons else []
                if str(lesson_id) not in completed_lessons:
                    completed_lessons.append(str(lesson_id))
                    user.completed_lessons = ','.join(completed_lessons)

            db.session.commit()
            flash(f'Quiz submitted successfully! You earned {xp_earned} points. Total points: {user.points}', 'success')
        except Exception as e:
            db.session.rollback()
            # current_app.logger.error(f"Failed to update user points: {e}")
            flash('Error saving your results. Please try again.', 'error')

    # Handle Get request
    filename = f"quiz_{lesson_id}"
    quiz_data = get_quiz(filename)

    if not quiz_data:
            abort(404, description="Quiz not found")

    # Pass the specific parts of quiz_data separately
    return render_template(
        'quiz.html',
        user=user,
        quiz_id=lesson_id,
        points=quiz_data.get('points', 0),
        time_limit=quiz_data.get('time_limit_minutes', 0),
        questions=quiz_data.get('question', [])  # Pass just the questions array
    )
