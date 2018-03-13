# So You Think You Can Cater

Name: Eric Laslo
Pitt ID: ERL67@pitt.edu

## Installation

1. flask run

2. http://127.0.0.1:5000/

3. If flask works on 2.6.6 it will be hosted here cs1520.ericlaslo.com



## Running the App

Initialize Database Automatically:

Set REBUILD_DB = True at beginning of program. 
	If catering.db exists it will be regenerated.
	If it doesn't exist it will be created.  No need for CLI.
	Tables will be populated with sample data in the model



Initialize Database Manually: 


goto project directory >>> cd C:\Users\E\git\201801-so-you-think-you-can-cater-erl67\Catering

set FLASK_APP=catering.py

flask initdb {drop, create, populate}