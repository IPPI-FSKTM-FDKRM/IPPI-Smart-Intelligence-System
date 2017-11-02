import requests
import json
import time
from datetime import date,datetime
from dateutil import tz
from flask import Flask, render_template
from instagram.client import InstagramAPI
import pytz
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from instagram.bind import InstagramAPIError


app = Flask(__name__)

class Instagram():
    token = "38254173.b20129c.6db34c4c1f80445fa9d3946e84fdd50d" # Obtained from https://www.instagram.com/developer/
    client_id = "b20129c9e6c04c009d310c99b0d490e0" # Obtained from https://www.instagram.com/developer/
    client_secret = "e0fc4d2c42734a668096137bb4cd30ed" # Obtained from https://www.instagram.com/developer/
    api = InstagramAPI(access_token=token, client_secret=client_secret)

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
        recent_media, nextt = self.api.user_recent_media(user_id=userID, count=10)
        if not recent_media:
            print "Can't retrieve user media"
        else:
            for media in recent_media:

                print "Id = " + media.id
                print "Image = " + media.images['standard_resolution'].url
                print "Caption = " + media.caption.text
                print "Time = " , media.created_time.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))
                """print "Likes = " , media.likes.count"""
                print "Location = " + media.location.name

                print

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

'''var = raw_input("Who do you want to search?")
hai.user_search(var)
var1 = raw_input("Which profile do you want to view?")
hai.user_profile(var1)
print
#hai.user_media(var1)
var2 = raw_input("Which image do you want to view the comments?")
hai.comment_media(var2)
#var3 = raw_input("User previous location")
#hai.location(var3)'''





@app.route("/")
def index():
    return "Welcome"

@app.route("/search/<word>")
def user_search(word):
    profile = hai.user_search(word)
    return render_template("search.html", result=profile)

@app.route("/profile/<username>")
def profile(username):
    user = hai.user_profile(username)
    print user
    #media = hai.user_media(username)

    return render_template("Instagram.html", user = user)
app.run(debug=True)

#            <!--<a href="{{ url_for('profile', username = result.id) }}"> View profile :</a>-->