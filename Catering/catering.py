REBUILD_DB = True

import os
from tendo import singleton
inst = singleton.SingleInstance() 

from flask import Flask, g, send_from_directory, flash, render_template, abort, request, redirect, url_for, session, Response
from flask_debugtoolbar import DebugToolbarExtension

from models import db, User, Event, populateDB
from utils import eprint, getUsers, getEvents

def create_app():
    app = Flask(__name__)
    DB_NAME = os.path.join(app.root_path, 'catering.db')
    
    app.config.update(dict(
        DEBUG=False,
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
        
    app.jinja_env.auto_reload = True
    toolbar = DebugToolbarExtension(app)    
    print(app.__str__(), end="  ")
    return app

app = create_app()

@app.route("/register/", methods=["GET", "POST"])
def signer():
    if g.user:
        flash("Already logged in!")
        return redirect(url_for("profile", uid=g.user.id))
    elif request.method == "POST":
        POST_USER = str(request.form['user'])
        POST_PASS = str(request.form['pass'])
        if User.query.filter(User.username==POST_USER, User.password==POST_PASS):
            session["username"] = POST_USER
            session["uid"] = User.query.filter(User.username==POST_USER).first().id
            flash("Successfully logged in!")
            return redirect(url_for("profile", uid=session["uid"]))
        else:
            flash("Error logging you in!")
    return Response(render_template("accounts/loginPage.html"), status=200, mimetype='text/html')

@app.route("/login/", methods=["GET", "POST"])
def logger():
    if "username" in session:
        flash("Already logged in!")
        return redirect(url_for("profile", uid=session["uid"]))
    elif request.method == "POST":
        POST_USER = str(request.form['user'])
        POST_PASS = str(request.form['pass'])
        if User.query.filter(User.username==POST_USER, User.password==POST_PASS):
            session["username"] = POST_USER
            session["uid"] = User.query.filter(User.username==POST_USER).first().id
            flash("Successfully logged in!")
            return redirect(url_for("profile", uid=session["uid"]))
        else:
            flash("Error logging you in!")
    return Response(render_template("accounts/loginPage.html"), status=200, mimetype='text/html')

@app.route("/profile/")
def profiles():
    return render_template("accounts/profiles.html", users=User.query.order_by(User.id.asc()).all())

@app.route("/profile/<uid>")
def profile(uid=None):
    if not uid:
        return redirect(url_for("profiles"))
    elif g.user:
        if g.user.id == uid:
            return render_template("accounts/curProfile.html")
        elif User.query.filter(User.id==uid).first() != None:
            return render_template("accounts/otherProfile.html", name=User.query.filter(User.id==uid).first().username)
        else:
            abort(404)
    else:
        return Response(render_template("accounts/loginPage.html"), status=200, mimetype='text/html')
        abort(404)

@app.route("/logout/")
def unlogger():
    if "username" in session:
        session.clear()
        flash("Successfully logged out!")
        return redirect(url_for("events"))
    else:
        flash("Not currently logged in!")
        return redirect(url_for("logger"))

@app.route("/events/")
def events():
    return render_template("events/events.html", items=Event.query.order_by(Event.id.asc()).all())

@app.before_request
def before_request():
    g.user = None
    if 'uid' in session:
        g.user = User.query.filter_by(id=session['uid']).first()

@app.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()
    populateDB()
    print('Initialized the database.')


@app.route("/test")
@app.route("/test/")
def tester():
    msg = 'test'
    return Response(render_template('test.html', testMessage=msg), status=203, mimetype='text/html')

@app.route("/db")
@app.route("/db/")
def testDB():
    msg=""
    msg += getUsers()
    msg += "\n\n"
    msg += getEvents()
    return Response(render_template('test.html', testMessage=msg), status=203, mimetype='text/html')

@app.route('/')
def index():
    eprint('index')
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

@app.route('/favicon.ico') 
def favicon():
    eprint('loading icon')
    return send_from_directory(os.path.join(app.root_path, 'static'), 'faviconF.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    print('Starting......')
    app.run(use_reloader=False)
