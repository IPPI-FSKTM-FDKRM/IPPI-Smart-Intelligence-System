#import requests
#import json
#import time
#from datetime import date,datetime
#from dateutil import tz
import pytz
from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from instagram.client import InstagramAPI
from werkzeug.security import generate_password_hash, check_password_hash

from Flask.SocialMediaProfiler.key import *
from forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
#------------------Database location-----------------
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/User/PycharmProjects/untitled1/database.db' #linux
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\User\\PycharmProjects\\untitled1\\database.db' #windows
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Instagram():
    profile = ""
    client_id = INSTACLIENT_ID
    api = InstagramAPI(access_token=INSTATOKEN, client_secret=INSTACLIENT_SECRET)

    app.config['GOOGLEMAPS_KEY'] = GOOGLEKEY
    GoogleMaps(app)

    #search profile
    def user_search(self,nama):
        profile = self.api.user_search(q = nama)

        return profile

    #display user's profile
    def user_media(self, userID):
        recent_media , nextt = self.api.user_recent_media(user_id=userID, count=20)
        if not recent_media:
            print "Can't retrieve user media"
        else:
            for media in recent_media:
                print "Id = " + media.id
                print "Image = " + media.images['standard_resolution'].url
                #print "Caption = " + media.caption.text
                print "Time = " , media.created_time.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))

        return recent_media

    #display comment
    def comment_media(self, mediaID):
        recent_comment = self.api.media_comments(media_id=mediaID)
        if not recent_comment:
            print "Comments can't be found"
        else:
            for comment in recent_comment:
                print "Time : ", comment.created_at.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))
                print comment

    #display user's profile
    def user_profile(self, userID):
        profile = self.api.user(user_id=userID)

        return profile

    #display location
    def location(self, userID):
        recent_media, nextt = self.api.user_recent_media(user_id=userID, count=10)

        if not recent_media:
            print "Can't retrieve user media"
        else:
            for media in recent_media:
                print "Latitude = " , media.location.latitude
                print "Longitude = " , media.location.longitude
                print "Location = " + media.location.name
                print


@app.route("/")
@login_required
def index():
    return "Welcome " + current_user.username

@app.route("/insta/search/<word>")
@login_required
def user_search(word=None):
    profile = hai.user_search(word)
    return render_template("insta-search.html", result=profile)

@app.route("/insta/profile/<id>")
@login_required
def user_profile(id):
    try:
        profile = hai.user_profile(id)
        media = hai.user_media(id)
        return render_template("insta-profile.html", user=profile, media=media)
    except Exception as e:
        return render_template("insta-private.html", error = e)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error=''
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        error = 'Invalid username or password'
        return render_template("login.html", form=form, error=error)

    return render_template("login.html", form = form, error = error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> New User has been created!</h1>'

    return render_template("register.html", form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    hai = Instagram()
    app.run(debug=True)

