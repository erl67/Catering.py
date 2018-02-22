# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:31:53 2018

@author: E
"""

from flask import Flask, flash, render_template, abort, request, Response
from flask_sqlalchemy import SQLAlchemy

from webpage import header, footer, setTitle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route('/helloT/')
@app.route('/helloT/<name>')
def helloT(name=None):
    return render_template('hello.html', name=name)

@app.route('/')
@app.route('/base/')
def index():
    return Response(render_template('base.html'), status=203, mimetype='text/html')

@app.route('/test/')
def test():
    return header() + setTitle('Test') + '<h4 onclick=\"reColor(\'page\', \'page\');\">Test Page</h4>' + footer()

@app.route('/about')
def about():
    return header() + setTitle('About Page') + '<h4 onclick=\"reColor(\'page\', \'page\');\">About Page</h4>' + footer()

@app.errorhandler(403)
@app.errorhandler(404)
def page_not_found(error):
    return Response(render_template('404.html', errno=error), status=404, mimetype='text/html')

@app.route('/404/')
def error404():
    abort(404)
    
@app.route('/404t/')
def error404t():
    return render_template('404.html')

@app.route('/418/')
def err418(error=None):
    return Response(render_template('418.html', errno=error), status=418, mimetype='text/html')

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
    app.run()