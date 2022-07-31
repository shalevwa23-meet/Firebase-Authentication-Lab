from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import time


config = {
  "apiKey": "AIzaSyA36o7RW7GxzaM875g4ZLnYOdOubH3220g",
  "authDomain": "fir-authentication-lab-b8319.firebaseapp.com",
  "projectId": "fir-authentication-lab-b8319",
  "storageBucket": "fir-authentication-lab-b8319.appspot.com",
  "messagingSenderId": "325966028459",
  "appId": "1:325966028459:web:c1929837692bff53c261ee",
  "measurementId": "G-G2S5ES09B4",
  "databaseURL": "https://fir-authentication-lab-b8319-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

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
		full_name = request.form["full_name"]
		user_name = request.form["user_name"]
		bio = request.form["bio"]
		user = {"email" : email, "password" : password, "full_name": full_name, "user_name": user_name, "bio": bio}
		# try:
		login_session['user'] = auth.create_user_with_email_and_password(email, password)
		db.child("Users").child(login_session["user"]["localId"]).set(user)
		return redirect(url_for("add_tweet"))
		# except:
		# 	error = "Authentication Failed"
	return render_template("signup.html")

@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == "POST":
		tweet = {"title": request.form["title"], "text": request.form["text"], "uid": login_session["user"]["localId"], "time":time.strftime("%d/%m/%Y, %H:%M",time.localtime()), "likes":0}
		db.child("Tweets").push(tweet)
	return render_template("add_tweet.html")

@app.route("/sign_out")
def sign_out():
	login_session["user"] = None
	auth.current_user = None
	return redirect(url_for("signin"))

@app.route("/all_tweets")
def all_tweets():
	return render_template("tweets.html", tweets = db.child("Tweets").get().val(), users = db.child("Users").get().val())

@app.route("/like", methods = ["GET", "POST"])
def like():
	if request.method == "POST":
		tweet = request.form["tweet"]
		likes = db.child("Tweets").child(tweet).get().val()["likes"]
		db.child("Tweets").child(tweet).update({"likes":likes+1})
	return redirect(url_for("all_tweets"))

if __name__ == '__main__':
    app.run(debug=True)