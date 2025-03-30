from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import re
from models.models import User, Course
from models.database import db

def admin_courses_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if not user.is_admin:
        return redirect(url_for('courses'))
    
    if request.method == 'POST':
        if 'add_course' in request.form:
            name = request.form['course_name']
            image = request.form['course_image']
            if Course.query.filter_by(name=name).first():
                flash('Course already exists!')
            else:
                new_course = Course(name=name, image=image)
                db.session.add(new_course)
                db.session.commit()
                flash('Course added successfully!')
        elif 'delete_course' in request.form:
            course_id = request.form['course_id']
            course = db.session.get(Course, course_id)
            if course:
                db.session.delete(course)
                db.session.commit()
                flash('Course deleted successfully!')
            else:
                flash('Course not found!')
    
    courses = Course.query.all()
    return render_template('admin_courses.html', user=user, courses=courses)