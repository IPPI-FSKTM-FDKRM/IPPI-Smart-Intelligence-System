

from twitter import *
from datetime import *
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, jsonify, url_for
from TwitterSearch import *
from collections import *
from Sentiment_Analysis import nBayesTesting
import TopicSentiment

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

    userCreatedAt = []

    def getUserProfile(self,username):
        user = self.twitter.users.show(screen_name=username)
        print "Profile image: %s" % user["profile_image_url"]
        print "Username: @%s" % user["screen_name"]
        print "Name: %s" % user["name"]
        print "Twitter ID: %s" % user["id"]
        print "Bio: %s" % user["description"]
        print "Followers: %s " % user["followers_count"]
        print "Account created since: %s" % user["created_at"]
        str = user["created_at"].encode('utf-8')
        str = str.split()
        str = str[0] + str[1] + str[2] + str[3] + str[5]
        str = datetime.strptime(str, '%a%b%d%H:%M:%S%Y')
        self.userCreatedAt = str
        return user

    def getUserCreate(self):
        return self.userCreatedAt

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
                html = user["profile_image_url"].encode('utf-8')
                html = html.replace("normal","400x400")
                url = url + html
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
        return self.tweetTime

    def getTweetLocation(self):
        print self.tweetLocation
        return self.tweetLocation

    topic = {"politic":[], "sports":[], "travel":[], "education":[],"technology":[], "spending":[]}
    posnegneu = {"positive":[], "negative":[], "neutral":[]}

    def getSentimentTopic(self):
        print self.topic
        return self.topic

    def getPolarity(self):
        print self.posnegneu
        return self.posnegneu

    hour = {}
    month = {}
    day = {}

    def getHourlyTweet(self):
        print "Hourly Tweet:"
        print self.hour
        return self.hour

    def getMonthlyTweet(self):
        print "Monthly Tweet:"
        print self.month
        return self.month

    def getDailyTweet(self):
        print "Daily Tweet:"
        print self.day
        return self.day

    def getTweets(self, username):
        tweet = []
        tweetSource = []
        tTime = []
        topic = {}
        posnegneu = {"positive":[], "negative":[], "neutral":[]}
        hour = {}
        month = {}
        day = {}

        tw = self.twitter.statuses.user_timeline(screen_name=username, count=50, exclude_replies="false")



        for tw in tw:
            t = ''
            twString = tw["text"]
            t = t + twString
            print twString
            tweet.append(t)
            getTopic = TopicSentiment.getArrayFromString(twString)
            print getTopic
            if getTopic not in topic:
                topic[getTopic] = [twString]
            else:
                if twString not in topic[getTopic]:
                    topic[getTopic].append(twString)

            getPosNegNeu = nBayesTesting.getListValue([twString])
            print getPosNegNeu
            if getPosNegNeu[0] == 'positive':
                posnegneu['positive'].append(twString)
            elif getPosNegNeu[0] == 'negative':
                posnegneu['negative'].append(twString)
            elif getPosNegNeu[0] == 'neutral':
                posnegneu['neutral'].append(twString)

            source = ''
            source = source + tw["source"].encode('utf-8')
            tweetSource.append(source)


            time = ''
            time = time + tw["created_at"].encode('utf-8')
            time = time.split()
            str = ''
            str = str + time[0] + ' ' + time[1] + ' ' + time[2] + ' ' + time[3] + ' ' + time[5]
            setTime = datetime.strptime(str, '%a %b %d %H:%M:%S %Y')
            realTime = setTime + timedelta(hours=8)
            tTime.append(realTime)

            if realTime.hour not in hour:
                hour[realTime.hour] = [twString]
            else:
                hour[realTime.hour].append(twString)

            if realTime.month not in month:
                month[realTime.month] = [twString]
            else:
                month[realTime.month].append(twString)

            if realTime.weekday() not in day:
                day[realTime.weekday()] = [twString]
            else:
                day[realTime.weekday()].append(twString)

            coordinates = tw["coordinates"]
            location = {}
            if coordinates != None:
                point = tw["coordinates"]

            else:
                continue
            self.tweetLocation.append(point)


        self.tweet = tweet
        self.tweetSource = tweetSource
        self.tweetTime = tTime
        self.topic = topic
        self.posnegneu = posnegneu
        self.hour = hour
        self.month = month
        self.day = day

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
                html = user["profile_image_url"].encode('utf-8')
                html = html.replace("normal", "400x400")
                url = url + html
                followerImgURL.append(url)
        self.followerImgURL = followerImgURL
        self.followerName = followerName