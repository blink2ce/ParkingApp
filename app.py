from __future__ import print_function
import sys
from flask import Flask, send_file
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask.json import jsonify
from flask import session, redirect, url_for, escape, request
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

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
	wantsToSwitchWithUser = db.Column(db.Integer, unique=False)
	def __init__(self, firstName, lastName, email, password, spot, wantsToSwitchWithUser):
		self.firstName = firstName
		self.lastName = lastName
		self.email = email
		self.password = password
		self.spot = spot
		self.wantsToSwitchWithUser = wantsToSwitchWithUser
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

@app.route("/useraccount", methods=['POST', 'GET'])
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
	if request.method == 'GET':
		if 'email' in session:
			user = User.query.filter_by(email=session['email']).first_or_404()
			return render_template('useraccount.html', text=user, firstName=user.firstName, lastName=user.lastName, email=user.email, password=user.password, spot=user.spot, thetext=showUsername())
		else:
			return 'Error - Not logged in'


@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		newUser = User(request.form['firstName'], request.form['lastName'], request.form['email'], request.form['password'], 0, 0)
		session['email'] = request.form['email']
		db.session.add(newUser)
		db.session.commit()
		return send_file('templates/signupConfirmed.html')

	if request.method == 'GET':
		return render_template('signup.html', thetext=showUsername())


@app.route('/confirmSpotChoice', methods=['POST'])
def confirmChoice():
	choice = request.form['spotChoice']
	if 'email' in session:
		user = User.query.filter_by(email=session['email']).first()
		currentSpot = user.spot
		return render_template('confirmSpotChoice.html', choice=choice, thetext=showUsername(), currentSpot=currentSpot)
	else:
		return 'Error - Not logged in'

@app.route('/confirmChangedSpot', methods=['POST'])
def confirmChange():
	if 'email' in session:
		user = User.query.filter_by(email=session['email']).first()
		newSpot = request.form['newSpot']
		user.spot = newSpot
		db.session.commit()
		return render_template('confirmChangedSpot.html')
	return 'Not logged in - Please log in and try again.'

@app.route('/confirmSwitchedSpot', methods=['POST'])
def confirmSwitch():
	if 'email' in session:
		user = User.query.filter_by(email=session['email']).first()
		newSpot = request.form['newSpot']
		newSpotsUser = User.query.filter_by(spot=newSpot).first()
		sentinel = user.spot
		user.spot = newSpot
		newSpotsUser.spot = sentinel
		newSpotsUser.wantsToSwitchWithUser = None
		db.session.commit()
		#send notification to friend that the request was accepted by buddy
		fromaddr = "hotparkingready@gmail.com"
		toaddr = user.email
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg["Subject"] = "You have switched your parking spot with " + user.email
		body = "Hi! Your buddy " + user.email + "agrees to switch spots with you! Your spot has now been updated. To see your account please log in."
		msg.attach(MIMEText(body, 'plain'))
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, 'readytorumble')
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
		return render_template('confirmChangedSpot.html')
	return 'Not logged in - Please log in and try again.'


@app.route('/choosespot', methods=['POST', 'GET'])
def choosespot():
	if request.method == 'GET':
		if 'email' in session:
			theUser = User.query.filter_by(email=session['email']).first()
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
		return render_template('choosespot.html', thetext=showUsername(), currentSpot=theUser.spot, availableSpots=availableSpots, assignedSpots=assignedSpots)

@app.route('/switchSpots', methods=['POST', 'GET'])
def switchSpots():
	if request.method == 'GET':
		return render_template('switchSpots.html')
	else:
		return 'error'

@app.route('/confirmSwitchEmailSent', methods=['POST'])
def confirmSwitchEmailSent():
	spotChoice = request.form['spotChoice']
	friend = User.query.filter_by(spot=spotChoice).first()
	#send email to person who currently has the spot, asking for switch on behalf of sender
	fromaddr = "hotparkingready@gmail.com"
	toaddr = friend.email
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg["Subject"] = "Will you switch your parking spot with me?"
	body = "Hi! " + session['email'] + ' wants to switch his/her parking spot with you. Click here to login and view the request: http://127.0.0.1:5000/ '
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, 'readytorumble')
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

	user = User.query.filter_by(email=session['email']).first()
	#friend = User.query.filter_by(email=request.form['friendsEmail']).first()
	user.wantsToSwitchWithUser = friend.id
	db.session.commit()
	return "Sent"

@app.route('/confirmMutualSpotSwitch', methods=['GET'])
def confirmMutualSpotSwitch():
	return render_template('confirmMutualSpotSwitch.html')

@app.route('/switchOptions', methods=['GET'])
def switchOptions():
	#Get emails of all users who want to switch with this user
	user = User.query.filter_by(email=session['email']).first()
	listOfSuitors = User.query.filter(User.wantsToSwitchWithUser==user.id).all()
	listOfSuitorsEmails = []
	for u in listOfSuitors:
		listOfSuitorsEmails.append(u.email)
	return render_template('switchOptions.html', listOfSuitors=listOfSuitorsEmails, thetext=showUsername())

@app.route('/confirmSpotAgreement', methods=['POST'])
def confirmSpotAgreement():
	#Give page the choice of spot
	usersEmail = request.form['usersEmail']
	user = User.query.filter_by(email=usersEmail).first()
	spotToTake = user.spot
	currentUser= User.query.filter_by(email=session['email']).first()
	currentSpot = currentUser.spot
	return render_template('confirmSpotAgreement.html', choice=spotToTake, currentSpot=currentSpot, thetext=showUsername())

@app.route('/logout')
def logout():
	session.pop('email', None)
	return render_template('logout.html')

if __name__ == '__main__':
	app.run(debug=True)
