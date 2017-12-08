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


    return render_template("Twitter2.html", user=user, getCreateTime=getCreateTime, userImg=userImg, followingCount=followingCount,
                           followingName=followingName, followingImgURL=followingImgURL,
                           followerCount=followerCount, followerName=followerName, followerImgURL=followerImgURL,
                           getTweetList=getTweetList, getTweetSource=getTweetSource, getTweetTime=getTweetTime)

@app.route("/twitter/analysis")
def twitterAnalysis():
    getTweetLocation = twitter.getTweetLocation()
    getSentimentTopic = twitter.getSentimentTopic()
    getPolarity = twitter.getPolarity()
    getHourlyTweet = twitter.getHourlyTweet()
    getDailyTweet = twitter.getDailyTweet()
    getMonthlyTweet = twitter.getMonthlyTweet()
    getPolarityGraph = getPolarityChart()
    getSentimentGraph = getSentimentTopicChart()
    getDayChart = getDailyChart()
    getHourChart = getHourlyChart()
    getMonthChart = getMonthlyChart()

    markers = []
    if getTweetLocation:
        for location in getTweetLocation:
            str = location[2]+"<br>"+location[4]
            markers.insert(0, {'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                               'lat' : location[0], 'lng' : location[1], 'infobox' : str})
        sndmap = Map(style="height:480px;width:950px;margin:0;", identifier="cluster-map",
                     lat=getTweetLocation[0][0],lng=getTweetLocation[0][1],markers=markers,
                     fit_markers_to_bounds=True)
    else:
        sndmap = Map(
            style="height:480px;width:950px;margin:0;",
            identifier="cluster-map",
            lat=0,
            lng=0
            )

    return render_template("twitter_Analysis.html", getTweetLocation=getTweetLocation, getSentimentTopic=getSentimentTopic,
                           getPolarity=getPolarity, getHourlyTweet=getHourlyTweet, getDailyTweet=getDailyTweet,
                           getMonthlyTweet=getMonthlyTweet, getPolarityGraph=getPolarityGraph, getSentimentGraph=getSentimentGraph,
                           getDayChart=getDayChart, getHourChart=getHourChart, getMonthChart=getMonthChart, sndmap=sndmap)

def getPolarityChart():
    fig = Visualization.pieChartSentiment(twitter.getPolarity(),"black")
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    polarity_graph = base64.b64encode(img.getvalue())
    return polarity_graph

def getSentimentTopicChart():
    fig = Visualization.pieChart(twitter.getSentimentTopic(),"white")
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    sentiment_graph = base64.b64encode(img.getvalue())
    return sentiment_graph

def getDailyChart():
    fig = Visualization.barChart(twitter.getDailyTweet(), 'Day', 'Frequency',"white")
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    daily_graph = base64.b64encode(img.getvalue())
    return daily_graph

def getMonthlyChart():
    fig = Visualization.barChart(twitter.getMonthlyTweet(), 'Month', 'Frequency',"white")
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    monthly_graph = base64.b64encode(img.getvalue())
    return monthly_graph

def getHourlyChart():
    fig = Visualization.barChart(twitter.getHourlyTweet(), 'Hour', 'Frequency',"white")
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    hourly_graph = base64.b64encode(img.getvalue())
    return hourly_graph