from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    class_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=0)
    course = db.Column(db.String(50))
    completed_lessons = db.Column(db.String(200), default="")
    is_admin = db.Column(db.Boolean, default=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(100), nullable=False)
# Initialize Database
def init_db():
    with app.app_context():
        db.create_all()
        # Check if admin exists, if not, create one
        if not User.query.filter_by(username='Sanket').first():
            admin = User(
                name='Sanket',
                username='Sanket',
                email='jadhavdamodar027@gmail.com',
                mobile='8788120613',
                class_name='Admin',
                password='admin123',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
        # Add default course if none exist
        if not Course.query.first():
            default_course = Course(name='Python', image='python_logo.png')
            db.session.add(default_course)
            db.session.commit()
