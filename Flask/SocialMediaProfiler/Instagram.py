import pytz
from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from instagram.client import InstagramAPI
from werkzeug.security import generate_password_hash, check_password_hash

from config import *
from forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
#------------------Database location-----------------
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/User/PycharmProjects/untitled1/database.db' #linux





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
                # print "Time = " , media.created_time.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))

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
