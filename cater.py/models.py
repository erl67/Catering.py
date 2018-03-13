# from __main__ import *     
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column    (db.String(120), unique=True, nullable=True)
#     password = db.Column(db.String(64), unique=False, nullable=True)

    def __repr__(self):
        return "<User {}>".format(repr(self.username))
    
print('Model created.')

def populateDB():
    print('Populating DB')
    a = User(username="admin", email="admin@example.com")
    db.session.add(a)
    p = User(username="peter", email="peter@example.org")
    db.session.add(p)
    g = User(username="guest", email="guest@example.com")
    db.session.add(g)
    db.session.commit()
    print('Database filled')
    return True
