from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'rewfmv34rj23r32'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=30) 
db = SQLAlchemy(app)

login_manager = LoginManager(app)

from quiz import models, authentication, wordsHandler

with app.app_context():
    db.create_all()


