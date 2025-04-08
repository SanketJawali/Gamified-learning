from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models.models import User, Course
from models.database import db
from .helpers import get_course_image

def courses_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if user.is_admin:
        return redirect(url_for('admin_courses'))
    courses = Course.query.all()

    return render_template('courses.html', user=user, courses=courses)

def select_course_page():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.clear()
        return jsonify({'error': 'Not logged in'}), 401
    
    if user.is_admin:
        return jsonify({'error': 'Admins cannot select courses'}), 403
    
    data = request.get_json()
    if not data or 'course' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    course_id = data['course']
    course = db.session.get(Course, course_id)
    
    if not course:
        return jsonify({'error': 'Invalid course'}), 400
    
    # Check if user is already enrolled
    if course not in user.courses:
        # Add the course to user's courses
        user.courses.append(course)
        db.session.commit()
    
    # Set session variables
    session['current_course_id'] = course.id
    session['current_course_name'] = course.name


    
    return jsonify({
        'success': True, 
        'redirect': url_for('lessons', course_id=course.id, _external=True)
    })

