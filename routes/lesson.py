from flask import render_template, redirect, url_for, session, flash
from models.models import User, Course
from .helpers import *
from models.database import db

def lessons_page():
    # Authentication check
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    if user is None:
        session.clear()
        return redirect(url_for('login'))

    # Check if user has selected a level
    if not user.level:
        return redirect(url_for('select_level'))

    # Get user current course
    course_id = session['current_course_id']

    # Verify the course exists
    course = db.session.get(Course, course_id)
    if not course:
        flash('Course not found', 'error')
        return redirect(url_for('courses_page'))

    lessons = get_course_lessons(course_id)

    completed_lessons_list = get_completed_chapters(user.id, session['current_course_id'])['completed_chapters']
    completed_chapter_ids = {lesson['chapter_id'] for lesson in completed_lessons_list}
    print(completed_chapter_ids)

    return render_template('lessons.html', user=user, lessons=lessons, completed_chapter_ids=completed_chapter_ids)
