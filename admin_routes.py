from flask import Flask, flash, redirect, render_template, request, session, url_for
import os
from werkzeug.utils import secure_filename
from app import app
from models import db, Influencer, Company, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_login', methods=['POST'])
def admin_login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if username and password are provided
    if not username or not password:
        flash('All the fields are required')
        return redirect(url_for('admin_login'))

    # Query for the admin user by username
    admin = Admin.query.filter_by(username=username).first()

    # Check if admin exists and the password matches
    if not admin or not check_password_hash(admin.password_hash, password):
        flash('Invalid username or password')
        return redirect(url_for('admin_login'))

    # Redirect to the welcome message page on successful login
    return redirect(url_for('welcome_msg'))