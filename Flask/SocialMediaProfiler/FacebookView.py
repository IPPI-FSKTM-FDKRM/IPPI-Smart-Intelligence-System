import base64
import json
import os

import Visualization
import StringIO
import requests

from datetime import datetime
from flask_login import  login_required
from flask import render_template, jsonify, request
from flask_googlemaps import Map
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
    result  = fb.Find(data);
    print result

    return jsonify({'result': render_template("facebook_searchResult.html", result=result['data'])})

@app.route("/facebook/analysis")
@login_required
def facebookAnalysis():
    postHour , postMonth, postDay = fb.getTimePost()
    location = fb.getLocationPost()
    topic = fb.getTopic()
    posnegneu = fb.getPostNegNeu()
    topicGraph = getTopicChart()
    timeGraph = getTimeChart()
    posnegneuGraph = getPosNegNeuChart()

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
            str = loc[1]+"<a href='https://facebook.com/"+loc[0]+"'><br><div al>"+tagUser+"</div></a>"
            print str
            markers.insert(0, {             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                                            'lat': loc[2],
                                            'lng': loc[3],
                                            'infobox': str })
        sndmap = Map(
            style="height:480px;width:950px;margin:0;",
            identifier="cluster-map",
            lat=location[0][2],
            lng=location[0][3],
            markers=markers,
            fit_markers_to_bounds = True

        )

    else:
        sndmap = Map(
            style="height:480px;width:950px;margin:0;",
            identifier="cluster-map",
            lat=0,
            lng=0
            # fit_markers_to_bounds=True

        )
    return render_template("facebook_Analysis.html", posnegneuGraph=posnegneuGraph,timeGraph=timeGraph , topicGraph = topicGraph,posnegneu=posnegneu,topic=topic, postHour=postHour, postMonth=postMonth, postDay=postDay, sndmap=sndmap)

def getPosNegNeuChart():
    fig = Visualization.pieChart(fb.getPostNegNeu())
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    posNegNeu_graph = base64.b64encode(img.getvalue())
    return posNegNeu_graph

def getTopicChart():
    fig = Visualization.pieChart(fb.getTopic())
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    topic_graph = base64.b64encode(img.getvalue())
    return topic_graph

def getTimeChart():
    hour, Month, Day  = fb.getTimePost()
    fig = Visualization.barChart(hour,"time(Hour)","Number of post")
    img = StringIO.StringIO()
    fig.savefig(img, format='png', transparent=True)
    img.seek(0)
    time_graph = base64.b64encode(img.getvalue())
    return time_graph

@app.route("/facebook/profile/relation/<currentId>/<id>")
@login_required
def facebookRelation(id,currentId):
    print "relation"
    print currentId
    cache_comment, cache_like = fb.get_relation_post(id)
    relationProfile = fb.getProfileInstance(id)
    name = fb.getProfile(currentId)['name']
    relationLocation = fb.getLocationRelatioin()

    # relationLocation = {u'1661021870583831': [{'lat': 3.13983145, 'lng': 101.64764368333, 'post': {u'created_time': u'2017-11-08T11:27:17+0000', u'message': u'Main lawn bowl bersama Raam Kanaisan Irfan Kamaruddin dan Hazim Kamaruzzaman\n\n#FYPpurpose', u'story': u'Khairul Albertado Danial is with Raam Kanaisan and 2 others at Malaysian Lawn Bowls Federation.', u'id': u'1362815530452737_1539814052752883'}}], u'1898030863542173': [{'lat': 3.120446, 'lng': 101.654622, 'post': {u'created_time': u'2017-11-24T15:47:36+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Kolej Kediaman Kelapan,Universiti Malaya.', u'id': u'1362815530452737_1554897484577873'}}], u'10208163758610976': [{'lat': 3.120446, 'lng': 101.654622, 'post': {u'created_time': u'2017-11-24T15:47:36+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Kolej Kediaman Kelapan,Universiti Malaya.', u'id': u'1362815530452737_1554897484577873'}}], u'10214804744656245': [{'lat': 3.120446, 'lng': 101.654622, 'post': {u'created_time': u'2017-11-24T15:47:36+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Kolej Kediaman Kelapan,Universiti Malaya.', u'id': u'1362815530452737_1554897484577873'}}, {'lat': 3.13983145, 'lng': 101.64764368333, 'post': {u'created_time': u'2017-11-08T11:27:17+0000', u'message': u'Main lawn bowl bersama Raam Kanaisan Irfan Kamaruddin dan Hazim Kamaruzzaman\n\n#FYPpurpose', u'story': u'Khairul Albertado Danial is with Raam Kanaisan and 2 others at Malaysian Lawn Bowls Federation.', u'id': u'1362815530452737_1539814052752883'}}], u'1501641643217956': [{'lat': 3.120446, 'lng': 101.654622, 'post': {u'created_time': u'2017-11-24T15:47:36+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Kolej Kediaman Kelapan,Universiti Malaya.', u'id': u'1362815530452737_1554897484577873'}}], u'1306146266088657': [{'lat': 3.13983145, 'lng': 101.64764368333, 'post': {u'created_time': u'2017-11-08T11:27:17+0000', u'message': u'Main lawn bowl bersama Raam Kanaisan Irfan Kamaruddin dan Hazim Kamaruzzaman\n\n#FYPpurpose', u'story': u'Khairul Albertado Danial is with Raam Kanaisan and 2 others at Malaysian Lawn Bowls Federation.', u'id': u'1362815530452737_1539814052752883'}}]}
    # cache_like = [{u'created_time': u'2017-10-16T12:44:58+0000', u'message': u'Hazim Kamaruzzaman Yeah manager', u'story': u"Khairul Albertado Danial shared Jawatankuasa Pelajar Luar Kampus Universiti Malaya's post.", u'id': u'1362815530452737_1519290884805200'}]
    # cache_comment = [{u'created_time': u'2017-11-24T10:26:00+0000', u'message': u'Mcm contradict je caption dgn emotions', u'from': {u'name': u'Irfan Kamaruddin', u'id': u'1661021870583831'}, u'id': u'1554649987935956_1554675254600096'}, {u'created_time': u'2017-11-21T08:00:41+0000', u'message': u'Agreed', u'from': {u'name': u'Irfan Kamaruddin', u'id': u'1661021870583831'}, u'id': u'1551861968214758_1551862704881351'}, {u'created_time': u'2017-11-19T17:55:02+0000', u'message': u'Terbaek', u'from': {u'name': u'Irfan Kamaruddin', u'id': u'1661021870583831'}, u'id': u'1549934008407554_1550434125024209'}, {u'created_time': u'2017-11-08T11:28:21+0000', u'message': u'Dah dah focus warm up cepat skit coach tgh tgu giloq', u'from': {u'name': u'Irfan Kamaruddin', u'id': u'1661021870583831'}, u'id': u'1539814052752883_1539814652752823'}, {u'created_time': u'2017-10-28T22:30:46+0000', u'message': u'Cringe at first but vida tu style pulak', u'from': {u'name': u'Irfan Kamaruddin', u'id': u'1661021870583831'}, u'id': u'1530158793718409_1530438467023775'}, {u'created_time': u'2017-10-27T20:26:13+0000', u'message': u'Tak habis habis', u'from': {u'name': u'Irfan Kamaruddin', u'id': u'1661021870583831'}, u'id': u'1526977137369908_1529464707121151'}]



    if id in relationLocation:
        relationLocation = relationLocation[id]
    else:
        relationLocation = []

    print relationLocation
    return render_template("facebook_Relation.html",
                           currentUserId = currentId,
                           username = name,
                           relationUser =id,
                           relationName = relationProfile['name'],
                           relationLocation = relationLocation,
                           comment = cache_comment,
                           like = cache_like)

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

    profile     = fb.getProfile(username)
    userID      = profile['id']
    fb.object    = userID
    post        = fb.Post()
    name        = profile['name']
    family      = fb.Family()
    post = post['data']
    friends = fb.Friends()

    return render_template("Facebook.html"
                           ,family=family
                           , friends=friends
                           , userID = userID
                           , name = name
                           , post=post)

@app.route('/facebook/nextAnalysis', methods = ['POST'])
@login_required
@celery.task
def getNextAnalysis():

    post = fb.Post()
    if "paging" in post :
        reqData = requests.get(post['paging']['next'])
        postData = reqData.json()
        like , comment , location =fb.get_post_like_comment_location(fb.loadCache(fb.getUsername()),fb.getGraph() ,postData)
        print fb.getCacheCommentsAndLikes()
        print fb.getUsername()

        return jsonify({'LikesComments': render_template('facebook_TopFriends.html', currentId=fb.getUsername(),
                                                         likes=like, comments=comment)})

    return jsonify()


@app.route('/facebook/analysis', methods=['POST'])
@login_required
@celery.task
def getAnalysis():
    print fb.getUsername()

    like , comment , location =fb.get_post_like_comment_location(fb.loadCache(fb.getUsername()),fb.getGraph() , fb.Post())
    return jsonify({ 'LikesComments': render_template('facebook_TopFriends.html', currentId=fb.getUsername(), likes=like, comments=comment)})

@app.route('/facebook/refreshAnalysis', methods=['POST'])
@login_required
@celery.task
def refreshAnalysis():
    like, comment, location = fb.get_post_like_comment_location(False, fb.getGraph(),
                                                                fb.Post())
    return jsonify({'LikesComments': render_template('facebook_TopFriends.html', likes=like, comments=comment)})

def saveCache(id):

    locationRelation = fb.getLocationRelatioin()
    posnegneu = fb.getPostNegNeu()
    hour, month,day = fb.getTimePost()
    cache_comments, cache_likes = fb.getCacheCommentsAndLikes()
    locationPost = fb.getLocationPost()
    topic = fb.getTopic()
    amount_likes , amount_comment = fb.getAmountLikesAndComments()


    data = {"day":day, "hour":hour, "month":month, "topic":topic, "posnegneu":posnegneu, "locationPost": locationPost, "amount_likes":amount_likes,
            "amount_comment":amount_comment, "cache_likes":cache_likes,"cache_comments":cache_comments,
            "locationPost":locationPost, "locationRelation":locationRelation}

    dir_path = os.path.dirname(os.path.realpath(__file__))
    filePathNameWExt = dir_path + "/Cache/" + id + '.json'
    print filePathNameWExt
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)