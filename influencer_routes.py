from flask import Flask, flash, redirect, render_template, request, url_for, session
import os
from werkzeug.utils import secure_filename
from app import app
from models import db, Influencer, Company, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


from config import *

# Declaring the auth required for influencer
def influencer_auth_required(func):
    @wraps(func)
    def func2(*args, **kwargs):
        if 'influencer_id' in session:
            return func(*args, **kwargs)
        else:
            flash("Please login first")
            return redirect(url_for('influencer_login'))
    return func2


@app.route('/influencer_submission_msg')
def influencer_submission_msg():
    return render_template('influencer_submission_msg.html')

@app.route('/update_message')
def update_message():
    return render_template('update_message.html')


@app.route('/influencer_register')
def influencer_register():
    return render_template('influencer_register.html')

@app.route('/influencer_register', methods=['POST'])
def influencer_register_post():
    fullname = request.form.get('fullname')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    category = request.form.get('category')
    interest = request.form.get('interest')
    reach = request.form.get('reach')
    social_media_links = request.form.get('social_media')
    bio = request.form.get('bio')
    profile_picture = request.files.get('profile_picture')

    if not all([fullname, username, email, password, confirm_password, category, interest, reach, social_media_links, bio, profile_picture]):
        flash('All fields are required')
        return redirect(url_for('influencer_register'))

    if password != confirm_password:
        flash('Passwords do not match')
        return redirect(url_for('influencer_register'))

    if Influencer.query.filter_by(username=username).first():
        flash('Username already exists')
        return redirect(url_for('influencer_register'))

    if Influencer.query.filter_by(email=email).first():
        flash('Email already exists')
        return redirect(url_for('influencer_register'))

    user_directory = os.path.join(app.config['INFLUENCER_UPLOAD_FOLDER'], username)
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)

    filename = secure_filename(profile_picture.filename)
    profile_picture_path = os.path.join(user_directory, filename)
    profile_picture.save(profile_picture_path)

    password_hash = generate_password_hash(password)

    new_influencer = Influencer(
        name=fullname,
        username=username,
        email=email,
        password_hash=password_hash,
        category=category,
        interest=interest,
        reach=reach,
        social_media_links=social_media_links,
        bio=bio,
        profile_picture=filename
    )

    db.session.add(new_influencer)
    db.session.commit()

    return redirect(url_for('influencer_submission_msg'))

@app.route('/influencer_login')
def influencer_login():
    return render_template('influencer_login.html')

@app.route('/influencer_login', methods=['POST'])
def influencer_login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('All fields are required')
        return redirect(url_for('influencer_login'))

    influencer = Influencer.query.filter_by(username=username).first()

    if not influencer or not check_password_hash(influencer.password_hash, password):
        flash('Invalid username or password')
        return redirect(url_for('influencer_login'))

    session['influencer_id'] = influencer.id
    return redirect(url_for('influencer_dashboard'))

@app.route('/influencer_dashboard')
@influencer_auth_required
def influencer_dashboard():
    user = Influencer.query.filter_by(id=session['influencer_id']).first()
    return render_template('influencer_dashboard.html', user=user)

@app.route('/influencer_dashboard', methods=['POST'])
@influencer_auth_required
def influencer_dashboard_post():
    name = request.form.get('fullname')
    username = request.form.get('username')
    email = request.form.get('email')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_new_password')
    category = request.form.get('category')
    other_category = request.form.get('other_category')
    interest = request.form.get('interest')
    reach = request.form.get('reach')
    social_media = request.form.get('social_media')
    bio = request.form.get('bio')
    profile_picture = request.files.get('profile_picture')

    user = Influencer.query.get(session['influencer_id'])

    if old_password and not check_password_hash(user.password_hash, old_password):
        flash('Invalid password')
        return redirect(url_for('influencer_dashboard'))

    if new_password and new_password != confirm_new_password:
        flash('Please confirm your new password')
        return redirect(url_for('influencer_dashboard'))

    if new_password:
        user.password_hash = generate_password_hash(new_password)

    if username and username != user.username:
        if Influencer.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('influencer_dashboard'))
        user.username = username

    if email and email != user.email:
        if Influencer.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('influencer_dashboard'))
        user.email = email

    if name:
        user.name = name
    if category == "Other":
        user.category = other_category
    else:
        user.category = category
    if interest:
        user.interest = interest
    if reach:
        user.reach = reach
    if social_media:
        user.social_media_links = social_media
    if bio:
        user.bio = bio

    db.session.commit()
    return redirect(url_for('update_message'))


@app.route('/influencer_logout')
@influencer_auth_required
def influencer_logout():
    session.pop('influencer_id')
    return redirect(url_for('influencer_login'))