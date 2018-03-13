REBUILD_DB = False

import os
from flask import Flask, send_from_directory, flash, render_template, abort, request, url_for, Response
# from flask_sqlalchemy import SQLAlchemy
from models import db, User, Event, populateDB
from flask_debugtoolbar import DebugToolbarExtension


def create_app():
    app = Flask(__name__)
    DB_NAME = os.path.join(app.root_path, 'catering.db')
    app.config.update(dict(
        DEBUG=True,
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SECRET_KEY='erl67',
        TEMPLATES_AUTO_RELOAD = True,
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_NAME
    ))
    db.init_app(app)
    
    if REBUILD_DB == True and os.access(DB_NAME, os.W_OK):
        os.remove(DB_NAME)
        print('DB Dropped')
    if os.access(DB_NAME, os.W_OK):
        print('DB Exists')
    else:
        app.app_context().push()
        db.drop_all()
        db.create_all()
        print('DB Created')
        populateDB()
        
    print(app.__str__(), end="  ")
    return app

app = create_app()

@app.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()
    populateDB()
    print('Initialized the database.')

@app.route("/hello")
def hello():
    return "Hello World!"

# @app.route("/test")
# @app.route("/test/")
# def tester():
#     msg = 'test'
#     return Response(render_template('test.html', testMessage=msg), status=203, mimetype='text/html')

@app.route("/db")
@app.route("/db/")
def testerDB():
    msg=""
    
    users = User.query.order_by(User.id.asc()).all()
    for user in users:
        msg = " ".join([msg, str(user.id), user.username, user.password, user.email, str(user.staff), "\n"])
   
    msg += "\n\n"
    
    events = Event.query.order_by(Event.id.asc()).all()
    for event in events:
        msg = " ".join([msg, str(event.id), event.eventname, event.email, str(event.date), str(event.created), "\n"])

    return Response(render_template('test.html', testMessage=msg), status=203, mimetype='text/html')

@app.route('/helloT/')
@app.route('/helloT/<name>')
def helloT(name=None):
    return render_template('hello.html', name=name)

@app.route('/')
def index():
    return Response(render_template('base.html'), status=203, mimetype='text/html')

@app.errorhandler(403)
@app.errorhandler(404)
def page_not_found(error):
    return Response(render_template('404.html', errno=error), status=404, mimetype='text/html')

@app.route('/404/')
def error404():
    abort(404)

@app.route('/418/')
def err418(error=None):
    return Response(render_template('418.html', errno=error), status=418, mimetype='text/html')

# @app.route('/favicon.ico') 
# def favicon(): 
#     return url_for('static', filename='favicon.ico')
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    print('Starting......')
    app.jinja_env.auto_reload = True
    toolbar = DebugToolbarExtension(app)
    app.run(use_reloader=False)
    app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

