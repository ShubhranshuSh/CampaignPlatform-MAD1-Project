from flask import Flask, flash, redirect, render_template, request, session, url_for
import os
from werkzeug.utils import secure_filename
from app import app
from models import db, Influencer, Company
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from config import *

def company_auth_required(func):
    @wraps(func)
    def func3(*args, **kwargs):
        if 'company_id' in session:
            return func(*args, **kwargs)
        else:
            flash("Please login first")
            return redirect(url_for('company_login'))
    return func3


@app.route('/company_submission_msg')
def company_submission_msg():
    return render_template('company_submission_msg.html')

@app.route('/company_register')
def company_register():
    return render_template('company_register.html')

@app.route('/company_register', methods=['POST'])
def company_register_post():
    company_name = request.form.get('company_name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    phone_number = request.form.get('phone_number')
    address = request.form.get('address')
    industry = request.form.get('industry')
    other_industry = request.form.get('other_industry')
    website = request.form.get('website')
    description = request.form.get('description')
    social_media_link = request.form.get('social_media')
    logo = request.files.get('logo')


    # debugging the form data
    # print(company_name, username, email, password, confirm_password, phone_number, address, industry, website, description, social_media_link, logo)

    if not all([company_name, username, email, password, confirm_password, phone_number, address, industry ,website, description, social_media_link, logo]):
        flash('All fields are required')
        return redirect(url_for('company_register'))

    if password != confirm_password:
        flash('Passwords do not match')
        return redirect(url_for('company_register'))

    if Company.query.filter_by(username=username).first():
        flash('Username already exists')
        return redirect(url_for('company_register'))

    if Company.query.filter_by(email=email).first():
        flash('Email already exists')
        return redirect(url_for('company_register'))

    user_directory = os.path.join(app.config['COMPANY_UPLOAD_FOLDER'], username)
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)

    filename = secure_filename(logo.filename)
    profile_picture_path = os.path.join(user_directory, filename)
    logo.save(profile_picture_path)

    password_hash = generate_password_hash(password)

    new_company = Company(
        company_name=company_name,
        username=username,
        email=email,
        password_hash=password_hash,
        phone_number=phone_number,
        address=address,
        industry=industry,
        other_industry=other_industry,
        website=website,
        description=description,
        social_media_link=social_media_link,
        logo=filename
    )

    db.session.add(new_company)
    db.session.commit()

    return redirect(url_for('company_submission_msg'))


@app.route('/company_login')
def company_login():
    return render_template('company_login.html')

@app.route('/company_login', methods=['POST'])
def company_login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if username and password are provided
    if not username or not password:
        flash('All the fields are required')
        return redirect(url_for('company_login'))

    # Query for the company user by username
    company = Company.query.filter_by(username=username).first()

    # Check if company exists and the password matches
    if not company or not check_password_hash(company.password_hash, password):
        flash('Invalid username or password')
        return redirect(url_for('company_login'))

    # Redirect to the welcome message page on successful login
    session['company_id'] = company.id
    return redirect(url_for('company_dashboard'))

@app.route('/company_dashboard')
@company_auth_required
def company_dashboard():
    user = Company.query.filter_by(id=session['company_id']).first()
    return render_template('company_dashboard.html', user=user)

@app.route('/company_dashboard', methods=['POST'])
@company_auth_required
def company_dashboard_post():
    company_name=request.form.get('company_name')
    username = request.form.get('username')
    email = request.form.get('email')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_new_password')
    phone_number = request.form.get('phone_number')
    address = request.form.get('address')
    industry = request.form.get('industry')
    other_industry = request.form.get('other_industry')
    website = request.form.get('website')
    description = request.form.get('description')
    social_media_link = request.form.get('social_media')
    logo = request.files.get('logo')

    user=Company.query.get(session['company_id'])

    if old_password and not check_password_hash(user.password_hash, old_password):
        flash('Invalid password')
        return redirect(url_for('company_dashboard'))
    
    if new_password and new_password != confirm_new_password:
        flash('Please confirm your new password')
        return redirect(url_for('company_dashboard'))
    
    if new_password:
        user.password_hash = generate_password_hash(new_password)

    if username and username != user.username:
        if Company.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('company_dashboard'))
        user.username = username

    if email and email != user.email:
        if Company.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('company_dashboard'))
        user.email = email

    if company_name:
        user.company_name = company_name

    if phone_number:
        user.phone_number = phone_number

    if address:
        user.address = address

    if industry:
        user.industry = industry

    if other_industry:
        user.other_industry = other_industry

    if website:
        user.website = website

    if description:
        user.description = description

    if social_media_link:
        user.social_media_link = social_media_link

    db.session.commit()
    return redirect(url_for('update_message'))

@app.route('/company_logout')
@company_auth_required
def company_logout():
    session.pop('company_id')
    return redirect(url_for('company_login'))