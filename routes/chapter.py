from flask import Flask, render_template, request, redirect, url_for, flash, session
from routes.helpers import *
from models.models import User
from models.database import db

def chapter_page(chapter_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    # Get chapter content
    content = get_chapter_content(chapter_id + ".md")

    # Convert markdown to html


    # Render chapters template
    return render_template('chapter.html', user=user, content=content)
