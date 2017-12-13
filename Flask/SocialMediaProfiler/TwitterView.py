import base64
import json
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from flask import render_template, jsonify, request, send_file, url_for
from flask_googlemaps import Map
from flask_weasyprint import HTML, render_pdf
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
    try:
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

        return render_template("Twitter.html", user=user, getCreateTime=getCreateTime, userImg=userImg,
                               followingCount=followingCount,
                               followingName=followingName, followingImgURL=followingImgURL,
                               followerCount=followerCount, followerName=followerName, followerImgURL=followerImgURL
                               )
    except Exception as e:
        return render_template("insta-private.html")





@app.route("/twitter/gettweet/<username>", methods = ['POST'])
@celery.task
def twitterGetTweet(username):
    print "starting"
    twitter.getTweets(username)
    getTweetList = twitter.getTweetList()
    getTweetSource = twitter.getTweetSource()
    getTweetTime = twitter.getTweetTime()

    return jsonify({'result': render_template("tweetTwitter.html", getTweetList=getTweetList, getTweetSource=getTweetSource, getTweetTime=getTweetTime)})

@app.route("/twitter/analysis")
def twitterAnalysis():
    getTweetLocation = twitter.getTweetLocation()
    getTweetLocationString = twitter.getTweetLocationString()
    getSentimentTopic = twitter.getSentimentTopic()
    getPolarity = twitter.getPolarity()
    getHourlyTweet = twitter.getHourlyTweet()
    getDailyTweet = twitter.getDailyTweet()
    getMonthlyTweet = twitter.getMonthlyTweet()
    getPolarityGraph = getPolarityChart("white")
    getSentimentGraph = getSentimentTopicChart("white")
    getDayChart = getDailyChart("white")
    getHourChart = getHourlyChart("white")
    getMonthChart = getMonthlyChart("white")

    markers = []
    if getTweetLocation:
        for location in getTweetLocation:
            str = "Tweet: "+location[2]+"<br>Source: "+location[4]+"<br>Time: "+datetime.strftime(location[3],'%A %b %d %H:%M:%S')
            markers.insert(0, {'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                               'lat' : location[0], 'lng' : location[1], 'infobox' : str})
            print str
        sndmap = Map(style="height:480px;width:950px;margin:0;", identifier="cluster-map",
                     lat=getTweetLocation[0][0],lng=getTweetLocation[0][1],cluster=True,cluster_gridsize=10,markers=markers,
                     cluster_imagepath='https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',
                     zoom=2,
                     # fit_markers_to_bounds=True
                     )
    else:
        sndmap = Map(
            style="height:480px;width:950px;margin:0;",
            identifier="cluster-map",
            lat=0,
            lng=0
            )

    return render_template("twitter_Analysis.html", getTweetLocation=getTweetLocation, getTweetLocationString=getTweetLocationString,
                           getSentimentTopic=getSentimentTopic, getPolarity=getPolarity, getHourlyTweet=getHourlyTweet, getDailyTweet=getDailyTweet,
                           getMonthlyTweet=getMonthlyTweet, getPolarityGraph=getPolarityGraph, getSentimentGraph=getSentimentGraph,
                           getDayChart=getDayChart, getHourChart=getHourChart, getMonthChart=getMonthChart, sndmap=sndmap)

@app.route("/twitter/report")
def twitterReport():
    userNameAlias = twitter.getUserNameAlias()
    userName = twitter.getUserName()
    userImg = twitter.getUserImg()
    userDescription = twitter.getUserDescription()
    userCreatedAt = twitter.getUserCreate()

    getTweetLocation = twitter.getTweetLocation()
    getTweetLocationString = twitter.getTweetLocationString()

    getPolarityGraph = getPolarityChart("black")
    getSentimentGraph = getSentimentTopicChart("black")
    getDayChart = getDailyChart("black")
    getHourChart = getHourlyChart("black")
    getMonthChart = getMonthlyChart("black")

    return render_template("twitterReport.html", userNameAlias=userNameAlias, userName=userName, userImg=userImg, userDescription=userDescription,
                    userCreatedAt=userCreatedAt, getPolarityGraph=getPolarityGraph, getSentimentGraph=getSentimentGraph,
                    getDayChart=getDayChart, getHourChart=getHourChart, getMonthChart=getMonthChart, getTweetLocation=getTweetLocation,
                    getTweetLocationString=getTweetLocationString)

@app.route("/twitter/twitterReport.pdf")
def twitterToPDF():
    return render_pdf(url_for("twitterReport"))


def getPolarityChart(color):
    fig = Visualization.pieChartSentiment(twitter.getPolarity(),color)
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    polarity_graph = base64.b64encode(img.getvalue())
    return polarity_graph

def getSentimentTopicChart(color):
    fig = Visualization.pieChart(twitter.getSentimentTopic(),color)
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    sentiment_graph = base64.b64encode(img.getvalue())
    return sentiment_graph

def getDailyChart(color):
    fig = Visualization.barChartTimeNew(twitter.getDailyTweet(), 'Day', 'Frequency',color,0,6)
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    daily_graph = base64.b64encode(img.getvalue())
    return daily_graph

def getMonthlyChart(color):
    fig = Visualization.barChartTimeNew(twitter.getMonthlyTweet(), 'Month', 'Frequency',color,1,12)
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    monthly_graph = base64.b64encode(img.getvalue())
    return monthly_graph

def getHourlyChart(color):
    fig = Visualization.barChartTimeNew(twitter.getHourlyTweet(), 'Hour', 'Frequency',color,0,23)
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    hourly_graph = base64.b64encode(img.getvalue())
    return hourly_graph