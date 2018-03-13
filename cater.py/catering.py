import os

from flask import Flask, send_from_directory, flash, render_template, abort, request, url_for, Response
# from flask_sqlalchemy import SQLAlchemy
from models import db, User, populateDB

from flask_debugtoolbar import DebugToolbarExtension



def create_app():
    app = Flask(__name__)
    
    app.config.update(dict(
        #FLASK_APP='catering.py',
        DEBUG=True,
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SECRET_KEY='erl67',
        TEMPLATES_AUTO_RELOAD = True,
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'catering.db')
    ))
    
    db.init_app(app)
    
    app.app_context().push()
    db.drop_all()
    db.create_all()
    populateDB()
    print('Created app.')
    
    return app

app = create_app()

# app = Flask(__name__)

# app.config.update(dict(
#     #FLASK_APP='catering.py',
#     DEBUG=True,
#     SQLALCHEMY_TRACK_MODIFICATIONS = False,
#     SECRET_KEY='erl67',
#     TEMPLATES_AUTO_RELOAD = True,
#     USERNAME='admin',
    PASSWORD='default',
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'catering.db')
# ))

# db.init_app(app)

# @app.cli.command('initdb')
# def initdb_command():
#     db.drop_all()
#     db.create_all()
#     populateDB()
#     print('Initialized the database.')
#     return


@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/test")
@app.route("/test/")
def tester():
    msg = 'test'
    return Response(render_template('test.html', testMessage=msg), status=203, mimetype='text/html')

@app.route("/db")
@app.route("/db/")
def testerDB():
    msg = str(User.query.all())
#     msg = User.query.limit(1).all()
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

# app = create_app()
# def loaddb():
#     app.app_context().push()
#     db.drop_all()
#     db.create_all()
#     populateDB()
#     print('Loaded the database.')

if __name__ == "__main__":
    print('Starting......')
    app.jinja_env.auto_reload = True
    toolbar = DebugToolbarExtension(app)
    app.run(use_reloader=False)
    #app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

