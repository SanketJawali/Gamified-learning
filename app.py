from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from models import init_db, db
from routes import *
from routes.helpers import *
import markdown
from markupsafe import Markup
import os
import re
import secrets


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'mysecret123'

    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'gamifiedlearnig.pvt.ltd@gmail.com'  # Replace with your Gmail address
    app.config['MAIL_PASSWORD'] = 'pfcvyxokglcgkurc'  # Replace with your Gmail App Password
    app.config['MAIL_DEFAULT_SENDER'] = 'gamifiedlearnig.pvt.ltd@gmail.com'  # Default sender for emails

    app.jinja_env.globals.update(chr=chr)
    app.jinja_env.globals.update(get_achievement_by_code=get_achievement_by_code)

    init_db(app)

    # Routes
    app.add_url_rule('/', 'home', home.home_page)

    app.add_url_rule('/register', 'register', auth_routes.register_page, methods=['GET', 'POST'])

    app.add_url_rule('/login', 'login', auth_routes.login_page, methods=['GET', 'POST'])

    app.add_url_rule('/courses', 'courses', course.courses_page)

    app.add_url_rule('/achievements','achievements',user.achievements_page,methods=['POST','GET'])

    app.add_url_rule('/select_course', 'select_course', course.select_course_page, methods=['POST'])

    app.add_url_rule('/set_currect_course_session', 'set_current_course_session', course.set_current_course_session, methods=['POST'])

    app.add_url_rule('/admin/image/<int:course_id>', 'course_image', admin. get_course_image)

    app.add_url_rule('/admin_courses', 'admin_courses', admin.admin_courses_page, methods=['GET', 'POST'])

    app.add_url_rule('/admin/delete_course/<int:course_id>', 'admin_delete', admin.delete_course, methods=['DELETE'])

    app.add_url_rule('/lessons>', 'lessons', lesson.lessons_page)

    app.add_url_rule('/chapter/<int:chapter_id>', 'chapter', chapter.chapter_page)

    app.add_url_rule('/quiz/<int:quiz_id>', 'quiz', quiz.quiz_page, methods=['GET', 'POST'])

    app.add_url_rule('/quiz_logic/<int:quiz_id>', 'quiz_logic', quiz.quiz_logic_page, methods=['GET', 'POST'])

    app.add_url_rule('/profile', 'profile', user.profile_page)

    app.add_url_rule('/contact_support', 'contact_support', user.contact_support_page)

    app.add_url_rule('/code', 'code', code.code_page)

    app.add_url_rule('/run', 'run_code', code.run_code, methods=['POST'])

    # Add verify-email route
    app.add_url_rule('/verify-email', 'verify_email', auth_routes.verify_email)

    app.add_url_rule('/logout', 'logout', auth_routes.logout_page)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.after_request
    def add_csrf_header(response):
        csrf_token = secrets.token_hex(16)
        response.set_cookie('csrf_token', csrf_token)
        response.headers['X-CSRF-Token'] = csrf_token
        return response

    @app.template_filter('markdown')
    def markdown_filter(text):
        extensions = ['fenced_code', 'codehilite', 'tables', 'nl2br']
        raw_html = markdown.markdown(text, extensions=extensions)
        return clean_markdown_html(raw_html)

    return app


app = create_app()

# Initialize Flask-Mail
mail = Mail(app)

if __name__ == '__main__':
    app.run(debug=True)
