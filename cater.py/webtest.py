# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:31:53 2018

@author: E
"""

from flask import Flask
app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route('/')
def index():
    return header() + setTitle('Flask Test') + '<h1 onclick=\"reColor(\'page\', \'page\');\">Index Page</h1>' + footer()

@app.route('/test/')
def test():
    return header() + setTitle('Test') + '<h4 onclick=\"reColor(\'page\', \'page\');\">Test Page</h4>' + footer()

@app.route('/about')
def about():
    return header() + setTitle('About Page') + '<h4 onclick=\"reColor(\'page\', \'page\');\">About Page</h4>' + footer()

def header():
    header = """
    <!DOCTYPE html>
        <html lang="en-US" xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="robots" content="noindex">
        <meta name="googlebot" content="noindex">
        <meta name="author" content="Eric Laslo">
        <meta name="description" content="IS1061 ERL67">
        <link rel="icon" type="image/x-icon" href="http://ericlaslo.com/assets/icons/faviconf0.ico">
        <script src="http://ericlaslo.com/assets/code/footerbar.js" type="text/javascript"></script>
        <script src="http://ericlaslo.com/assets/code/color.js" type="text/javascript"></script>
        <title>Flask</title>
        </head>
        <body id="page">
        """
    return header

def footer():
    footer = """
        <script type='text/javascript'>
            colorize(['page']);
            colorizeText(['page'], false);
            footerBar();
        </script>
        </body>
        </html>
        """
    return footer

def setTitle(str):
    title = "<script type=>document.title = \'" 
    title += str
    title += "\';</script>"
    return title

if __name__ == "__main__":
    app.run()