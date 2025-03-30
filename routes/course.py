from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models.models import User, Course
from models.database import db

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
        session.pop('user_id', None)
        return jsonify({'error': 'Not logged in'}), 401
    if user.is_admin:
        return jsonify({'error': 'Admins cannot select courses'}), 403
    course_name = request.json.get('course')
    course = Course.query.filter_by(name=course_name).first()
    if course:
        user.course = course.name
        db.session.commit()
        return jsonify({'success': True, 'redirect': url_for('select_level')})
    return jsonify({'error': 'Invalid course'}), 400