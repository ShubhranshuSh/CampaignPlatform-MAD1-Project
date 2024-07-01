from app import app
from flask_sqlalchemy import SQLAlchemy
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
    company_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    other_industry = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text, nullable=False)
    social_media_link = db.Column(db.String(250), nullable=False)
    logo = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


    #to check whether there's an admin or not
    admin=Admin.query.filter_by(username='admin').first()
    if not admin:
        password_hash = generate_password_hash('admin')
        admin=Admin(username='admin',password_hash=password_hash,name="Admin")
        db.session.add(admin)
        db.session.commit()