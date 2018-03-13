# from sys import stderr
import sys
from models import User, Event


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    
def getUsers():
    msg = ""
    
    cols = User.__table__.columns.keys()
    msg += (str(cols) + "\n")
    
    resultSet = User.query.order_by(User.id.asc()).all()
    for item in resultSet:
        msg += ' '.join([str(getattr(item, col)) for col in cols]) +  "\n"
        
    return msg

def getEvents():
    msg = ""
    
    cols = Event.__table__.columns.keys()
    msg += (str(cols) + "\n")
    
    resultSet = Event.query.order_by(Event.id.asc()).all()
    for item in resultSet:
        msg += ' '.join([str(getattr(item, col)) for col in cols]) +  "\n"
        
    return msg