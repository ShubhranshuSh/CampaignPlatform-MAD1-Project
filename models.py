from app import app
from flask_sqlalchemy import SQLAlchemy
from pytz import timezone
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy(app)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(150), nullable=False)

influencer_campaign_association = db.Table('influencer_campaign_association',
    db.Column('influencer_id', db.Integer, db.ForeignKey('influencers.id'), primary_key=True),
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaign.id'), primary_key=True)
)

class Influencer(db.Model):
    __tablename__ = 'influencers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    interest = db.Column(db.String(255), nullable=False)
    reach = db.Column(db.Integer, nullable=False)
    social_media_links = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=False)
    campaigns = db.relationship('Campaign', secondary=influencer_campaign_association, back_populates='influencers')

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    other_industry = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    social_media_link = db.Column(db.String(200), nullable=False)
    logo = db.Column(db.String(200), nullable=False)
    campaigns = db.relationship('Campaign', backref='company', lazy=True)

class Campaign(db.Model):
    __tablename__ = 'campaign'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    category = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    visibility = db.Column(db.String(50), nullable=False, default='public')
    influencers = db.relationship('Influencer', secondary=influencer_campaign_association, back_populates='campaigns')

    @property
    def created_at_ist(self):
        utc_time = self.created_at.replace(tzinfo=timezone('UTC'))
        ist_time = utc_time.astimezone(timezone('Asia/Kolkata'))
        return ist_time

with app.app_context():
    db.create_all()

    # To check whether there's an admin or not
    admin = Admin.query.filter_by(username='admin').first()
