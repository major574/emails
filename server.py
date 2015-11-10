from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
app = Flask(__name__)
app.secret_key = "whatever"
mysql = MySQLConnector('email_val')
@app.route('/')
def index():
    emails = mysql.fetch("SELECT * FROM emails")
    return render_template('index.html', emails=emails)
@app.route('/emails', methods=['POST'])
def create():
	if len(request.form['emailaddr']) < 1:
		flash("Email cannot be blank.")
	elif not EMAIL_REGEX.match(request.form['emailaddr']):
		flash("Invalid Email Address!")
	else:
		query = "INSERT INTO emails (emailaddr, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(request.form['emailaddr'])
		print query
		mysql.run_mysql_query(query)
		flash("Success!")
	return redirect('/')
app.run(debug=True)