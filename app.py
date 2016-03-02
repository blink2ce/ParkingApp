from __future__ import print_function
import sys
from flask import Flask, send_file
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask.json import jsonify
from flask import session, redirect, url_for, escape, request

app = Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

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
		def get_id():
			pass

	def __repr__(self):
		return '<User %r>' % self.firstName

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
db.create_all();

def showUsername():
	if 'email' in session:
		return  'Logged in as  %s' % escape(session['email'])
	else:
		return ''

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("index.html", thetext=showUsername())

@app.route("/useraccount", methods=['POST'])
def account():
	if request.method == "POST":
		session['email'] = request.form['email']
		user = User.query.filter_by(email=request.form['email']).first_or_404()
		password = user.password
		enteredPassword = request.form['password']
		if password != enteredPassword:
			return 'ERROR - Password entered does not match password on file. Go back and try again'
		else:
			return render_template('useraccount.html', text=user, firstName=user.firstName, lastName=user.lastName, email=user.email, password=password, spot=user.spot, thetext=showUsername())
	#if request.method == 'GET':
		#Need to verify that the user is logged in by checking for email in session.
		#If user is logged in, show him/her his/her account info.

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		newUser = User(request.form['firstName'], request.form['lastName'], request.form['email'], request.form['password'], 0)
		session['email'] = request.form['email']
		db.session.add(newUser)
		db.session.commit()
		return send_file('templates/signupConfirmed.html')

	if request.method == 'GET':
		return render_template('signup.html', thetext=showUsername())


@app.route('/confirmSpotChoice', methods=['POST'])
def confirmChoice():
	#if request.method == 'GET':
	#	if 'email' in session:
	#		thetext =  'Logged in as  %s' % escape(session['email'])
 	#	else:
	#		thetext = ''
	#	return render_template('confirmSpotChoice.html', thetext=thetext, urrentSpot = user.spot)
	choice = request.form['spotChoice']
	#Change value in database
	return 'hi'


@app.route('/choosespot', methods=['POST', 'GET'])
def choosespot():
	if request.method == 'GET':
		if 'email' in session:
			user = User.query.filter_by(email=session['email']).first()
			#find all spots that are assigned
			assignedSpots = set()
			for user in User.query.all():
				assignedSpots.add(user.spot)
			garage = set()
			count = 0
			while count <= 300:
				garage.add(count)
				count = count + 1
			#Difference between garage and assigned spots is the set of availableSpots
			availableSpots = garage - assignedSpots
		return render_template('choosespot.html', thetext=showUsername(), currentSpot = user.spot, availableSpots = availableSpots)



@app.route('/logout')
def logout():
	session.pop('email', None)
	return 'Logged out'

if __name__ == '__main__':
	app.run(debug=True)
