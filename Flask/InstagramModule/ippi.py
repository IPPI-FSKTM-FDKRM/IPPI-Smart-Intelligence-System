#import requests
#import json
#import time
#from datetime import date,datetime
#from dateutil import tz
from flask import Flask, render_template, url_for, redirect, flash, request
from instagram.client import InstagramAPI
from key import *
import pytz
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from instagram.bind import InstagramAPIError
from forms import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
import os

file_path = os.path.abspath(os.getcwd()) + "\database.db"
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mnt/c/Users/user/PycharmProjects/untitled1/database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ file_path
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class Instagram():
    profile = ""
    client_id = INSTACLIENT_ID
    api = InstagramAPI(access_token=INSTATOKEN, client_secret=INSTACLIENT_SECRET)

    app.config['GOOGLEMAPS_KEY'] = GOOGLEKEY
    GoogleMaps(app)


    def user_search(self,nama):
        profile = self.api.user_search(q = nama)

        return profile

    def user_media(self, userID):
        recent_media , nextt = self.api.user_recent_media(user_id=userID, count=50)
        if not recent_media:
            print "Can't retrieve user media"
        else:
            for media in recent_media:
                print "Id = " + media.id
                print "Image = " + media.images['standard_resolution'].url
                print "Caption = " + media.caption.text
                print "Time = " , media.created_time.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))
                print "Likes = " , media.likes


        return recent_media

    def comment_media(self, mediaID):
        recent_comment = self.api.media_comments(media_id=mediaID)
        if not recent_comment:
            print "Comments can't be found"
        else:
            for comment in recent_comment:
                print "Time : ", comment.created_at.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))
                print comment

    def user_profile(self, userID):
        profile = self.api.user(user_id=userID)

        return profile

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

hai = Instagram()

@app.route("/")
def index():
    return "Welcome"

@app.route("/search/<word>")
def user_search(word=None):
    profile = hai.user_search(word)
    return render_template("page_search.html", result=profile)

@app.route("/profile/<id>")
def user_profile(id):

    profile = hai.user_profile(id)
    media = hai.user_media(id)

    return render_template("Instagram.html", user=profile, media=media)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()


if __name__ == '__main__':
    app.run(debug=True)

