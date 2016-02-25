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

@app.route('/', methods=['GET', 'POST'])
def index():
	if 'email' in session:
		thetext = 'Logged in as  %s' % escape(session['email'])
	else:
		thetext = ''
	return render_template("index.html", thetext=thetext)

@app.route("/useraccount", methods=['POST'])
def echo():
	user = User.query.filter_by(email=request.form['email']).first_or_404()
	session['email'] = request.form['email']
	password = user.password
	enteredPassword = request.form['password']
	firstName = user.firstName
	lastName = user.lastName
	email = user.email
	spot = user.spot
	if 'email' in session:
		thetext =  'Logged in as  %s' % escape(session['email'])
	else:
		thetext = ''
	if password != enteredPassword:
		return 'ERROR - Password entered does not match password on file. Go back and try again'
	else:
		return render_template('useraccount.html', text=user, firstName=firstName, lastName=lastName, email=email, password=password, spot=spot, thetext=thetext)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		newUser = User(request.form['firstName'], request.form['lastName'], request.form['email'], request.form['password'], 0)
		session['email'] = request.form['email']
		#return 'Session is  %s' % escape(session['email'])
		db.session.add(newUser)
		db.session.commit()
		User.query.all()

	if request.method == 'GET':
		if 'email' in session:
			thetext =  'Logged in as  %s' % escape(session['email'])
		else:
			thetext = ''
		return render_template('signup.html', thetext=thetext)

@app.route('/choosespot', methods=['POST', 'GET'])
def choosespot():
	if 'email' in session:
		thetext =  'Logged in as  %s' % escape(session['email'])
		currentSpot = session['password']
	else:
		thetext = ''
	return render_template('choosespot.html', thetext=thetext, currentSpot=currentSpot)

@app.route('/logout')
def logout():
	session.pop('email', None)
	return 'Logged out'

if __name__ == '__main__':
	app.run(debug=True)
