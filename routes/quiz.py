from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
from models.models import User, Chapter, UserChapterProgress
from datetime import datetime
from models.database import db
from routes.helpers import get_chapter_content,get_quiz_answers
from quiz_generator import generate_quiz

def quiz_page(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if not user.level:
        return redirect(url_for('quiz'))
    
    return render_template('quiz.html', user=user, quiz_id=quiz_id)

def quiz_logic_page(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if not user.level:
        return redirect(url_for('quiz'))

    # Handle GET request: Generate quiz and redirect to quiz.html
    if request.method == 'GET':
        try:
            # Get chapter content

            # Get course_id from session
            course_id = session['current_course_id']
            content = get_chapter_content(course_id, quiz_id)['content']
            quiz = generate_quiz(content)
            
            # Enhanced validation
            if not quiz:
                raise ValueError("Quiz generation failed")
            if not isinstance(quiz, dict):
                raise ValueError("Invalid quiz format")
            if 'questions' not in quiz:
                raise ValueError("No questions found in quiz")
            questions = quiz.get('questions', [])
            if not isinstance(questions, list) or len(questions) != 8:
                raise ValueError(f"Expected 8 questions, got {len(questions)}")

            # Validate each question's structure
            for i, question in enumerate(questions):
                if not all(key in question for key in ['Question', 'Options', 'Answer']):
                    raise ValueError(f"Missing required fields in question {i}")
                if not isinstance(question['Options'], list) or len(question['Options']) != 4:
                    raise ValueError(f"Invalid options in Question {i}")
            
            # Store quiz and answer key in session
            session['quiz'] = quiz
            answer_key = {f"question_{idx+1}": q["Answer"] for idx, q in enumerate(quiz["questions"])}
            session['answers'] = answer_key
            
            return render_template('quiz_logic.html', user=user, quiz=quiz, quiz_id=quiz_id)
        
        except Exception as e:
            print(f"Error in quiz generation: {str(e)}")
            return render_template('error.html', message=f"Error generating quiz: {str(e)}"), 500

    # Handle POST request: Check answers and render quiz_ans.html
    elif request.method == 'POST':
        if 'quiz' not in session or 'answers' not in session:
            flash("Quiz session expired. Please restart the quiz.", "error")
            return redirect(url_for('quiz', quiz_id=quiz_id))
        
        quiz = session['quiz']
        answers = session['answers']
        # print(answers)
        
        user_answers = {}
        # Collect user answers from the form for all 8 questions
        for i in range(1, 9):  # 8 questions
            user_answer = request.form.get(f'question_q{i}')
            if user_answer is not None:
                try:
                    user_answers[f'question_{i}'] = int(user_answer)  # Convert to index (0, 1, 2, 3)
                except ValueError:
                    user_answers[f'question_{i}'] = -1  # Invalid input
        # print(user_answers)
        
        # Compare with correct answers and calculate score for all 8 questions
        score = 0
        results = {}
        for q in range(1, 9):  # Loop over all 8 questions
            user_ans = user_answers.get(f'question_{q}')
            # qid = question_id.get(f'question_{q}')
            correct_ans = answers.get(f'question_{q}')
            is_correct = (user_ans == correct_ans if user_ans is not None else False)
            results[f'question_{q}'] = {
                'user_answer': user_ans,
                'correct_answer': correct_ans,
                'is_correct': is_correct
            }
            if is_correct and user_ans is not None:
                score += 1
        earned_points = score * 10
        user.points += earned_points
        
        # Optionally: Check level up after updating points
        leveled_up = user.check_level_up()

        # Add completed lesson
        # Assuming `chapter_id` or `quiz_id` corresponds to a chapter
        chapter = Chapter.query.filter_by(id=quiz_id).first()  # or use `chapter_id` if named differently

        if chapter:
            # Check if progress already exists
            progress = UserChapterProgress.query.filter_by(user_id=user.id, chapter_id=chapter.id).first()
            
            if not progress:
                progress = UserChapterProgress(
                    user_id=user.id,
                    chapter_id=chapter.id,
                    completed=True,
                    completed_at=datetime.utcnow(),
                    score=earned_points
                )
                db.session.add(progress)
            else:
                # Update existing record if it exists
                progress.completed = True
                progress.completed_at = datetime.utcnow()
                progress.score = earned_points


        db.session.commit()

        # clear session to make sure no re-submissions
        session.pop('quiz', None)

        flash(f"Your answred: {score} out of 8 correctly You Got {score*10} Points", "success")
        if(leveled_up):
            flash("Congratulations! You Leveled Up !!!", "success")

        return render_template(
            'quiz_ans.html',
            user=user,
            quiz=quiz,
            points=score*10,  # Adjust as needed based on your logic
            time_limit=5,  # Adjust as needed based on your logic
            questions=quiz['questions'],  # Pass the questions list
            user_answers=user_answers,
            answer_key=answers,  # Pass the correct answers
            results=results,  # Pass results for color coding
            submitted=True
        )