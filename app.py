from flask import Flask, send_file, session
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
import os.path

app = Flask(__name__)
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstName = db.Column(db.String(80), unique=True)
	lastName = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120), unique=False)
	def __init__(self, firstName, lastName, email, password):
		self.firstName = firstName
		self.lastName = lastName
		self.email = email
		self.password = password

	def __repr__(self):
		return '<User %r>' % self.firstName

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
db.create_all();

@app.route('/')
def index():
	return send_file('templates/index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
			newUser = User(request.form['firstName'], request.form['lastName'], request.form['email'], request.form['password']);
			db.session.add(newUser);
			db.session.commit();
	else:
			error = "Error on form"
	return send_file('static/partials/signup.html')

#def sign_the_user_up(firstName, lastName, email, password):
#	newUser = User(firstName, lastName, email, passowrd);
#	db.session.add(newUser);
#	db.session.commit();

if __name__ == '__main__':
	app.run(debug=True)
