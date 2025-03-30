from app import app,db, User  # Import from your app.py

with app.app_context():  # Needed for Flask-SQLAlchemy to work outside the app
    # Print all users
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Password: {user.password}")
        print(f"Points: {user.points}")
        print(f"Course: {user.course}")
        print(f"Completed Lessons: {user.completed_lessons}")
        print("---")

    # Example: Add a test user (optional)
    # new_user = User(username="debuguser", password="debugpass")
    # db.session.add(new_user)
    # db.session.commit()
    # print("Added debuguser")