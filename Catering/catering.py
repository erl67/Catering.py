REBUILD_DB = True

import os
# from tendo import singleton    #not helpful for debugging
# inst = singleton.SingleInstance() 

from flask import Flask, g, send_from_directory, flash, render_template, abort, request, redirect, url_for, session, Response
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime


from models import db, User, Event, populateDB
from utils import eprint, getUsers, getEvents

def create_app():
    app = Flask(__name__)
    DB_NAME = os.path.join(app.root_path, 'catering.db')
    
    app.config.update(dict(
        DEBUG=True,
        DEBUG_TB_INTERCEPT_REDIRECTS = True,
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

@app.cli.command('initdb')
def initdb_command():
    db.drop_all()
    db.create_all()
    populateDB()
    print('Initialized the database.')
    
@app.before_request
def before_request():
    g.user = None
    g.events = None
    if 'uid' in session:
        g.user = User.query.filter_by(id=session['uid']).first()
        if g.user.staff == True:
            g.events = Event.query.order_by(Event.id.asc()).all()
        else:
            g.events = Event.query.filter(Event.client==g.user.id).order_by(Event.date.asc()).all()
    eprint("g.user: " + str(g.user))
    eprint("g.events: " + str(g.events))
    
@app.before_first_request
def before_first_request():
    eprint("🥇")

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

@app.route("/registerstaff/")
def signerStaff():
    flash("TBD")
    abort(404)
        
@app.route("/login/", methods=["GET", "POST"])
def logger():
    if "username" in session:
        flash("Already logged in!")
        return redirect(url_for("profile", uid=session["uid"]))
    elif request.method == "POST":
        POST_USER = str(request.form['user'])
        POST_PASS = str(request.form['pass'])
        valid = User.query.filter(User.username==POST_USER, User.password==POST_PASS).first()
        eprint(str(valid))
        if (POST_USER == "owner") and (POST_PASS == "pass"):
            session["username"] = "owner"
            session["uid"] = 1
            session["staff"] = "owner"
            flash("Successfully logged in as Mr. Manager")
            return redirect(url_for("owner"))
        elif valid is not None:
            session["username"] = POST_USER
            session["uid"] = valid.id
            flash("Successfully logged in!  " + session["username"])
            if valid.staff == True:
                session["staff"] = True
                return redirect(url_for("staff", uid=session["uid"]))
            else:
                return redirect(url_for("customer", uid=session["uid"]))
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
            return render_template("accounts/curProfile.html", name=g.user)
        elif User.query.filter(User.id==uid).first() != None:
            return render_template("accounts/otherProfile.html", name=User.query.filter(User.id==uid).first().username)
        else:
            abort(404)
    else:
        return Response(render_template("accounts/loginPage.html"), status=200, mimetype='text/html')
        abort(404)

@app.route("/owner/")
def owner():
    if g.user.id != 1:
        return redirect(url_for("index"))
    elif g.user.id == 1:
        if Event.query.count() < 1: 
            flash("no events scheduled")
        else:
            next = Event.query.order_by(Event.date.asc()).first()   #filter by now to avoid dates in past
            days = str((next.date - datetime.now()).days)
            flash("next event: " + str(next.eventname))
            flash("in " + days + " days")
        return render_template("types/owner.html", user=g.user, events=g.events)
    else:
        abort(404)
        
@app.route("/staff/<uid>")
def staff(uid=None):
    if not uid:
        return redirect(url_for("index"))
    elif g.user.staff == True and g.user.id == int(uid):
        return render_template("types/staff.html", user=g.user)
    else:
        abort(404)
        
        
@app.route("/customer/")
def customers(uid=None):
    if not g.user:
        flash("must be logged in")
        return(url_for("index"))
    return Response(render_template("types/customer.html", user=g.user, items=g.events), status=200, mimetype='text/html')


@app.route("/customer/<uid>")
def customer(uid=None):
    eprint("customer: " + uid + " " + str(g.user.staff))
    eprint("g.user.id == uid" + str(g.user.id) + "==" + uid + " returns:" + str(g.user.id == uid))
    if not uid:
        return redirect(url_for("customers"))
    elif (g.user.staff == False) and (int(g.user.id) == int(uid)):
        return redirect(url_for("customers"))
    elif (g.user.id == 1):
        flash("Viewing customer page as owner")
        return redirect(url_for("customers"))
    elif (g.user.staff == True):
        flash("Viewing customer page as staff")
        return redirect(url_for("customers"))
    else:
        return Response("something is broke here", status=200, mimetype='text/html')
        
@app.route("/logout/")
def unlogger():
    if "username" in session:
        session.clear()
        flash("Successfully logged out!")
        return redirect(url_for("index"))
    else:
        flash("Not currently logged in!")
        return redirect(url_for("logger"))

@app.route("/events/")
def events():
    if g.user.staff != True:
        flash("Access to events denied.")
        return redirect(url_for("index"))
    elif g.user.staff == True:
        flash("List of all events.")
        return render_template("events/events.html", events=Event.query.order_by(Event.date.asc()).all())
    else:
        abort(404)
        
@app.route("/events/<eid>")
def event(eid=None):
    if g.user.staff != True:
        flash("Access to events denied.")
        return redirect(url_for("index"))
    elif g.user.staff == True:
        eprint("staff")
        eventRS = Event.query.filter(Event.id==int(eid)).first()
        eprint("\n" + str(eventRS) + "\n")
        if eventRS == None:
            flash("Event Id not found")
            return redirect(url_for("events"))
        else:
            return render_template("events/event.html", event=eventRS)
    else:
        abort(404)
        
        
        
        
@app.route("/newevent/")
def newEvent():
    if g.user:
        return render_template("events/newEvent.html")
    else:
        abort(404)

@app.route("/db/")
def rawstats():
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
    return Response(render_template('404.html', errno=error), status=418, mimetype='text/html')

@app.route('/favicon.ico') 
def favicon():
    #eprint('loading icon')
    return send_from_directory(os.path.join(app.root_path, 'static'), 'faviconF.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    print('Starting......')
    app.run()
#     app.run(use_reloader=False)
