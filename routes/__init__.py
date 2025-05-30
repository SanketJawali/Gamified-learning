from .home import home_page
from .admin import admin_courses_page, delete_course
from .auth_routes import register_page, login_page, logout_page
from .course import courses_page,select_course_page, set_current_course_session
from .lesson import lessons_page
from .quiz import quiz_page, quiz_logic_page
from .user import profile_page
from .chapter import chapter_page
from .code import code_page, run_code

def init_admin(app):
    app.add_url_rule('/admin_courses', 'admin_courses', admin_courses_page, methods=['GET', 'POST'])
    app.add_url_rule('/admin/delete_course', 'admin_delete', delete_course, methods=['DELETE'])

def init_auth_routes(app):
    app.add_url_rule('/register', 'register', register_page, methods=['GET', 'POST'])
    app.add_url_rule('/login', 'login', login_page, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', logout_page)

def init_course(app):
    app.add_url_rule('/courses', 'courses', courses_page, methods=['GET'])
    app.add_url_rule('/select_course', 'select_course',select_course_page, methods=['POST'])
    app.add_url_rule('/set_current_course_session', 'set_current_course_session', set_current_course_session, methods=['POST'])

def init_chapter(app):
    app.add_url_rule('/chapter', 'chapter', chapter_page, method=['GET','POST'])

def init_lesson(app):
    app.add_url_rule('/lessons', 'lessons', lessons_page,methods=['GET','POST'])

def init_home(app):
    app.add_url_rule('/', 'home', home_page)

def init_quiz(app):
    app.add_url_rule('/quiz', 'quiz', quiz_page, methods=['GET', 'POST'])
    app.add_url_rule('/quiz_logic', 'quiz_logic', quiz_logic_page, methods=['GET', 'POST'])

def init_user(app):
    app.add_url_rule('/profile', 'profile', profile_page)

def init_code(app):
    app.add_url_rule('/code', 'code', code_page)
    app.add_url_rule('/run', 'run', run_code, methods=['POST'])