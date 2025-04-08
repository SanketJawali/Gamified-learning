from .database import db
from .models import User, Course

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


