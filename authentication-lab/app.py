from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyA36o7RW7GxzaM875g4ZLnYOdOubH3220g",
  "authDomain": "fir-authentication-lab-b8319.firebaseapp.com",
  "projectId": "fir-authentication-lab-b8319",
  "storageBucket": "fir-authentication-lab-b8319.appspot.com",
  "messagingSenderId": "325966028459",
  "appId": "1:325966028459:web:c1929837692bff53c261ee",
  "measurementId": "G-G2S5ES09B4",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
	if request.method=="POST":
		email = request.form["email"]
		password = request.form["password"]
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for("add_tweet"))
		except:
			error = "Authentication Failed"
	return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method=="POST":
		print("hi")
		email = request.form["email"]
		password = request.form["password"]
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			return redirect(url_for("add_tweet"))
		except:
			error = "Authentication Failed"
	return render_template("signup.html")

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

@app.route("/sign_out")
def sign_out():
	return redirect(url_for("signin"))

if __name__ == '__main__':
    app.run(debug=True)