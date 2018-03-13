# from __main__ import *     
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(64), unique=False, nullable=True)
#     email = db.Column(db.String(120), unique=False, nullable=True)
    
#     def __init__(self, username, password, email):
#         self.username = username
#         self.password = password
#         self.email = email

    def __repr__(self):
        return "<User {}>".format(repr(self.username))
    
print('Model loaded...')

def populateDB():
    print('Populating DB...')
    db.session.add(User(username="owner", password="pass"))

#     db.session.add(User(username="owner", password="pass", email="owner@catering.py"))
#     db.session.add(User(username="customer", password="pass", email="customer@catering.py"))
#     db.session.add(User(username="staff", password="pass", email="staff@catering.py"))
#     db.session.add(User(username="admin", password="admin", email="admin@example.com"))
#     db.session.add(User(username="guest", password="guest", email="guest@example.com"))
    db.session.commit()
    print('Database filled...')
    return True
