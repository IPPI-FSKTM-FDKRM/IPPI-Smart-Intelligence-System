

from twitter import *
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
        count = self.twitter.followers.ids(screen_name=username)
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

