# from __main__ import *     
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(64), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)
    staff = db.Column(db.Boolean, default=False)
    
    def __init__(self, username, password, email, staff):
        self.username = username
        self.password = password
        self.email = email
        self.staff = False if staff == None else True

    def __repr__(self):
#         return self.username
        return "<User {}>".format(repr(self.username))
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    eventname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
#     created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow(), server_default=datetime.utcnow())
    
    def __init__(self, eventname, email, date, created):
        self.eventname = eventname
        self.email = email
        self.date = date
        self.created = datetime.utcnow() if created == None else created 

    def __repr__(self):
        return "<Event {}>".format(repr(self.eventname))
    

def populateDB():
    db.session.add(User(username="owner", password="pass", email="owner@catering.py", staff=None))
    db.session.add(User(username="customer", password="pass", email="customer@catering.py", staff=None))
    db.session.add(User(username="staff", password="pass", email="staff@catering.py", staff=True))
    db.session.add(User(username="admin", password="admin", email="admin@example.com", staff=None))
    db.session.add(User(username="guest2", password="guest", email="guest@example.com", staff=None))
    db.session.add(User(username="guest3", password="guest", email="guest@example.com", staff=None))
    db.session.add(Event(eventname="Grand Opening", email="test@email", date=datetime(2018, 3, 16, 23, 59), created=None))
    db.session.add(Event(eventname="Grand Closing", email="test2@email", date=datetime.utcnow()+timedelta(days=420), created=datetime.utcnow()-timedelta(days=420)))
    db.session.commit()
    print('DB Populated...') 
    return True

print('Model loaded...')

