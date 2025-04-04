from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
import re
from models.models import User, Course
from models.database import db
from routes.helpers import get_quiz, get_quiz_answers

def quiz_page(quiz_id):
    if 'user_id' not in session:
            return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if not user.level:
        return redirect(url_for('quiz'))

    if request.method == 'POST':
        # Load the quiz answers
        answer_filename = f"answer_{quiz_id}"
        answer_data = get_quiz_answers(answer_filename)
        if not answer_data:
            abort(404, description="Answer key not found")


    # Handle Get request
    filename = f"quiz_{quiz_id}"
    quiz_data = get_quiz(filename)

    if not quiz_data:
        abort(404, description="Quiz not found")

    # Pass the specific parts of quiz_data separately
    return render_template(
        'quiz.html',
        user=user,
        quiz_id=quiz_id,
        points=quiz_data.get('points', 0),
        time_limit=quiz_data.get('time_limit_minutes', 0),
        questions=quiz_data.get('questions', [])  # Pass just the questions array
    )


def quiz_ans_page(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if not user.level:
        return redirect(url_for('quiz'))

    # Load quiz and answer data
    filename = f"quiz_{quiz_id}"
    quiz_data = get_quiz(filename)
    if not quiz_data:
        abort(404, description="Quiz not found")

    answer_filename = f"answer_{quiz_id}"
    answer_data = get_quiz_answers(answer_filename)
    if not answer_data:
        abort(404, description="Answer key not found")

    questions = quiz_data.get('questions', [])
    answer_key = answer_data.get('answers', {})

    if request.method == 'POST':
        # Store user's answers in session and calculate score
        user_answers = {}
        correct_answers = 0
        total_questions = len(answer_key)

        for question_id, correct_index in answer_key.items():
            user_answer = request.form.get(question_id, '').strip()
            user_answers[question_id] = user_answer
            try:
                if int(user_answer) == int(correct_index):
                    correct_answers += 1
            except (ValueError, TypeError):
                continue

        # Check if lesson was already completed
        completed_lessons = user.completed_lessons.split(',') if user.completed_lessons else []
        is_lesson_completed = str(quiz_id) in completed_lessons

        # Calculate results
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        xp_earned = correct_answers * answer_data['xp_per_question'] if not is_lesson_completed else 0

        # Update user's progress
        try:
            if not is_lesson_completed and score >= 40:
                # First time passing - award points and mark completed
                user.points += xp_earned
                completed_lessons.append(str(quiz_id))
                user.completed_lessons = ','.join(completed_lessons)
                flash(f'Congratulations! You earned {xp_earned} points for completing this lesson!', 'success')
            elif is_lesson_completed:
                flash('You have already completed this lesson. No additional points awarded.', 'info')
            else:
                flash(f'You scored {score:.1f}%. Try again to pass and earn points!', 'warning')

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # current_app.logger.error(f"Failed to update user progress: {e}")
            flash('Error saving your results. Please try again.', 'error')

        # Check for level up
        if user.check_level_up():
            db.session.commit()  # If you're not committing elsewhere
            flash(f'Level Up! You are now Level {user.level}!', 'success')

        # Storing the level and points in session
        session['user_level'] = user.level
        session['user_points'] = user.points
        session['user_answers'] = user_answers  # Store user answers in session
        session['answer_key'] = answer_key      # Store correct answers in session
        session['questions'] = questions

    # Retrieve data from session
        user_answers = session.get('user_answers', {})
        answer_key = session.get('answer_key', {})
        questions = session.get('questions', [])

        if not user_answers or not answer_key or not questions:
            flash('Quiz data not found. Please retake the quiz.', 'error')
            return redirect(url_for('quiz', quiz_id=quiz_id))

        return render_template(
            'quiz_ans.html',
            user=user,
            quiz_id=quiz_id,
            points=0,  # Adjust as needed
            time_limit=5,  # Adjust as needed
            questions=questions,
            user_answers=user_answers,
            answer_key=answer_key,
            submitted=True
            )
    return redirect(url_for('quiz', quiz_id=quiz_id))
