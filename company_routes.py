from flask import Flask, flash, redirect, render_template, request, session, url_for
import os
from werkzeug.utils import secure_filename
from app import app
from models import db, Influencer, Company , Campaign , InterestedCampaigns
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

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

@app.route('/company/register')
def company_register():
    return render_template('company_register.html')

@app.route('/company/register', methods=['POST'])
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


@app.route('/company/login')
def company_login():
    return render_template('company_login.html')

@app.route('/company/login', methods=['POST'])
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

@app.route('/company/dashboard')
@company_auth_required
def company_dashboard():
    user = Company.query.filter_by(id=session['company_id']).first()
    return render_template('company_dashboard.html', user=user)

@app.route('/company/dashboard', methods=['POST'])
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


@app.route('/company/home', methods=['GET'])
@company_auth_required
def company_home():
    user = Company.query.get(session['company_id'])
    
    selected_category = request.args.get('category', '')
    selected_sort = request.args.get('sort', 'latest')

    campaigns_query = Campaign.query.filter_by(visibility='public')  # Only public campaigns

    if selected_category:
        campaigns_query = campaigns_query.filter_by(category=selected_category)

    if selected_sort == 'oldest':
        campaigns = campaigns_query.order_by(Campaign.created_at.asc()).all()
    else:
        campaigns = campaigns_query.order_by(Campaign.created_at.desc()).all()

    categories = [
        "Fashion", 
        "Beauty", 
        "Fitness and health", 
        "Travel", 
        "Food and beverage", 
        "Lifestyle", 
        "Finance", 
        "Automotive", 
        "Entertainment", 
        "Education", 
        "Business", 
        "Art and design", 
        "Sports", 
        "Sustainability and environmental", 
        "Politics and social issues"
    ]

    return render_template('company_home.html', campaigns=campaigns, categories=categories, selected_category=selected_category, selected_sort=selected_sort, user=user)



@app.route('/company/influencer_search', methods=['GET'])
@company_auth_required
def influencer_search():
    user = Company.query.get(session['company_id'])
    
    selected_category = request.args.get('category', '')

    if selected_category:
        influencers = Influencer.query.filter_by(category=selected_category).all()
    else:
        influencers = Influencer.query.all()

    categories = [
        "fashion", 
        "beauty", 
        "fitness and health", 
        "travel", 
        "food and beverage", 
        "lifestyle", 
        "finance", 
        "automotive", 
        "entertainment", 
        "education", 
        "business", 
        "art and design", 
        "sports", 
        "sustainability and environmental", 
        "politics and social issues"
    ]

    return render_template(
        'influencer_search.html',
        influencers=influencers,
        categories=categories,
        selected_category=selected_category,
        user=user
    )



@app.route('/company/influencer/<int:influencer_id>')
@company_auth_required
def influencer_view(influencer_id):
    influencer = Influencer.query.get(influencer_id)
    user = Company.query.get(session['company_id'])
    return render_template('influencer_show.html', influencer=influencer, user=user)





@app.route('/campaign_created')
@company_auth_required
def campaign_created():
    return render_template('campaign_created.html')

@app.route('/company/activity')
@company_auth_required
def company_activity():
    user = Company.query.get(session['company_id'])
    campaign = Campaign.query.filter_by(company_id=session['company_id']).all()
    return render_template('company_activity.html', campaigns=campaign, user=user)

@app.route('/campaign/add')
@company_auth_required
def campaign_add():
    return render_template('Campaign/add.html')

@app.route('/campaign/add', methods=['POST'])
@company_auth_required
def campaign_add_post():
    title = request.form.get('title')
    description = request.form.get('description')
    budget = request.form.get('budget')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    status = request.form.get('status')
    category = request.form.get('category')
    visibility = request.form.get('visibility')

    if not all([title, description, budget, start_date, end_date, status, category, visibility]):
        flash('All fields are required')
        return redirect(url_for('campaign_add'))

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        flash('Invalid date format')
        return redirect(url_for('campaign_add'))

    new_campaign = Campaign(
        title=title,
        description=description,
        budget=float(budget),
        start_date=start_date,
        end_date=end_date,
        company_id=session['company_id'],
        status=status,
        category=category,
        visibility=visibility,  # Add visibility to campaign
        created_at=datetime.utcnow()
    )

    db.session.add(new_campaign)
    db.session.commit()

    return redirect(url_for('company_activity'))

@app.route('/campaign/<int:campaign_id>/view')
@company_auth_required
def campaign_view(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)  # Use get_or_404 to handle cases where the campaign is not found
    user = Company.query.get_or_404(session['company_id'])  # Use get_or_404 to handle cases where the company is not found
    return render_template('Campaign/show.html', campaign=campaign, user=user)

@app.route('/campaign/<int:campaign_id>/edit')
@company_auth_required
def campaign_edit(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        flash('Campaign not found')
        return redirect(url_for('company_activity'))
    return render_template('Campaign/edit.html', campaign=campaign)

@app.route('/campaign/<int:campaign_id>/edit', methods=['POST'])
@company_auth_required
def campaign_edit_post(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    title = request.form.get('title')
    description = request.form.get('description')
    budget = request.form.get('budget')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    status = request.form.get('status')
    category = request.form.get('category')
    visibility = request.form.get('visibility')

    if not all([title, description, budget, start_date, end_date, status, category, visibility]):
        flash('All fields are required')
        return redirect(url_for('campaign_edit', campaign_id=campaign.id))

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        flash('Invalid date format')
        return redirect(url_for('campaign_edit', campaign_id=campaign.id))

    campaign.title = title
    campaign.description = description
    campaign.budget = float(budget)
    campaign.start_date = start_date
    campaign.end_date = end_date
    campaign.status = status
    campaign.category = category
    campaign.visibility = visibility  # Update visibility

    db.session.commit()

    return redirect(url_for('company_activity'))

@app.route('/campaign/<int:campaign_id>/delete')
@company_auth_required
def campaign_delete(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('Campaign/delete.html', campaign=campaign)

@app.route('/campaign/<int:campaign_id>/delete', methods=['POST'])
@company_auth_required
def campaign_delete_post(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign has been deleted successfully.')
    return redirect(url_for('company_activity'))


@app.route('/company/requests')
@company_auth_required
def company_requests():
    user = Company.query.get(session['company_id'])
    
    # Fetch requests related to this company
    requests = db.session.query(InterestedCampaigns).join(Campaign).filter(Campaign.company_id == user.id).all()
    
    # Separate requests by status
    pending_requests = [req for req in requests if req.status == 'pending']
    accepted_requests = [req for req in requests if req.status == 'accepted']
    rejected_requests = [req for req in requests if req.status == 'rejected']
    
    return render_template('company_requests.html', user=user, 
                           pending_requests=pending_requests,
                           accepted_requests=accepted_requests,
                           rejected_requests=rejected_requests)



@app.route('/company/requests/accept/<int:request_id>', methods=['POST'])
@company_auth_required
def accept_request(request_id):
    request = InterestedCampaigns.query.get(request_id)
    if request:
        request.status = 'accepted'
        db.session.commit()

        # Redirect to the actioned page to reflect the changes
        return redirect(url_for('company_actioned'))
    
    return jsonify({'status': 'error', 'message': 'Request not found'})



@app.route('/company/requests/reject/<int:request_id>', methods=['POST'])
@company_auth_required
def reject_request(request_id):
    request = InterestedCampaigns.query.get(request_id)
    if request:
        request.status = 'rejected'  # Update status instead of deleting
        db.session.commit()

        # Redirect to the actioned page to reflect the changes
        return redirect(url_for('company_actioned'))
    
    return jsonify({'status': 'error', 'message': 'Request not found'})



@app.route('/company/request_status')
@company_auth_required
def company_request_status():
    user = Company.query.get(session['company_id'])
    return render_template('company_request_status.html', user=user)





@app.route('/company/actioned')
@company_auth_required
def company_actioned():
    user = Company.query.get(session['company_id'])

    # Fetch actioned requests for this company
    actioned_requests = db.session.query(InterestedCampaigns).join(Campaign).filter(Campaign.company_id == user.id).filter(InterestedCampaigns.status.in_(['accepted', 'rejected'])).all()
    
    return render_template('company_actioned.html', user=user, actioned_requests=actioned_requests)
    















@app.route('/company_logout')
@company_auth_required
def company_logout():
    session.pop('company_id')
    return redirect(url_for('company_login'))