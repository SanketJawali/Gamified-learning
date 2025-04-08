from app import app,db, user  # Import from your app.py

with app.app_context():  # Needed for Flask-SQLAlchemy to work outside the app
    # Print all users
    users = user.query.all()
    for u in users:
        print(f"ID: {u.id}")
        print(f"Username: {u.username}")
        print(f"Password: {u.password}")
        print(f"Points: {u.points}")
        print(f"Course: {u.course}")
        print(f"Completed Lessons: {u.completed_lessons}")
        print("---")

    # Example: Add a test user (optional)
    # new_user = User(username="debuguser", password="debugpass")
    # db.session.add(new_user)
    # db.session.commit()
    # print("Added debuguser")