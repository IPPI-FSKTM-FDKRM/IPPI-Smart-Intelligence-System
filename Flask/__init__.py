from FacebookModule import Facebook
# from InstagramModule import Instagram
from datetime import datetime
from collections import Counter

import json
import facebook
import requests
from celery import Celery
from flask import Flask, render_template, jsonify, url_for, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

class SocialMediaProfiler:

    @app.template_filter()
    def format_date(date):  # date = datetime object.
        date = datetime.strptime(date[0:16], '%Y-%m-%dT%H:%M')
        return date.strftime('%Y-%m-%d  %H:%M:%S')

    @app.template_filter()
    def Facebook_Get_Picture(self):
        self.modFacebook.get_picture()

@app.route("/")
def index():
    return render_template("Home.html")

@app.route("/search")
def searchGeneral():
    return render_template("search.html")

@app.route("/facebookProfiling/<username>")
def facebookProfiling(username):
    print "username adalah ", fb.getUsername()

    if username == fb.getUsername():
        print fb.getUsername()
        print username
        fb.setCache(True)
    else:
        print "new user not cache"
        fb.initialize()
        fb.setUsername(username)
        fb.setCache(False)
        print "sekarang username adalah ", fb.getUsername()

    profile     = fb.getProfile(username)
    userID      = profile['id']
    fb.object   = userID
    post        = fb.Post()
    name        = profile['name']
    family      = fb.Family()
    post        = post['data']
    friends     = fb.Friends()

    return render_template("Facebook.html"
                           , family=family
                           , friends=friends
                           , userID=userID
                           , name=name
                           , post=post)

if __name__ == "__main__":
    fb = Facebook.Facebook()
    app.run(debug=True)
    app.static_folder = 'static'




