from flask import Flask, render_template, request, redirect, url_for, flash, session
from routes.helpers import *
from models.models import User
from models.database import db

def code_page():
    return render_template('code.html')

