from app import app, db
from models.models import (User, Course, Chapter, 
                   UserChapterProgress, Achievement, 
                   UserAchievement, user_courses)  # Add user_courses to imports
from datetime import datetime

def print_all_data():
    with app.app_context():
        print("\n" + "="*50)
        print("USERS")
        print("="*50)
        users = User.query.all()
        for u in users:
            print(f"\nID: {u.id}")
            print(f"Name: {u.name}")
            print(f"Username: {u.username}")
            print(f"Email: {u.email}")
            print(f"Stream: {u.stream}")
            print(f"Year: {u.year}")
            print(f"Points: {u.points}")
            print(f"Level: {u.level}")
            print(f"Is Admin: {u.is_admin}")
            print(f"Created At: {u.created_at}")
            print(f"Last Login: {u.last_login}")
            
            # Print enrolled courses with progress
            # if u.courses:
            #     print("\nEnrolled Courses:")
            #     for course in u.courses:
            #         # Get progress through the association table
            #         progress = db.session.execute(
            #             db.select(user_courses)
            #             .where(
            #                 (user_courses.c.user_id == u.id) &
            #                 (user_courses.c.course_id == course.id)
            #             )
            #         ).scalar_one_or_none()
                    
            #         if progress:
            #             status = "Completed" if progress.completed else "In Progress"
            #             date = f" on {progress.completion_date}" if progress.completion_date else ""
            #             print(f"- {course.name} ({status}{date})")

        # Rest of your printing code remains the same...
        print("\n" + "="*50)
        print("COURSES")
        print("="*50)
        courses = Course.query.all()
        for c in courses:
            print(f"\nID: {c.id}")
            print(f"Name: {c.name}")
            print(f"Image: {c.image}")
            # print(f"Description: {c.description[:50]}...")
            print(f"Active: {c.is_active}")
            print(f"Created At: {c.created_at}")
            print(f"Updated At: {c.updated_at}")
            
            if c.chapters:
                print("\nChapters:")
                for chapter in sorted(c.chapters, key=lambda x: x.order):
                    print(f"- {chapter.order}. {chapter.title}")

        print("\n" + "="*50)
        print("ACHIEVEMENTS")
        print("="*50)
        achievements = Achievement.query.all()
        for a in achievements:
            print(f"\nID: {a.id}")
            print(f"Code: {a.code}")
            print(f"Name: {a.name}")
            print(f"Description: {a.description}")
            print(f"Category: {a.category}")
            print(f"Points: {a.points}")
            
            earned_by = UserAchievement.query.filter_by(achievement_id=a.id).count()
            print(f"Earned by: {earned_by} users")

if __name__ == "__main__":
    print_all_data()