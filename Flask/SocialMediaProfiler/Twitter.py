

from twitter import *
from datetime import *
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, jsonify, url_for
from TwitterSearch import *
from collections import *


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
		auth = OAuth(config["ACCESS_KEY"], config["ACCESS_SECRET"], config["CONSUMER_KEY"], config["CONSUMER_SECRET"]))

    #username = raw_input("Enter username to search: @")

    def searchUser(self,username):
        user = self.twitter.users.search(q = username)
        return user

    def getUserProfile(self,username):
        user = self.twitter.users.show(screen_name=username)
        print "Profile image: %s" % user["profile_image_url"]
        print "Username: @%s" % user["screen_name"]
        print "Name: %s" % user["name"]
        print "Twitter ID: %s" % user["id"]
        print "Bio: %s" % user["description"]
        print "Followers: %s " % user["followers_count"]
        print "Account created since: %s" % user["created_at"]
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
        followingName = []
        followingImgURL = []
        friends = self.twitter.friends.ids(screen_name=username)
        self.followingCount = len(friends["ids"])
        limit = len(friends["ids"])
        print limit
        if limit >= 2000:
            limit = 2000
        else:
            limit = len(friends["ids"])
        for n in range(0, limit, 100):
            ids = friends["ids"][n:n+100]

            subquery = self.twitter.users.lookup(user_id = ids)
            for user in subquery:
                #print " [%s] %s - %s [%s]" % ("*" if user["verified"] else " ", user["screen_name"], user["location"], user["description"])
                name = ''
                name = name + user["screen_name"].encode('utf-8')
                followingName.append(name)
                url = ''
                url = url + user["profile_image_url"].encode('utf-8')
                followingImgURL.append(url)
        self.followingName = followingName
        self.followingImgURL = followingImgURL

    tweet = []
    tweetSource = []
    tweetTime = []
    tweetLocation = []

    def getTweetList(self):
        return self.tweet

    def getTweetSource(self):
        s = self.tweetSource
        source = []
        for tweet in s:
            str = ''
            tweet = tweet.replace('>', ' ')
            tweet = tweet.replace('<', ' ')
            tweet = tweet.split()
            target = "Twitter"
            for i,w in enumerate(tweet):
                if w == target:
                    str = tweet[i] + " "
                    str = str + tweet[i+1] + " "
                    str = str + tweet[i+2]
            source.append(str)
        return source

    def getTweetTime(self):
        time = self.tweetTime
        tTime = []
        for i in time:
            i = i.split()
            str = ''
            str = str + i[0] + ' ' + i[1]+ ' ' + i[2]+ ' ' + i[3] + ' ' + i[5]
            #print str
            setTime = datetime.strptime(str, '%a %b %d %H:%M:%S %Y')
            realTime = setTime + timedelta(hours=8)
            tTime.append(realTime)
        return tTime

    def getTweetLocation(self):
        return self.tweetLocation

    def getTweets(self, username):
        tweet = []
        tweetSource = []
        tweetTime = []
        tw = self.twitter.statuses.user_timeline(screen_name=username, exclude_replies="false")
        # print tweet
        for tw in tw:
            t = ''
            t = t + tw["text"]
            tweet.append(t)
            source = ''
            source = source + tw["source"].encode('utf-8')
            tweetSource.append(source)
            time = ''
            time = time + tw["created_at"].encode('utf-8')
            tweetTime.append(time)
            coordinates = tw["coordinates"]
            str = {}
            if coordinates != None:
                str = tw["coordinates"]
            else:
                continue
            self.tweetLocation.append(str)
        self.tweet = tweet
        self.tweetSource = tweetSource
        self.tweetTime = tweetTime


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
        followerName = []
        followerImgURL = []
        count = self.twitter.followers.ids(screen_name=username)
        self.followerCount = len(count["ids"])
        limit = len(count["ids"])
        if limit >= 2000:
            limit = 2000
        else:
            limit = len(count["ids"])

        for n in range(0, limit, 100):
            ids = count["ids"][n:n + 100]
            #
            subquery = self.twitter.users.lookup(user_id=ids)
            for user in subquery:
                # print " [%s] %s - %s [%s]" % ("*" if user["verified"] else " ", user["screen_name"], user["location"], user["description"])
                name = ''
                name = name + user["screen_name"].encode('utf-8')
                followerName.append(name)
                url = ''
                url = url + user["profile_image_url"].encode('utf-8')
                followerImgURL.append(url)
        self.followerImgURL = followerImgURL
        self.followerName = followerName
