

from twitter import *
from flask_bootstrap import Bootstrap
from flask import Flask, render_template


app = Flask(__name__)
broker_url = 'amqp://guest@localhost'


try:
    import json
except ImportError:
    import simplejson as json

config = {}
execfile("config.py", config)

class Twitter():


    twitter = Twitter(
		auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

    #username = raw_input("Enter username to search: @")

    def getUserProfile(self,username):
        user = self.twitter.users.search(q = username)
        for user in user:
            print "Profile image: %s" % user["profile_image_url"]
            print "Username: @%s" % user["screen_name"]
            print "Name: %s" % user["name"]
            print "Twitter ID: %s" % user["id"]
            print "Bio: %s" % user["description"]
            print "Followers: %s " % user["followers_count"]
            print "Account created since: %s" %  user["created_at"]
        return user

    followingName = []
    followingImgURL = []
    followingCount = 0

    def getFollowingCount(self):
        return self.followingCount

    def getFollowingName(self):
        return self.followingName

    def getFollowingImgURL(self):
        return self.followingImgURL

    def getFollowingInfo(self,username):
        friends = self.twitter.friends.ids(screen_name=username)
        self.followingCount = len(friends["ids"])
        for n in range(0, len(friends["ids"]), 100):
            ids = friends["ids"][n:n+100]

            subquery = self.twitter.users.lookup(user_id = ids)
            for user in subquery:
                #print " [%s] %s - %s [%s]" % ("*" if user["verified"] else " ", user["screen_name"], user["location"], user["description"])
                name = ''
                name = name + user["screen_name"].encode('utf-8')
                self.followingName.append(name)
                url = ''
                url = url + user["profile_image_url"].encode('utf-8')
                self.followingImgURL.append(url)

    tweet = []
    tweetSource = []
    tweetTime = []
    tweetLocation = []

    def getTweetList(self):
        return self.tweet

    def getTweetSource(self):
        return self.tweetSource

    def getTweetTime(self):
        return self.tweetTime

    def getTweetLocation(self):
        return self.tweetLocation

    def getTweets(self, username):
        tw = self.twitter.statuses.user_timeline(screen_name=username, exclude_replies="false")
        # print tweet
        for tw in tw:
            t = ''
            t = t + tw["text"]
            self.tweet.append(t)
            source = ''
            source = source + tw["source"].encode('utf-8')
            self.tweetSource.append(source)
            time = ''
            time = time + tw["created_at"].encode('utf-8')
            self.tweetTime.append(time)
            coordinates = tw["coordinates"]
            str = {}
            if coordinates != None:
                str = tw["coordinates"]
            else:
                continue
            self.tweetLocation.append(str)

    followerName = []
    followerImgURL = []
    followerCount = 0

    def getFollowerName(self):
        return self.followerName

    def getFollowerImgURL(self):
        return self.followerImgURL

    def getFollowerCount(self):
        return self.followerCount

    def getFollowerInfo(self,username):
        count = self.twitter.followers.ids(q=username)
        self.followerCount = len(count["ids"])
        for n in range(0, len(count["ids"]), 100):
            ids = count["ids"][n:n + 100]
            #
            subquery = self.twitter.users.lookup(user_id=ids)
            for user in subquery:
                # print " [%s] %s - %s [%s]" % ("*" if user["verified"] else " ", user["screen_name"], user["location"], user["description"])
                name = ''
                name = name + user["screen_name"].encode('utf-8')
                self.followerName.append(name)
                url = ''
                url = url + user["profile_image_url"].encode('utf-8')
                self.followerImgURL.append(url)

x = Twitter()

@app.route("/")
def index():
    return "WELCOME"


@app.route("/profile/<username>")
def profile(username):
    user = x.getUserProfile(username)
    x.getFollowingInfo(username)
    followingCount = x.getFollowingCount()
    followingName = x.getFollowingName()
    followingImgURL = x.getFollowingImgURL()

    x.getFollowerInfo(username)
    followerCount = x.getFollowerCount()
    followerName = x.getFollowerName()
    followerImgURL = x.getFollowerImgURL()

    x.getTweets(username)
    getTweetList = x.getTweetList()
    getTweetSource = x.getTweetSource()
    getTweetTime = x.getTweetTime()
    getTweetLocation = x.getTweetLocation()

    return render_template("Twitter.html", user=user, followingCount=followingCount, followingName=followingName, followingImgURL=followingImgURL,
                           followerCount=followerCount, followerName=followerName, followerImgURL=followerImgURL,
                           getTweetList=getTweetList, getTweetSource=getTweetSource, getTweetTime=getTweetTime, getTweetLocation=getTweetLocation)

app.static_folder = 'static'
app.run(debug=True)

#x = Twitter()
#x.getUserProfile()
#x.getConnections()
#x.getTweets()
#x.getFriendship()

