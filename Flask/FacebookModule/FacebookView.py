import json
from datetime import datetime

import requests
from flask import render_template, jsonify, request
from flask_googlemaps import Map

from Flask.SocialMediaProfiler import app, celery, fb

@app.template_filter()
def format_date(date):  # date = datetime object.
    date = datetime.strptime(date[0:16], '%Y-%m-%dT%H:%M')
    return date.strftime('%Y-%m-%d  %H:%M:%S')


@app.template_filter()
def Facebook_Get_Picture(self):
    self.modFacebook.get_picture()



@app.route("/facebook/search" )
def facebookSearch():
    return render_template("search.html", result="")

@app.route("/facebook/searchResult",  methods=['POST'])
def facebookSearchResult():
    data = json.loads(request.data)
    result  = fb.Find(data);
    print result

    return jsonify({'result': render_template("facebook_searchResult.html", result=result['data'])})

@app.route("/facebook/analysis")
def facebookAnalysis():
    postHour , postMonth, postDay = fb.getTimePost()
    location = fb.getLocationPost()
    print postHour
    print postDay
    print postMonth
    markers = []
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
    return render_template("Analysis.html", postHour=postHour, postMonth=postMonth, postDay=postDay, sndmap=sndmap)

@app.route("/facebook/profile/<username>/relation/<id>")
def facebookRelation(username, id):
    print "relation"
    cache_comment, cache_like = fb.get_relation_post(id)
    return render_template("test.html", comment = cache_comment, like =cache_like)

@app.route("/facebook/profile/<username>")
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

    return render_template("FacebookProfile.html"
                           ,family=family
                           , friends=friends
                           , userID = userID
                           , name = name
                           , post=post)

@app.route('/facebook/nextAnalysis', methods = ['POST'])
@celery.task
def getNextAnalysis():

    post = fb.Post()
    if "paging" in post :
        reqData = requests.get(post['paging']['next'])
        postData = reqData.json()
        like , comment ,tags, location =fb.get_post_like_comment_location(fb.isCache(),fb.getGraph() ,postData)
        print fb.getCacheCommentsAndLikes()

        return jsonify({ 'LikesComments': render_template('TopFriends.html', tags=tags,likes=like, comments=comment)})

    return jsonify()


@app.route('/facebook/analysis', methods=['POST'])
@celery.task
def getAnalysis():

    like , comment , tags ,location =fb.get_post_like_comment_location(fb.isCache(),fb.getGraph() , fb.Post())
    return jsonify({ 'LikesComments': render_template('TopFriends.html',tags=tags, likes=like, comments=comment)})



