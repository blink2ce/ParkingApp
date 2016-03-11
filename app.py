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
#from flask_mail import Mail, Message

app = Flask(__name__)

#app.config.update(dict(
#    DEBUG = True,
#    MAIL_SERVER = 'smtp.gmail.com',
#    MAIL_PORT = 587, #465
#    MAIL_USE_TLS = True,
#    MAIL_USERNAME = 'hotparkingready@gmail.com',
#    MAIL_PASSWORD = 'readytorumble',
#))

#mail = Mail(app)
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
		#Need to verify that the user is logged in by checking for email in session.
		#If user is logged in, show him/her his/her account info.
		if 'email' in session:
			user = User.query.filter_by(email=session['email']).first_or_404()
			return render_template('useraccount.html', text=user, firstName=user.firstName, lastName=user.lastName, email=user.email, password=user.password, spot=user.spot, thetext=showUsername())
		else:
			return 'Error - Not logged in'


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
		return render_template('choosespot.html', thetext=showUsername(), currentSpot=user.spot, availableSpots=availableSpots)

@app.route('/switchSpots', methods=['POST', 'GET'])
def switchSpots():
	if request.method == 'GET':
		return render_template('switchSpots.html')
	else:
		return 'error'

@app.route('/confirmSwitchEmailSent', methods=['POST'])
def confirmSwitchEmailSent():
	fromaddr = "hotparkingready@gmail.com"
	toaddr = request.form['friendsEmail']
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg["Subject"] = "Will you switch your parking spot with me?"
	code = 'xyz'
	body = "Hi! " + session['email'] + ' wants to switch his/her parking spot with you. Click the link to view your account! http://127.0.0.1:5000/confirmMutualSpotSwitch User Code: ' + code
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, 'readytorumble')
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	#send email to friend
	#msg = Message("Hello", sender="hotparkingready@gmail.com", recipients=["friendsEmail"])
	#mail.send(msg)
	#msg = Message(
    #          'Hello',
	#       sender='hotparkingready@dgoogle.com',
	#       recipients=
    #           ['friendsEmail'])
	#msg.body = "This is the email body"
	#mail.send(msg)
	return "Sent"

@app.route('/confirmMutualSpotSwitch', methods=['GET'])
def confirmMutualSpotSwitch():
	return render_template('confirmMutualSpotSwitch.html')

@app.route('/MutualSpotSwitchConfirmed', methods=['POST'])
def MutualSpotSwitchConfirmed():
	userCode = request.form['userCode']
	if userCode == 'xyz':
		return send_file('templates/index.html')
	else:
		return 'error switching spots'

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
