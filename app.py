from flask import Flask , render_template

app = Flask(__name__)

import config

import models

import routes , company_routes , influencer_routes , admin_routes

if __name__ == '__main__':
    app.run(debug=True)