from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app
from .models import db
from .models import User, Course

# Models

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
