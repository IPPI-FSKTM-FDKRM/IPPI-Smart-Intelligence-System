import base64
import json
import os
from flask_weasyprint import HTML, render_pdf
import Visualization
import StringIO
import requests

from datetime import datetime
from Sentiment_Analysis import nBayesTesting
from flask_login import  login_required
from flask import render_template, jsonify, request, url_for
from flask_googlemaps import Map
import facebook
from SocialMediaProfiler import app, celery, fb


@app.template_filter()
def format_date(date):  # date = datetime object.
    date = datetime.strptime(date[0:16], '%Y-%m-%dT%H:%M')
    return date.strftime('%Y-%m-%d  %H:%M:%S')

@app.template_filter()
def Facebook_Get_Picture(self):
    self.modFacebook.get_picture()


@app.route("/facebook/search" )
@login_required
def facebookSearch():
    return render_template("facebook_search.html", result="")

@app.route("/facebook/searchResult",  methods=['POST'])
@login_required
def facebookSearchResult():
    data = json.loads(request.data)
    resultUser  = fb.FindUser(data)
    resultPage  = fb.FindPage(data)

    return jsonify({'result': render_template("facebook_searchResult.html", resultUser=resultUser['data'], resultPage=resultPage['data'])})

@app.route("/facebook/analysis")
@login_required
def facebookAnalysis():
    postHour , postMonth, postDay = fb.getTimePost()
    location = fb.getLocationPost()
    topic = fb.getTopic()
    posnegneu = fb.getPostNegNeu()
    topicGraph = getTopicChart("white")
    hourGraph = getHourChart(postHour,"white")
    monthGraph = getMonthChart(postMonth, "white")
    dayGraph = getDayChart(postDay,"white")
    posnegneuGraph = getPosNegNeuChart(fb.getPostNegNeu(),"white")
    address = fb.getLocationAddress()

    saveCache(fb.getUsername())


    print topic
    print postHour
    print postDay
    print postMonth
    markers = []
    if location:
        for loc in location:
            tagUser = ""
            for tag in loc[4]:
                tagUser = tagUser+"<img src = 'https://graph.facebook.com/"+tag+"/picture?type=small' style = 'width:30px; height:30px' >"
            str = "<a href='https://facebook.com/"+loc[0]+"'>"+loc[1]+"<br><div al>"+tagUser+"</div></a>"

            markers.insert(0, {'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                                'lat': loc[2],
                                'lng': loc[3],
                                'infobox': str })
        sndmap = Map(
            style="height:480px;width:950px;margin:0;",
            identifier="cluster-map",
            lat=location[0][2],
            lng=location[0][3],
            markers=markers,
            cluster=True,
            cluster_gridsize=10,
            cluster_imagepath='https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',
            fit_markers_to_bounds = True

        )

    else:
        sndmap = Map(
            style="height:480px;width:950px;margin:0;",
            identifier="cluster-map",
            lat=0,
            lng=0
        )
    return render_template("facebook_Analysis.html",  id=fb.getUsername(),address=address,
                           posnegneuGraph=posnegneuGraph,
                           dayGraph=dayGraph,
                           monthGraph=monthGraph,
                           hourGraph=hourGraph,
                           topicGraph = topicGraph,
                           posnegneu=posnegneu,
                           topic=topic,
                           postHour=postHour,
                           postMonth=postMonth,
                           postDay=postDay,
                           sndmap=sndmap)

def getPosNegNeuChart(dict , color):
    fig = Visualization.pieChartSentiment(dict, color)
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    posNegNeu_graph = base64.b64encode(img.getvalue())
    return posNegNeu_graph

def getTopicChart(color):
    fig = Visualization.pieChart(fb.getTopic(), color)
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    topic_graph = base64.b64encode(img.getvalue())
    return topic_graph

def getMonthChart(Month,color):
    figMonth = Visualization.barChartTimeNew(Month, "time(month)", "Number of post", color, 1,12)
    img = StringIO.StringIO()
    figMonth.savefig(img, format='png', transparent= True)
    img.seek(0)
    time_graph = base64.b64encode(img.getvalue())
    return time_graph

def getDayChart(Day, color):
    figDay = Visualization.barChartTimeNew(Day,"time(Day)", "Number of Post", color,0,6)
    img = StringIO.StringIO()
    figDay.savefig(img, format='png', transparent=True)
    img.seek(0)
    time_graph = base64.b64encode(img.getvalue())
    return time_graph

def getHourChart(hour,color):
    figHour = Visualization.barChartTimeNew(hour,"time(Hour)","Number of post",color,1,24)
    img = StringIO.StringIO()


    figHour.savefig(img, format='png', transparent=True)
    img.seek(0)
    time_graph = base64.b64encode(img.getvalue())
    return time_graph

@app.route("/facebook/profile/relation/<currentId>/<id>")
@login_required
def facebookRelation(id,currentId):
    print "relation"
    print currentId
    cache_comment, cache_like , cache_tag= fb.get_relation_post(id)

    relationProfile = fb.getProfileInstance(id)
    name = fb.getProfile(currentId)['name']
    relationLocation = fb.getLocationRelatioin()
    posGraph = getRelationChart(id)

    print cache_tag

    if id in relationLocation:
        relationLocation = relationLocation[id]
    else:
        relationLocation = []

    return render_template("facebook_Relation.html",
                           currentUserId = currentId,
                           username = name,
                           posGraph = posGraph,
                           relationUser =id,
                           relationName = relationProfile['name'],
                           relationLocation = relationLocation,
                           comment = cache_comment,
                           like = cache_like,
                           tags = cache_tag)

@app.route("/facebook/profile/<username>")
@login_required
def facebookProfile(username):

    print "username adalah ", fb.getUsername()


    if username == fb.getUsername():
        print fb.getUsername()
        print username
        fb.setCache(True)
    else:
        print "new user not cach"
        fb.initialize()
        fb.setUsername(username)
        fb.setCache(False)
        print "sekarang username adalah ", fb.getUsername()
    try :
        profile     = fb.getProfile(username)
        userID      = profile['id']
        fb.object    = userID
        post        = fb.Post()
        relationshipStatus = fb.getRelationShipStatus()
        name        = profile['name']
        family      = fb.Family()
        friends = fb.Friends()
        return render_template("FacebookProfile.html"
                               , family=family
                               , friends=friends
                               , userID=userID
                               , name=name
                               , relationshipStatus=relationshipStatus
                               , post=post['data']
                               , success=True
                               , error = None)
    except facebook.GraphAPIError as error:
        print error
        print error.message

        return render_template("FacebookProfile.html"
                               , family=[]
                               , friends=[]
                               , userID=[]
                               , name=[]
                               , relationshipStatus=[]
                               , post=[]
                               , success = False
                               , error = error.message)



@app.route("/facebook/pageProfile/<username>")
@login_required
def facebookPageProfile(username):

    print "username adalah ", fb.getUsername()


    if username == fb.getUsername():
        print fb.getUsername()
        print username
        fb.setCache(True)
    else:
        print "new user not cach"
        fb.initialize()
        fb.setUsername(username)
        fb.setCache(False)
        print "sekarang username adalah ", fb.getUsername()

    try:
        profile     = fb.getProfile(username)
        userID      = profile['id']
        fb.object    = userID
        post        = fb.Post()
        name        = profile['name']
        details     = fb.getPageDetails(username)

        print details

        return render_template("FacebookPageProfile.html"
                               , userID = userID
                               , name = name
                               , post=post['data']
                               , details=details
                               ,success= True
                               , error=[])

    except facebook.GraphAPIError as error:
        print error
        print error.message

        return render_template("FacebookProfile.html"
                                   , userID=[]
                                   , name=[]
                                   , post=['data']
                                   , success = False
                                   , error = error.message)


@app.route('/facebook/report/<id>')
@celery.task
def facebookReport(id):

        profile = fb.getProfile(id)
        name= profile['name']
        address = fb.getLocationAddress()
        post = fb.getPost()
        hour, month,day = fb.getTimePost()
        monthGraph = getMonthChart(month,"black")
        dayGraph = getDayChart(day,"black")
        hourGraph = getHourChart(hour,"black")

        topicGraph = getTopicChart("black")
        posnegGraph = getPosNegNeuChart(fb.getPostNegNeu(),"black")
        family = fb.Family()
        friends = fb.Friends()
        return render_template('facebookReport.html',
                              monthGraph=monthGraph,
                               dayGraph = dayGraph,
                               hourGraph = hourGraph,
                              topicGraph=topicGraph,
                              posnegGraph=posnegGraph,
                              address=address,
                              post=post,
                              userID=id,
                              family=family,
                              friends=friends,
                              name=name)

@app.route('/facebook/report_<id>.pdf')
def facebookPrintReport(id):
    profile = fb.getProfile(id)
    name = profile['name']
    address = fb.getLocationAddress()
    post = fb.getPost()
    hour, month, day = fb.getTimePost()
    timeGraph = getMonthChart(month, "black")
    topicGraph = getTopicChart("black")
    posnegGraph = getPosNegNeuChart(fb.getPostNegNeu(), "black")
    family = fb.Family()
    friends = fb.Friends()
    return render_pdf(url_for('facebookReport',id=id))


@app.route('/facebook/nextAnalysis', methods = ['POST'])
@login_required
@celery.task
def getNextAnalysis():

    post = fb.Post()
    if "paging" in post :
        reqData = requests.get(post['paging']['next'])
        postData = reqData.json()
        like , comment , tags ,location =fb.get_post_like_comment_location(fb.getUsername(),True,fb.getGraph() ,postData)
        saveCache(fb.getUsername())
        return jsonify({'LikesComments': render_template('facebook_TopFriends.html', currentId=fb.getUsername(),
                                                         tags=tags,likes=like, comments=comment)})
    return jsonify()


@app.route('/facebook/analysis', methods=['POST'])
@login_required
@celery.task
def getAnalysis():
    print fb.getUsername()
    like , comment ,tags, location =fb.get_post_like_comment_location(fb.getUsername(),fb.loadCache(fb.getUsername()),fb.getGraph() , fb.Post())
    address = fb.getLocationAddress()
    saveCache(fb.getUsername())
    return jsonify({ 'LikesComments': render_template('facebook_TopFriends.html',address=address, currentId=fb.getUsername(), likes=like, comments=comment,tags=tags)})

@app.route('/facebook/refreshAnalysis', methods=['POST'])
@login_required
@celery.task
def refreshAnalysis():
    like, comment, location = fb.get_post_like_comment_location(fb.getUsername(),False, fb.getGraph(),fb.Post())
    return jsonify({'LikesComments': render_template('facebook_TopFriends.html', likes=like, comments=comment)})

def saveCache(id):
    locationRelation = fb.getLocationRelatioin()
    posnegneu = fb.getPostNegNeu()
    hour, month,day = fb.getTimePost()
    cache_comments, cache_likes, cache_tags = fb.getCacheCommentsAndLikes()
    locationPost = fb.getLocationPost()
    topic = fb.getTopic()
    amount_likes , amount_comment , amount_tags= fb.getAmountLikesAndComments()
    address = fb.getLocationAddress()


    data = {"day":day, "hour":hour, "month":month, "topic":topic, "posnegneu":posnegneu, "locationPost": locationPost, "amount_likes":amount_likes,
            "cache_tags":cache_tags,"amount_tags": amount_tags, "amount_comment":amount_comment, "cache_likes":cache_likes,"cache_comments":cache_comments,
            "locationPost":locationPost, "locationRelation":locationRelation, "address":address}

    dir_path = os.path.dirname(os.path.realpath(__file__))
    filePathNameWExt = dir_path + "/Cache/" + id + '.json'
    print filePathNameWExt
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)



def getRelationChart(id):
    tempPosNeg = {}
    cacheComments , cacheLikes ,cachetags  = fb.getCacheCommentsAndLikes()

    if id in cacheComments:
        for i in cacheComments[id]:
            temp = nBayesTesting.getListValueString(i['message'])
            if temp not in tempPosNeg:
                tempPosNeg[temp] = [i]
            else:
                tempPosNeg[temp].append(i)

    return getPosNegNeuChart(tempPosNeg,"white")



