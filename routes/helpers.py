import markdown, os
import json
from flask import current_app

def markdown_to_html(markdown_text):
    """Convert Markdown text to HTML"""
    html = markdown.markdown(markdown_text)
    return html

def get_chapter_content(filename):
    # Define the base directory
    chapters_dir = os.path.join("templates", "chapters")

    # Construct full file path
    filepath = os.path.join(chapters_dir, filename)

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Chapter '{filename}' not found in {chapters_dir}/ directory"
        )
    except PermissionError:
        raise PermissionError(
            f"Permission denied reading {filepath}"
        )
    except UnicodeDecodeError:
        # Fallback to binary if UTF-8 fails
        with open(filepath, 'rb') as file:
            return file.read().decode('utf-8', errors='replace')

def get_quiz(filename):
    try:
        # Construct the full file path
        quiz_path = os.path.join(
            current_app.root_path,  # Flask application root directory
            'templates',
            'quizzes',
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
