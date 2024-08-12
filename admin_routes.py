from flask import Flask, flash, redirect, render_template, request, session, url_for
import os
from werkzeug.utils import secure_filename
from app import app
from models import db, Influencer, Company, Admin , Campaign , InterestedCampaigns, AdRequest
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64
import plotly.graph_objects as go
import kaleido

from config import *


def admin_auth_required(func):
    @wraps(func)
    def func4(*args, **kwargs):
        if 'admin_id' in session:
            return func(*args, **kwargs)
        else:
            flash("Please login first")
            return redirect(url_for('admin_login'))
    return func4


@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin_login', methods=['POST'])
def admin_login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('All fields are required')
        return redirect(url_for('admin_login'))

    admin = Admin.query.filter_by(username=username).first()

    if not admin or not check_password_hash(admin.password_hash, password):
        flash('Invalid username or password')
        return redirect(url_for('admin_login'))

    session['admin_id'] = admin.id
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dashboard')
def admin_dashboard():
    user = session.get('admin_id')
    total_influencers = Influencer.query.count()
    total_companies = Company.query.count()
    total_campaigns = Campaign.query.count()

    
    influencer_category_counts = db.session.query(Influencer.category, db.func.count(Influencer.id)).group_by(Influencer.category).all()
    influencer_category_counts = dict(influencer_category_counts)

    company_industry_counts = db.session.query(Company.industry, db.func.count(Company.id)).group_by(Company.industry).all()
    company_industry_counts = dict(company_industry_counts)

    campaign_category_counts = db.session.query(Campaign.category, db.func.count(Campaign.id)).group_by(Campaign.category).all()
    campaign_category_counts = dict(campaign_category_counts)

    
    def create_pie_chart_3d(category_counts, title):
        labels = list(category_counts.keys())
        values = list(category_counts.values())
        
        fig = go.Figure(go.Pie(
            labels=labels, 
            values=values, 
            hoverinfo="label+percent", 
            textinfo="label+percent",
            textposition="inside",
            pull=[0.05] * len(labels),
            hole=0.3,
            marker=dict(line=dict(color='#000000', width=2)),
            showlegend=True
        ))

        fig.update_layout(
            title_text=title, 
            title_x=0.5,
            margin=dict(l=0, r=0, t=50, b=0),
            scene=dict(
                aspectmode="manual",
                aspectratio=dict(x=1, y=1, z=0.5),
            )
        )

        
        img_bytes = fig.to_image(format="png", engine="kaleido")
        chart_url = base64.b64encode(img_bytes).decode('utf-8')
        return chart_url

    
    influencer_chart_url = create_pie_chart_3d(influencer_category_counts, "Influencer Category Distribution")
    company_chart_url = create_pie_chart_3d(company_industry_counts, "Company Industry Distribution")
    campaign_chart_url = create_pie_chart_3d(campaign_category_counts, "Campaign Category Distribution")

    return render_template('admin_dashboard.html',
                           total_influencers=total_influencers,
                           total_companies=total_companies,
                           total_campaigns=total_campaigns,
                           user=user,
                           influencer_chart_url=influencer_chart_url,
                           company_chart_url=company_chart_url,
                           campaign_chart_url=campaign_chart_url)


@app.route('/admin/home')
@admin_auth_required
def admin_home():
    user = session.get('admin_id')
    selected_category = request.args.get('category', '')
    selected_sort = request.args.get('sort', 'latest')

    campaigns_query = Campaign.query.filter(Campaign.is_flag == False).filter(Campaign.status != 'done')

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

    return render_template('admin_home.html', campaigns=campaigns, categories=categories, selected_category=selected_category, selected_sort=selected_sort, user=user)



@app.route('/admin/flag_campaign/<int:campaign_id>', methods=['POST'])
@admin_auth_required
def flag_campaign(campaign_id):
    
    campaign = Campaign.query.get_or_404(campaign_id)
    
   
    campaign.is_flag = True
    
  
    db.session.commit()
    
    
    return redirect(url_for('admin_home'))


@app.route('/admin/campaign_view/<int:campaign_id>')
@admin_auth_required
def admin_campaign_view(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if not campaign:
        flash('Campaign not found!', 'error')
        return redirect(url_for('admin_home'))  
    user = Admin.query.get(session['admin_id'])
    return render_template('admin_campaign_view.html', campaign=campaign, user=user)


@app.route('/admin/campaign/flagged')
@admin_auth_required
def admin_campaign_flagged():
    user = Admin.query.get(session['admin_id'])
    campaigns = Campaign.query.filter_by(flagged=True).all()
    return render_template('admin_campaign_flagged.html', campaigns=campaigns, user=user)


@app.route('/admin/company_view')
@admin_auth_required
def admin_company_view():
    user = Admin.query.get(session['admin_id'])
    
    selected_category = request.args.get('category', '')

    if selected_category:
        companies = Company.query.filter_by(category=selected_category).all()
    else:
        companies = Company.query.all()

    categories = [
        "accommodation",
        "accommodation and food services",
        "administrative and support and waste management and remediation services",
        "agriculture, forestry, fishing and hunting",
        "air transportation",
        "ambulatory health care service",
        "amusement, gambling and recreation industry",
        "animal production",
        "apparel manufacturing",
        "arts, entertainment and recreation",
        "beverage and tobacco products manufacturing",
        "broadcasting",
        "building material and garden equipment and supplies dealers",
        "chemical manufacturing",
        "clothing and clothing accessories stores",
        "computer and electronics products manufacturing",
        "construction",
        "courier and messengers"
    ]

    return render_template(
        'admin_company_view.html',
        companies=companies,
        categories=categories,
        selected_category=selected_category,
        user=user
    )

@app.route('/admin/influencer_view')
@admin_auth_required
def admin_influencer_view():
    user = Admin.query.get(session['admin_id'])
    
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
        'admin_influencer_view.html',
        influencers=influencers,
        categories=categories,
        selected_category=selected_category,
        user=user
    )


@app.route('/admin/logout')
@admin_auth_required
def admin_logout():
    session.pop('admin_id')
    return redirect(url_for('admin_login'))