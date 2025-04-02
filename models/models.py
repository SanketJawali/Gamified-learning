from .database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    stream = db.Column(db.String(20), nullable=False)  # New: Replacing class_name
    year = db.Column(db.String(10), nullable=False)   # New: Year field
    password = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=0)
    course = db.Column(db.String(50))
    level = db.Column(db.Integer, default=1)
    completed_lessons = db.Column(db.String(200), default="")
    is_admin = db.Column(db.Boolean, default=False)

    def check_level_up(self):
        """Check if user should level up and update accordingly"""
        levels_required = 200  # Points needed per level
        level_ups = self.points // levels_required

        if level_ups > 0:
            self.level += level_ups
            self.points = self.points % levels_required  # Carry over remaining points
            return True
        return False

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(100), nullable=False)
