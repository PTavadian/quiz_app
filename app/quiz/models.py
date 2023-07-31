from datetime import datetime
from flask_login import UserMixin
from quiz import db, login_manager



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    login = db.Column(db.String(50)) #, unique=True)
    psw = db.Column(db.String(500), nullable=True)
    role = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Word(db.Model, UserMixin):
    word_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lesson = db.Column(db.Integer)
    first_lng = db.Column(db.String)
    second_lng = db.Column(db.String)
    third_lng = db.Column(db.String)
    fourth_lng = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type_1 = db.Column(db.String(50))
    type_2 = db.Column(db.String(50))
    type_3 = db.Column(db.String(50))



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)







