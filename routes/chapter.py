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
    filename = f"chapter_{chapter_id}.md"
    md = get_chapter_content(filename)

    # Convert markdown to html
    content = markdown_to_html(md)

    # Render chapters template
    return render_template('chapter.html', user=user, content=content, chapter_id=chapter_id)
