import requests
import json
import time
from datetime import date,datetime
from dateutil import tz
from flask import Flask, render_template, url_for, redirect
from instagram.client import InstagramAPI
from key import GoogleKey, InstaClient_id, InstaClient_secret, InstaToken
import pytz
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from instagram.bind import InstagramAPIError


app = Flask(__name__)

class Instagram():
    profile = ""
    client_id = InstaClient_id
    api = InstagramAPI(access_token=InstaToken, client_secret=InstaClient_secret)

    app.config['GOOGLEMAPS_KEY'] = GoogleKey
    GoogleMaps(app)


    def user_search(self,nama):
        profile = self.api.user_search(q = nama)
        if not profile:
            print "User not found"
        else:
            for proff in profile:
                print "Id = " + proff.id
                print "Username : " + proff.username
                print "Profile Picture : " + proff.profile_picture
                print
        return profile

    def user_media(self, userID):
        recent_media , nextt = self.api.user_recent_media(user_id=userID, count=20)
        medialist = []
        if not recent_media:
            print "Can't retrieve user media"
        """else:
            for media in recent_media:
                print "Id = " + media.id
                print "Image = " + media.images['standard_resolution'].url
                print "Caption = " + media.caption.text
                print "Time = " , media.created_time.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))
                #print "Likes = " , media.likes.count
                #print "Location = " + media.location.name"""

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
        #if not profile:
        #    print "Profile is private"
        #else:
        print "Id = " + profile.id
        print profile
        print "Username : " + profile.username
        print "Profile Picture : " + profile.profile_picture
        print "Name : " + profile.full_name
        if profile.bio:
            print "Bio : " + profile.bio
        if profile.website:
            print "Website : " + profile.website
        print "Media : ", profile.counts['media']
        print "Follows : ", profile.counts['follows']
        print "Follow by : ", profile.counts['followed_by']

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

"""var = raw_input("Who do you want to search?")
hai.user_search(var)
var1 = raw_input("Which profile do you want to view?")
hai.user_profile(var1)
print
hai.user_media(var1)
var2 = raw_input("Which image do you want to view the comments?")
hai.comment_media(var2)"""
#var3 = raw_input("User previous location")
#hai.location(var3)





@app.route("/")
def index():
    return "Welcome"

@app.route("/search/<word>")
def user_search(word):
    profile = hai.user_search(word)
    return render_template("search.html", result=profile)

@app.route("/profile/<id>")
def user_profile(id):

    profile = hai.user_profile(id)
    print "here"
    print "Username : " + profile.username
    print profile.full_name

    media = hai.user_media(id)
    print media


    return render_template("Instagram.html", user = profile, media = media)
app.run(debug=True)

#            <!--<a href="{{ url_for('profile', username = result.id) }}"> View profile :</a>-->