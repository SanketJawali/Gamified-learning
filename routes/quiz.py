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
        print(total_questions)

        # Check each submitted answer
        for question_id, correct_index in answer_key.items():
            user_answer = request.form.get(question_id, '').strip()

            print(f"\nChecking question {question_id}:")
            print(f"- Correct index: {correct_index} (type: {type(correct_index)})")
            print(f"- User answer: '{user_answer}' (type: {type(user_answer)})")

            try:
                user_answer_int = int(user_answer)
                correct_index_int = int(correct_index)

                if user_answer_int == correct_index_int:
                    print("✅ CORRECT MATCH")
                    correct_answers += 1
                else:
                    print("❌ WRONG ANSWER")
            except (ValueError, TypeError) as e:
                print(f"⚠️ INVALID ANSWER: {e}")
                continue

        print(f"\n=== FINAL COUNT ===")
        print(f"Correct answers: {correct_answers}/{total_questions}")

        # Calculate results
        score = (correct_answers / total_questions) * 100
        xp_earned = correct_answers * answer_data['xp_per_question']

        # flash the result
        flash(f'Quiz submitted. You earned {xp_earned} points')

        # Update user's progress
        # try:
        #     user.xp += xp_earned

        #     # Mark lesson as completed if passing score (e.g., 70%)
        #     if score >= 70:
        #         completion = Completion(
        #             user_id=user.id,
        #             lesson_id=lesson_id,
        #             completed_at=datetime.utcnow(),
        #             score=score
        #         )
        #         db.session.add(completion)

        #     db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     current_app.logger.error(f"Error updating user progress: {e}")
        #     flash("Error saving your results", "error")

        # Render results template
        # return render_template()

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
