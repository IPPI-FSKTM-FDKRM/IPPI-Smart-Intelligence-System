from datetime import datetime
from collections import Counter
import json
import facebook
import requests
from celery import Celery
from flask import Flask, render_template, jsonify, url_for, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import pytz    # $ pip install pytz
import tzlocal # $ pip install tzlocal

import json
import facebook
import requests
from celery import Celery
from flask import Flask, render_template, jsonify, url_for, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from FacebookModule import Facebook

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
fb = Facebook.Facebook()

class SocialMediaProfiler:

    app.config['GOOGLEMAPS_KEY'] = "AIzaSyCQaXdeh30YGYlYPK6eqt9AcAJC4or5I8w"
    GoogleMaps(app)



@app.route("/")
def index():
    return render_template("Home.html")

@app.route("/fb/searchGeneral")
def facebookSearch():
    return render_template("search.html", result="")

@app.route("/searchResult",  methods=['POST'])
def facebookSearchResult():
    data = json.loads(request.data)
    print data
    result  = fb.Find(data);
    print result

    return jsonify({'result': render_template("searchResult.html", result=result['data'])})

@app.route("/analysis")
def facebookanalysis():
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

@app.route("/fb/profile/<username>/relation/<id>")
def relation(username, id):
    print "relation"
    cache_comment, cache_like = fb.get_relation_post(id)
    return render_template("test.html", comment = cache_comment, like =cache_like)

@app.route("/fb/profile/<username>")
def profile(username):

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

@app.route('/test', methods = ["POST"])
@celery.task
def testAnaly():
    test = fb.test()
    print(test)
    return jsonify({ 'Test': render_template('test.html', test = test)})

@app.route('/getPostMonth')
@celery.task
def getPostMonth():
    postMonth = fb.month
    print postMonth
    return jsonify({ 'result': render_template('postItem.html', item = postMonth)})

@app.route('/getPostDay')
@celery.task
def getPostDay():
    postDay = fb.day
    print postDay
    return jsonify({ 'result': render_template('postItem.html', item =postDay)})


@app.route('/getPostHour')
@celery.task
def getPostHour():
    postHour = fb.hour
    print postHour
    return jsonify({ 'result': render_template('postItem.html', item = postHour)})

@app.route('/nextAnalysis', methods = ['POST'])
@celery.task
def getNextAnalysis():

    post = fb.Post()
    if "paging" in post :
        reqData = requests.get(post['paging']['next'])
        postData = reqData.json()
        like , comment , location =fb.get_post_like_comment_location(fb.isCache(),fb.getGraph() ,postData)
        print fb.getCache()

        return jsonify({ 'LikesComments': render_template('TopFriends.html', likes=like, comments=comment)})

    return jsonify()


@app.route('/analysis', methods=['POST'])
@celery.task
def getAnalysis():

    like , comment , location =fb.get_post_like_comment_location(fb.getGraph() , fb.Post())
    return jsonify({ 'LikesComments': render_template('TopFriends.html', likes=like, comments=comment)})

if __name__ == "__main__":
    fb = Facebook.Facebook()
    app.run(debug=True)
    app.static_folder = 'static'




