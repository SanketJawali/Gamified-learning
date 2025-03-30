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
                email='jadhavdamodar027@gmail.com',
                mobile='8788120613',
                stream='Engineering',  # Updated
                year='4th Year',
                password='admin123',
                is_admin=True,
                level='Advanced'
            )
            db.session.add(admin)
            db.session.commit()

        # Add default course if none exist
        if not Course.query.first():
            default_course = Course(name='Python', image='python_logo.png')
            db.session.add(default_course)
            db.session.commit()
