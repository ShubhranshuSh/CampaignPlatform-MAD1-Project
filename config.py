from dotenv import load_dotenv
import os
from app import app

load_dotenv()

INFLUENCER_STATIC_FOLDER = os.path.join('profile_upload' , 'influencer') 
COMPANY_STATIC_FOLDER = os.path.join('profile_upload' , 'company')


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
INFLUENCER_UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static',INFLUENCER_STATIC_FOLDER)
COMPANY_UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static',COMPANY_STATIC_FOLDER)

app.config['INFLUENCER_UPLOAD_FOLDER'] = INFLUENCER_UPLOAD_FOLDER
app.config['COMPANY_UPLOAD_FOLDER'] = COMPANY_UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

if not os.path.exists(INFLUENCER_UPLOAD_FOLDER):
    os.makedirs(INFLUENCER_UPLOAD_FOLDER)

if not os.path.exists(COMPANY_UPLOAD_FOLDER):
    os.makedirs(COMPANY_UPLOAD_FOLDER)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
