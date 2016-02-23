from __future__ import print_function
import sys
from flask import Flask, send_file, session
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
import os.path
import logging
from flask.json import jsonify


#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
db = SQLAlchemy(app)
user = None
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstName = db.Column(db.String(80), unique=False)
	lastName = db.Column(db.String(80), unique=False)
	email = db.Column(db.String(120), unique=False)
	password = db.Column(db.String(120), unique=False)
	spot = db.Column(db.Integer, unique=False)
	def __init__(self, firstName, lastName, email, password, spot):
		self.firstName = firstName
		self.lastName = lastName
		self.email = email
		self.password = password
		self.spot = spot

	def __repr__(self):
		return '<User %r>' % self.firstName

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
db.create_all();

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("index.html")

@app.route("/useraccount", methods=['POST'])
def echo():
	user = User.query.filter_by(email=request.form['email']).first_or_404()
	password = user.password
	enteredPassword = request.form['password']
	firstName = user.firstName
	lastName = user.lastName
	email = user.email
	spot = user.spot
	if password != enteredPassword:
		return 'ERROR - Password entered does not match password on file. Go back and try again'
	else:
		return render_template('useraccount.html', text=user, firstName=firstName, lastName=lastName, email=email, password=password, spot=spot)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
			newUser = User(request.form['firstName'], request.form['lastName'], request.form['email'], request.form['password'], 0)
			db.session.add(newUser)
			db.session.commit()
			User.query.all()
	return send_file('static/partials/signup.html')

@app.route('/choosespot', methods=['POST', 'GET'])
def choosespot():
	spot = user.spot
	return render_template('static/partials/choosespot.html', spot=user.spot)


if __name__ == '__main__':
	app.run(debug=True)
