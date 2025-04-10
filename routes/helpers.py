import markdown, os
from markupsafe import Markup
import json
from models.models import User, Chapter, Course, UserChapterProgress
from flask import current_app, send_from_directory
from models.database import db
import os
import re
from werkzeug.exceptions import NotFound
from models import Achievement

def get_course_lessons(course_id):
    """
    Retrieve all chapter names/titles for a specific course
    
    Args:
        course_id (int): ID of the course
    
    Returns:
        list: List of chapter dictionaries with id and title, ordered by chapter order
        None: If course doesn't exist or has no chapters
    """
    try:
        # Get the course with its chapters
        course = Course.query.get(course_id)
        
        if not course:
            return None
            
        # Get all chapters ordered by their 'order' field
        chapters = Chapter.query.filter_by(
            course_id=course_id
        ).order_by(Chapter.order.asc()).all()
        
        if not chapters:
            return None
            
        return [{
            'id': chapter.id,
            'title': chapter.title,
            'order': chapter.order
        } for chapter in chapters]
        
    except Exception as e:
        # Log the error in a real application
        print(f"Error fetching course chapters: {str(e)}")
        return None

def markdown_to_html(markdown_text):
    extensions = [
        'fenced_code',       # GitHub-style code blocks
        'codehilite',       # Syntax highlighting
        'tables',           # Tables support
        'toc',              # Table of contents
        'nl2br',            # Convert newlines to <br>
        'md_in_html'        # Allow Markdown within HTML blocks
    ]

    extension_configs = {
        'codehilite': {
            'linenums': True,       # Add line numbers
            'use_pygments': True,   # Use Pygments for highlighting
            'css_class': 'codehilite'  # CSS class for styling
        }
    }

    html = markdown.markdown(
        markdown_text,
        extensions=extensions,
        extension_configs=extension_configs,
        output_format='html5'
    )
    return Markup(html)

def get_chapter_content(course_id, chapter_order):
    """
    Retrieve chapter content for a specific chapter in a course
    
    Args:
        course_id (int): ID of the course
        chapter_order (int): The order/sequence number of the chapter within the course
    
    Returns:
        dict: Chapter details including title and content if found
        None: If chapter doesn't exist or doesn't belong to the course
    """
    try:
        # Get the first chapter matching both course_id and order
        chapter = Chapter.query.filter_by(
            course_id=course_id,
            order=chapter_order
        ).first()  # Note: using .first() here

        if chapter:
            return {
                'id': chapter.id,
                'title': chapter.title,
                'content': chapter.content,
                'order': chapter.order,
                'course_id': chapter.course_id
            }
        return None
        
    except Exception as e:
        print(f"Error fetching chapter content: {str(e)}")
        return None

def get_quiz(filename):
    try:
        # Construct the full file path
        quiz_path = os.path.join(
            current_app.root_path,  # Flask application root directory
            'templates',
            'quizes',
            f'{filename}.json'  # Add .json extension
        )

        # Check if file exists
        if not os.path.exists(quiz_path):
            current_app.logger.error(f"Quiz file not found: {quiz_path}")
            return None

        # Load and parse JSON
        with open(quiz_path, 'r', encoding='utf-8') as f:
            quiz_data = json.load(f)

        return quiz_data

    except json.JSONDecodeError as e:
        current_app.logger.error(f"Invalid JSON in quiz file: {e}")
        return None
    except Exception as e:
        current_app.logger.error(f"Error loading quiz: {e}")
        return None

def get_quiz_answers(filename):
    try:
        answer_path = os.path.join(
            current_app.root_path,
            'templates',
            'quizes',
            f'{filename}.json'
        )

        if not os.path.exists(answer_path):
            current_app.logger.error(f"Answer file not found: {answer_path}")
            return None

        with open(answer_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    except Exception as e:
        current_app.logger.error(f"Error loading answers: {e}")
        return None

def get_completed_chapters(user_id, course_id=None):
    """
    Get all completed chapters for a user, optionally filtered by course
    
    Args:
        user_id (int): ID of the user
        course_id (int, optional): Specific course ID to filter by
        
    Returns:
        dict: {
            'completed_chapters': list of chapter IDs,
            'total_in_course': total chapters in course (if course_id provided),
            'completion_percentage': percentage completed (if course_id provided)
        }
        or None if user doesn't exist
    """
    # Verify user exists
    user = db.session.get(User, user_id)
    if not user:
        return None

    # Base query for completed chapters
    query = db.session.query(
        UserChapterProgress.chapter_id,
        Chapter.course_id,
        Chapter.title
    ).join(
        Chapter,
        UserChapterProgress.chapter_id == Chapter.id
    ).filter(
        UserChapterProgress.user_id == user_id,
        UserChapterProgress.completed == True
    )

    # Filter by course if specified
    if course_id:
        query = query.filter(Chapter.course_id == course_id)

    # Execute query
    completed_chapters = query.all()

    # Prepare results
    result = {
        'completed_chapters': [{
            'chapter_id': chap.chapter_id,
            'title': chap.title,
            'course_id': chap.course_id
        } for chap in completed_chapters]}

    return result


def get_course_image(course_id):
    """
    Retrieve a course image from storage
    
    Args:
        course_id (int): ID of the course
    
    Returns:
        Response: Flask send_file response with the image
        None: If no image exists for the course
    
    Raises:
        NotFound: If image file doesn't exist
    """
    course = Course.query.get(course_id)
    if not course or not course.image:
        return None
    
    # Construct full path from the stored relative path
    image_path = os.path.join('static', course.image)
    
    # Verify the file exists
    if not os.path.exists(image_path):
        raise NotFound(f"Image not found at {image_path}")
    
    # Get directory and filename for send_from_directory
    directory = os.path.join('static', 'uploads', 'courses')
    filename = os.path.basename(course.image)
    try:
        return send_from_directory(directory, filename)
    except NotFound:
        # Return default image if course image doesn't exist
        return send_from_directory('static', 'star.png')
    except Exception as e:
        return None

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_achievement_by_code(code):
    """Get achievement by code - used in templates"""
    return Achievement.query.filter_by(code=code).first()

def clean_markdown_html(html):
    """Transform raw markdown HTML into a more structured format"""
    # Convert single-item lists into regular paragraphs
    html = re.sub(
        r'<ol>\s*<li>(.*?)</li>\s*</ol>',
        r'<div class="text-lg">\1</div>',
        html,
        flags=re.DOTALL
    )
    
    # Clean up code blocks
    html = re.sub(
        r'<div class="codehilite"><pre><span></span><code>(.*?)</code></pre></div>',
        r'<div class="codehilite"><pre><span></span><code class="text-base">\1</code></pre></div>',
        html,
        flags=re.DOTALL
    )
    
    return Markup(html)