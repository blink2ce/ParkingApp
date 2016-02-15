from flask import Flask, send_file, session
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
	return send_file('templates/index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		if valid_signup(request.form['firstName'],
					   request.form['lastName'],
					   request.form['email'],
					   request.form['password']):
				return sign_the_user_up(request.form['firstName'],
							   request.form['lastName'],
							   request.form['email'],
							   request.form['password'],
							   request.form['numSpots'])
		else:
			error = "Error on form - Did you fill out all the fields?"
	return send_file('static/partials/signup.html')

def valid_signup(firstName, lastName, email, password):
	return True;

def sign_the_user_up(firstName, lastName, email, password, numSpots):
	db.create_all();
	newUser = User(firstName, lastName, email, passowrd, numSpots);
	db.session.add(newUser);
	db.session.commit();

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstName = db.Column(db.String(80), unique=True)
	lastName = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120), unique=False)
	numSpots = db.Column(db.Integer, unique=False)
def __init__(self, username, email):
	self.username = username
	self.email = email

	def __repr__(self):
		return '<User %r>' % self.username

if __name__ == '__main__':
	app.run(debug=True)
