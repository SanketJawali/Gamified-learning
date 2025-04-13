from flask import render_template, redirect, url_for,session,request,flash
from models.models import User, Course, UserAchievement, Achievement
from models.database import db

def profile_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('home'))
            
    course_id = session['current_course_id']
    course = Course.query.get(course_id)
    number_chapters = len(course.chapters)

    return render_template('profile.html', user=user, number_chapters=number_chapters)

def contact_support_page():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    return render_template('contact_support.html', user=user)

def select_level_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('home'))
    if request.method == 'POST':
        level = request.form['level']
        if level in ['Beginner', 'Intermediate', 'Advanced']:
            user.level = level
            db.session.commit()
            return redirect(url_for('lessons'))
        flash('Invalid level selected.')
    return render_template('select_level.html', user=user)

def achievements_page():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('home'))
    
    # Get user's earned achievements
    user_achievements = UserAchievement.query.filter_by(user_id=user.id).all()
    earned_ids = [ua.achievement_id for ua in user_achievements]
    
    # Get all achievements
    all_achievements = Achievement.query.all()
    
    return render_template('achivements_page.html',
                        user=user,
                        earned_ids=earned_ids,
                        all_achievements=all_achievements)