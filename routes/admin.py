from flask import Flask, render_template, request, redirect, url_for, flash,make_response, session, jsonify
import re
from models.models import *
from .helpers import *
from models.database import db
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/static/courses/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def admin_courses_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.clear()
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # Get form data
            course_name = request.form.get('course_name')
            image_file = request.files.get('course_image')
            
            # Validate required fields
            if not course_name:
                flash('Course name is required', 'error')
                return redirect(url_for('admin_courses'))
            
            if Course.query.filter_by(name=course_name).first():
                flash('Course already exists!', 'error')
                return redirect(url_for('admin_courses'))
            
            # Create new course
            new_course = Course(name=course_name)
            db.session.add(new_course)
            db.session.flush()  # Generate ID for image naming
            
            # Handle image upload
            if image_file:
                image_path = new_course.save_image(image_file)
                if not image_path:
                    flash('Invalid image file', 'error')
                    db.session.rollback()
                    return redirect(url_for('admin_courses'))
            else:
                flash('No valid image uploaded', 'error')
                db.session.rollback()
                return redirect(url_for('admin_courses'))
            
            # Handle chapters
            chapter_counter = 1
            while f'chapter_title_{chapter_counter}' in request.form:
                chapter_title = request.form.get(f'chapter_title_{chapter_counter}')
                chapter_content = request.form.get(f'chapter_content_{chapter_counter}')
                
                if chapter_title and chapter_content:
                    new_chapter = Chapter(
                        title=chapter_title,
                        content=chapter_content,
                        order=chapter_counter,
                        course_id=new_course.id
                    )
                    db.session.add(new_chapter)
                
                chapter_counter += 1
            
            db.session.commit()
            flash('Course created successfully!', 'success')
            return redirect(url_for('admin_courses'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating course: {str(e)}', 'error')
            return redirect(url_for('admin_courses'))
    
    # For GET requests or after processing
    courses = Course.query.all()
    return render_template('admin_courses.html', user=user, courses=courses)

def delete_course(course_id):
    """
    Delete a course (admin only) - HTMX compatible version
    """
    # Authentication and authorization check
    if 'user_id' not in session:
        return '', 401  # HTMX expects empty response for errors
    
    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin:
        return '', 403

    course = db.session.get(Course, course_id)
    if not course:
        return '', 404

    try:
        # Delete all associated data
        Chapter.query.filter_by(course_id=course_id).delete()
        db.session.execute(
            user_courses.delete().where(user_courses.c.course_id == course_id)
        )
        db.session.delete(course)
        db.session.commit()

        # Clear session if needed
        if session.get('current_course_id') == course_id:
            session.pop('current_course_id', None)
            session.pop('current_course_name', None)

        # Return HTMX-compatible response
        response = make_response('', 200)
        response.headers['HX-Trigger'] = json.dumps({
            'showToast': {
                'message': f'Course "{course.name}" deleted successfully',
                'type': 'success'
            }
        })
        return response

    except Exception as e:
        db.session.rollback()
        flash(f"Failed to delete Course: {str(e)}", "error")
        return response

def save_image(self, image_file):
    try:
        # Get file extension
        filename, ext = os.path.splitext(image_file.filename)
        if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
            return None
            
        # Create a unique filename
        secure_filename = f"course_{self.id}{ext}"
        
        # Make sure the uploads directory exists
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'courses')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(upload_dir, secure_filename)
        image_file.save(file_path)
        
        # Update the course's image path
        self.image_path = f"uploads/courses/{secure_filename}"
        
        return self.image_path
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return None
