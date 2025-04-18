from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from routes.helpers import *
from models.models import User
from models.database import db
import subprocess
import sys
import os

def code_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db.session.get(User, session['user_id'])
    if user is None:
        session.pop('user_id', None)
        return redirect(url_for('home'))
    if user.is_admin:
        return redirect(url_for('admin_courses'))

    return render_template('code.html', user=user)

def run_code():
    # Ensure we're getting JSON
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    code = data.get('code', '')
    
    try:
        # Create temporary file
        temp_file = 'temp_code.py'
        with open(temp_file, 'w') as f:
            f.write(code)
        
        # Execute code with timeout
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Clean up
        os.remove(temp_file)
        
        # Return consistent JSON structure
        return jsonify({
            'output': result.stdout,
            'error': result.stderr if result.returncode != 0 else None
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Code execution timed out'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
