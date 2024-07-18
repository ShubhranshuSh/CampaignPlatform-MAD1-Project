from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy(app)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name= db.Column(db.String(150), nullable=False)

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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

with app.app_context():
    db.create_all()


    #to check whether there's an admin or not
    admin=Admin.query.filter_by(username='admin').first()
    if not admin:
        password_hash = generate_password_hash('admin')
        admin=Admin(username='admin',password_hash=password_hash,name="Admin")
        db.session.add(admin)
        db.session.commit()