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

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstName = db.Column(db.String(80), unique=False)
	lastName = db.Column(db.String(80), unique=False)
	email = db.Column(db.String(120), unique=False)
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

@app.route('/', methods=['GET', 'POST'])
#def hello():
#    return render_template('showUser.html')

def index():

	#if request.method=='POST':
	#	user = User.query.filter_by(email=request.form['email']).first_or_404()
	return render_template("index.html")
		#render_template("showUser.html", text=user)
		#return send_file('templates/index.html')

		#How to show user info?
		#return render_template("show_user.html", user=user)

@app.route("/echo", methods=['POST'])
def echo():
	user = User.query.filter_by(email=request.form['email']).first_or_404()
	return render_template('showUser.html', text=user)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
			newUser = User(request.form['firstName'], request.form['lastName'], request.form['email'], request.form['password'])
			db.session.add(newUser)
			db.session.commit()
			User.query.all()
			print('Hello World!', file=sys.stderr)
	else:
			error = "Error on form"
	return send_file('static/partials/signup.html')

#def sign_the_user_up(firstName, lastName, email, password):
#	newUser = User(firstName, lastName, email, passowrd);
#	db.session.add(newUser);
#	db.session.commit();

if __name__ == '__main__':
	app.run(debug=True)
