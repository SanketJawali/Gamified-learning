from .database import db
from datetime import datetime
import os

# Association table for many-to-many relationship between users and courses
user_courses = db.Table('user_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('completed', db.Boolean, default=False),
    db.Column('completion_date', db.DateTime)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    stream = db.Column(db.String(20), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationship to courses (many-to-many with additional attributes)
    courses = db.relationship('Course', secondary=user_courses, back_populates='users')
    
    # Relationship to completed chapters (track progress)
    completed_chapters = db.relationship('UserChapterProgress', back_populates='user')
    
    def check_level_up(self):
        levels_required = 200  # Points needed per level
        level_ups = self.points // levels_required

        if level_ups > 0:
            self.level += level_ups
            self.points = self.points % levels_required
            return True
        return False

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(100), nullable=True, default="star.png")
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship to users (many-to-many)
    users = db.relationship('User', secondary=user_courses, back_populates='courses')
    
    # Relationship to chapters (one-to-many)
    chapters = db.relationship('Chapter', back_populates='course', cascade='all, delete-orphan')
    
    def save_image(self, image_file):
        """Handle image upload and save path to database"""
        if not image_file:
            return None
            
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join('static', 'uploads', 'courses')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        ext = os.path.splitext(image_file.filename)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            return None
            
        filename = f"course_{self.id}{ext}"
        filepath = os.path.join(upload_dir, filename)
        
        # Save file
        image_file.save(filepath)
        
        # Save relative path to database
        self.image = os.path.join('uploads', 'courses', filename)
        return self.image

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to course
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    # Relationship to course
    course = db.relationship('Course', back_populates='chapters')
    
    # Relationship to user progress
    user_progress = db.relationship('UserChapterProgress', back_populates='chapter')

class UserChapterProgress(db.Model):
    __tablename__ = 'user_chapter_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    score = db.Column(db.Integer)  # Optional: for quizzes or assessments
    
    # Relationships
    user = db.relationship('User', back_populates='completed_chapters')
    chapter = db.relationship('Chapter', back_populates='user_progress')
    
    # Composite unique constraint
    __table_args__ = (
        db.UniqueConstraint('user_id', 'chapter_id', name='_user_chapter_uc'),
    )

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    badge_image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer, default=10)
    
class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    date_earned = db.Column(db.DateTime, default=datetime.utcnow)
    
    achievement = db.relationship('Achievement')