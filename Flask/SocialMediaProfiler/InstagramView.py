from flask import Flask, render_template, url_for, redirect, jsonify, request
import json, pytz, Visualization, StringIO, base64
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_googlemaps import Map, icons
from config import *
from SocialMediaProfiler import app, celery, insta



@app.route("/insta/search")
@login_required
def instaSearch():
    return render_template("insta-search.html")

@app.route("/insta/search/result", methods = ["POST"])
@login_required
def instaSearchResult():
    print "searching"
    data = json.loads(request.data)
    profile = insta.user_search(data)
    print profile

    return jsonify({'result': render_template("insta-search-result.html", result=profile)})

@app.route("/insta/profile/<id>")
@login_required
def instaProfile(id):

    #try:
        profile = insta.user_profile(id)
        media = insta.user_media(id)

        insta.location(id)
        insta.get_created_post(id)

        return render_template("insta-profile.html", user=profile, media=media)
    #except Exception as e:
    #    return render_template("insta-private.html", error = e)

@app.route("/insta/analysis")
@login_required
def analysis():
    locate = insta.getLocationInstaPost()
    topic = insta.getTopic()
    posnegneu = insta.getPostNegNeu()
    topicGraph = getTopicChart()
    dayGraph = getDayChart()
    monthGraph = getMonthChart()
    hourGraph = getHourChart()
    posnegneuGraph = getPosNegNeuChart()
    day = insta.getInstaDay()
    month = insta.getInstaMonth()
    hour = insta.getInstaHour()

    print topic
    print "----"
    print posnegneu
    print "----"
    print locate
    print "no sorted"
    print month
    print "sorted"
    aaaa = sorted(month)
    print aaaa
    markers = []
    if locate:
        for loc in locate:
            str = "<img src='" + loc[3] + "'style = 'width:150px; height:150px'><br>" + loc[0]
            markers.insert(0, {             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                                            'lat': loc[1],
                                            'lng': loc[2],
                                            'infobox': str })
        print markers
        sndmap = Map(
            style="height:480px;width:950px;margin:0;",
            identifier="sndmap",
            lat=locate[0][1],
            lng=locate[0][2],
            markers=markers,
            cluster=True,
            cluster_gridsize=10,
            cluster_imagepath='https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',
            zoom=2
            #fit_markers_to_bounds = True

        )

    else:
        sndmap = Map(
            style="height:480px;width:950px;margin:0;",
            identifier="cluster-map",
            lat=0,
            lng=0
            # fit_markers_to_bounds=True

        )
    return render_template("insta-analysis.html", sndmap=sndmap,posnegneu=posnegneu,topic=topic,posnegneuGraph=posnegneuGraph,
                           topicGraph = topicGraph, day=day, month=month, hour=hour, dayGraph = dayGraph, hourGraph = hourGraph, monthGraph = monthGraph)


def getPosNegNeuChart():
    fig = Visualization.pieChartSentiment(insta.getPostNegNeu())
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    posNegNeu_graph = base64.b64encode(img.getvalue())
    return posNegNeu_graph

def getTopicChart():
    fig = Visualization.barChart(insta.getTopic(),"Topic", "Frequency")
    img2 = StringIO.StringIO()
    fig.savefig(img2, format='png', transparent=True)
    img2.seek(0)
    topic_graph = base64.b64encode(img2.getvalue())
    return topic_graph

def getHourChart():
    fig = Visualization.lineChart(insta.getInstaHour(), "Hour", "Frequency")
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    time_graph = base64.b64encode(img.getvalue())
    return time_graph

def getMonthChart():
    fig = Visualization.lineChart(insta.getInstaMonth(), "Month", "Frequency")
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    time_graph = base64.b64encode(img.getvalue())
    return time_graph

def getDayChart():
    fig = Visualization.lineChart(insta.getInstaDay(), "Day", "Frequency")
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    time_graph = base64.b64encode(img.getvalue())
    return time_graph