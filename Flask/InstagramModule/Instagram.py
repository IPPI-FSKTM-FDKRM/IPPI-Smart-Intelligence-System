import requests
import json
import time
from datetime import datetime
# from dateutil import tz
from flask import Flask, render_template
from instagram.client import InstagramAPI

"""follow = "https://api.instagram.com/v1/users/self/followed-by?access_token="
myProfile = "https://api.instagram.com/v1/users/self/?access_token="
Json = requests.get(self+token)

print Json.json()['data']"""

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
        recent_media, nextt = self.api.user_recent_media(user_id=userID, count=5)
        if not recent_media:
            print "Can't retrieve user media"
        else:
            for media in recent_media:
                print "Id = " + media.id
                print "Image = " + media.images['standard_resolution'].url
                print "Caption = " + media.caption.text

                print

    def comment_media(self, mediaID):
        recent_comment = self.api.media_comments(media_id=mediaID)
        if not recent_comment:
            print "Comments can't be found"
        else:
            for comment in recent_comment:
                #utc = datetime.strptime(comment.created_at,'%Y-%m-%d %H:%M:%S')
                #utc = comment.created_at.timetuple()
                #utc = utc.replace(tzinfo=from_zone)
                #central = utc.astimezone(to_zone)
                #print central
                print "Time : ", comment.created_at
                #print time.strptime(comment.created_at)
                print comment

    def user_profile(self, userID):
        profile = self.api.user(user_id=userID)
        if not profile:
            print "Profile is private"
        else:
            print "Id = " + profile.id
            print "Username : " + profile.username
            print "Profile Picture : " + profile.profile_picture
            print "Name : " + profile.full_name
            print "Bio : " + profile.bio
            print "Website : " + profile.website
            print "Media : ", profile.counts['media']
            print "Followers : ", profile.counts['follows']
            print "Follow by : ", profile.counts['followed_by']

hai = Instagram()

var = raw_input("Who do you want to search?")
a=hai.user_search(var)
if a:
    var1 = raw_input("Which profile do you want to view?")
    hai.user_profile(var1)


    hai.user_media(var1)
    var2 = raw_input("Which image do you want to view the comments?")
    hai.comment_media(var2)
"""
@app.route("/")
def index():
    return "Welcome"

@app.route("/search/<username>")
def user_search(username):
    result = hai.user_search(username);
    print result
    return render_template("search.html", result=result)

app.run(debug=True)"""