from flask import Flask, flash, redirect, render_template, request, session, url_for
import os
from werkzeug.utils import secure_filename
from app import app
from models import db, Influencer, Company, Admin , Campaign
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user_category')
def user_category():
    return render_template('user_category.html')

@app.route('/welcome_msg')
def welcome_msg():
    return render_template('welcome.html')


