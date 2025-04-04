from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from models import init_db, db
from routes import *
import os
import re


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'mysecret123'

    init_db(app)

    # Routes
    app.add_url_rule('/', 'home', home.home_page)

    app.add_url_rule('/register', 'register', auth_routes.register_page, methods=['GET', 'POST'])

    app.add_url_rule('/login', 'login', auth_routes.login_page, methods=['GET', 'POST'])

    app.add_url_rule('/courses', 'courses', course.courses_page)

    app.add_url_rule('/select_course', 'select_course', course.select_course_page, methods=['POST'])

    app.add_url_rule('/admin_courses', 'admin_courses', admin.admin_courses_page, methods=['GET', 'POST'])

    app.add_url_rule('/lessons', 'lessons', lesson.lessons_page)

    app.add_url_rule('/chapter/<int:chapter_id>', 'chapter', chapter.chapter_page)

    app.add_url_rule('/quiz/<int:quiz_id>', 'quiz', quiz.quiz_page, methods=['GET', 'POST'])

    app.add_url_rule('/quiz_ans/<int:quiz_id>', 'quiz_ans', quiz.quiz_ans_page, methods=['GET', 'POST'])

    app.add_url_rule('/profile', 'profile', user.profile_page)

    app.add_url_rule('/contact_support', 'contact_support', user.contact_support_page)

    app.add_url_rule('/logout', 'logout', auth_routes.logout_page)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
