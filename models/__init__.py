from .database import db
from .models import User, Course, Achievement

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

        # Check if admin exists, if not, create one
        if not User.query.filter_by(username='Sanket').first():
            admin = User(
                name='Sanket',
                username='Sanket',
                email='sanketjawali25@gmail.com',
                stream='Engineering',  # Updated
                year='4th Year',
                password='admin123',
                is_admin=True,
                level='1'
            )
            db.session.add(admin)
            db.session.commit()

# Add default achievements if none exist
        if not Achievement.query.first():
            achievements = [
                Achievement(
                    code="first_lesson",
                    name="First Steps",
                    description="Complete your first lesson",
                    badge_image="badge_first_lesson.svg",
                    category="progress",
                    points=10
                ),
                Achievement(
                    code="ten_lessons",
                    name="Consistent Learner",
                    description="Complete 10 lessons",
                    badge_image="badge_ten_lessons.svg",
                    category="progress",
                    points=25
                ),
                Achievement(
                    code="quiz_master",
                    name="Quiz Master",
                    description="Score 100% on any quiz",
                    badge_image="badge_quiz_master.svg",
                    category="quiz",
                    points=15
                ),
                Achievement(
                    code="python_beginner",
                    name="Python Beginner",
                    description="Complete the Python beginner course",
                    badge_image="badge_python_beginner.svg",
                    category="course",
                    points=50
                ),
                # Add more achievements here
            ]
            
            for achievement in achievements:
                db.session.add(achievement)
            
            db.session.commit()

