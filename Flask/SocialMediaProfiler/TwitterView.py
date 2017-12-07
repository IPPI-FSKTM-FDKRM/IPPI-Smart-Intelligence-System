import base64
import json
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from flask import render_template, jsonify, request, send_file
from flask_googlemaps import Map
import Visualization
# import StringIO
import StringIO

from SocialMediaProfiler import app, celery, fb, twitter

@app.route("/Twitter/search")
def twitterSearch():
    return render_template("Twitter_search.html")

@app.route("/Twitter/searchResult",  methods=['POST'])
def twitterSearchResult():
    data = json.loads(request.data)
    result  = twitter.searchUser(data)
    #print result

    return jsonify({'result': render_template("searchResultTwitter.html", result=result)})

@app.route("/profile/<username>")
def twitterProfile(username):
    user = twitter.getUserProfile(username)
    getCreateTime = twitter.getUserCreate()
    twitter.getFollowingInfo(username)
    userImg = user["profile_image_url"]
    userImg = userImg.replace("normal", "400x400")
    followingCount = twitter.getFollowingCount()
    followingName = twitter.getFollowingName()
    followingImgURL = twitter.getFollowingImgURL()

    twitter.getFollowerInfo(username)
    followerCount = twitter.getFollowerCount()
    followerName = twitter.getFollowerName()
    followerImgURL = twitter.getFollowerImgURL()

    twitter.getTweets(username)
    getTweetList = twitter.getTweetList()
    getTweetSource = twitter.getTweetSource()
    getTweetTime = twitter.getTweetTime()
    getTweetLocation = twitter.getTweetLocation()
    getSentimentTopic = twitter.getSentimentTopic()
    getPolarity = twitter.getPolarity()
    getHourlyTweet = twitter.getHourlyTweet()
    getDailyTweet = twitter.getDailyTweet()
    getMonthlyTweet = twitter.getMonthlyTweet()

    return render_template("Twitter2.html", user=user, getCreateTime=getCreateTime, userImg=userImg, followingCount=followingCount,
                           followingName=followingName, followingImgURL=followingImgURL,
                           followerCount=followerCount, followerName=followerName, followerImgURL=followerImgURL,
                           getTweetList=getTweetList, getTweetSource=getTweetSource, getTweetTime=getTweetTime, getTweetLocation=getTweetLocation)