from datetime import datetime
from collections import Counter


import facebook
import requests
from celery import Celery
from flask import Flask, render_template, jsonify, url_for
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

class Facebook():

    app.config['GOOGLEMAPS_KEY'] = "AIzaSyCQaXdeh30YGYlYPK6eqt9AcAJC4or5I8w"
    GoogleMaps(app)
    global cache_comments
    global cache_likes
    global user_id
    global location
    global amount_comment
    global amount_likes

    current_username = ""
    cache = False
    amount_likes = {}
    amount_comment = {}
    cache_likes = {}
    cache_comments = {}
    cache = False
    location = []

    #original app token
    # token = 'EAAFyPKV2cOIBAM1GJtjCW7oIftQzwo8RxujFy9ZBLeYNPrSNpMiuUbMAcpzvEkH6sJ0F2ZAf5ey0yle7toaSLJ2wd3yqZACnXJjKXotl8YHZA8KCLNWPBMHlV2ZAcdD4M4p8Y7RqiXV43sF5rfZCa7pmwOaZBWB6qsZD';

    token = 'EAAFyPKV2cOIBANz6EDcSV0CJAoKPt1YCeYGaWF5Tl6FLEmbELopL4XLUp5GZCS2OmwI1zNaa60D5MngsUGW4SZByLZB7w86wyZAZCR50ZAuGZC3dXZAZCLLZCAn5BDzj2UxkP1nlhZCvSmx9LAeZA3fHETSmAJIFZBZCSmooUZD'
    graph = facebook.GraphAPI(token);
    object = 'me';
    post = [];

    def initialize(self):
        print("initializing")
        amount_likes = {}
        amount_comment = {}
        cache_likes = {}
        cache_comments = {}
        cache = False
        location = []

    def getUsername(self):
        return self.current_username

    def setUsername(self, username):
        self.current_username = username

    def getCache(self):
        return cache_comments , cache_likes

    @app.template_filter()
    def format_date(date):  # date = datetime object.
        date = datetime.strptime(date[0:16], '%Y-%m-%dT%H:%M')
        return date.strftime('%Y-%m-%d  %H:%M:%S')

    @app.template_filter()
    def get_picture(self, post_id):  # date = datetime object.
        picture_url = self.graph.get_object(id=post_id, fields="picture")
        return picture_url

    def ExtendToken(self):
        app_id = '407079776317666'  # Obtained from https://developers.facebook.com/
        app_secret = 'f12509095067e4fde26fae23fdc0721f'  # Obtained from https://developers.facebook.com/
        # Extend the expiration time of a valid OAuth access token.
        extended_token = self.graph.extend_access_token(app_id, app_secret)

    def getGraph(self):
        return self.graph

    def isCache(self):
        return self.cache

    def isSameUser(self):
        return self.sameUser
    @celery.task(bind=True)
    def get_post_like_comment_location(self, graph , post):

        if not x.isCache():
            print post['data']
            cache_com = {}
            cache_like = {}
            cache_com , cache_like = x.getCache()

            print cache_com, cache_like
            for post in post['data']:
                likes = graph.get_object(id=post['id'], fields='likes')
                comment = graph.get_object(id=post['id'], fields='comments')
                place = graph.get_object(id=post['id'], fields='place')

                # if 'message' in post:
                #         print(post['message']))
                #         pos, neg = libraryTesting.testing(post['message'])
                #         print("positive " + str(pos))
                #         print("negative " + str(neg))

                if 'place' in place:
                    location.insert(0 , ( place['place']['location']['latitude'],place['place']['location']['longitude']))

                if 'likes' in likes:
                    for likes in likes['likes']['data']:

                        if not likes['id'] in amount_likes:
                            amount_likes[likes['id']] = 1;
                            cache_like[likes['id']] = [likes]
                        else:
                            amount_likes[likes['id']] += 1;
                            cache_like[likes['id']] = [likes]

                if 'comments' in comment:
                    for comments in comment['comments']['data']:

                        print comments['from']['id']
                        print comments['message']

                        if not comments['from']['id'] in amount_comment:
                            cache_com[comments['from']['id']] = [comments]
                            print cache_com[comments['from']['id']]
                            amount_comment[comments['from']['id']] = 1;
                        else:
                            cache_com[comments['from']['id']].append(comments)
                            print cache_com[comments['from']['id']]
                            amount_comment[comments['from']['id']] += 1;

        #get top commentator and likers
        if (amount_likes):
            if 'top' in amount_likes:
                amount_likes.pop('top', None)
            amount_likes['top'] = dict(Counter(amount_likes).most_common(5))
            print amount_likes

        if (amount_comment):
            if 'top' in amount_comment:
               amount_comment.pop('top', None)
            amount_comment['top'] = dict(Counter(amount_comment).most_common(5))
            print amount_comment

        if amount_likes and amount_comment :
            return amount_likes['top'] , amount_comment['top'], location

        else:
            return [], [] , None

    def get_relation_post(self, id):
        cache_com , cache_loc = x.getCache()
        print "sasa", cache_com
        if id in cache_com :
            cache_com = cache_com[id]
        else:
            cache_com = []

        if id in cache_loc :
            cache_loc = cache_loc[id]
        else:
            cache_loc = []
        return cache_com , cache_loc

    @celery.task(bind=True)
    def test(self):
        primpi = {}
        primpi['top'] = {u'1885788658114452': 19, u'10155599742768503': 4, u'1555961541130230': 1, u'10159456012925405': 5, u'1917910558461471': 1}
        return primpi['top']

    def Main(self):
        profile = self.graph.get_object(self.object);
        print profile;


    def Family(self):
        print "------------------------------------------------------------"
        print "                       Family                               "
        print "------------------------------------------------------------"
        family = self.graph.get_connections(self.object, 'family');
        print "------------------------------------------------------------"
        return family['data']

    def Friends(self):

        print "------------------------------------------------------------"
        print "                       Friends                              "
        print "------------------------------------------------------------"

        friends = self.graph.get_connections(self.object, 'friends');
        # friends = [friends['id'] for friends in friends['data']];
        #
        # if not friends:
        #     print "cant fetch friends data"
        # else:
        #     for friends_ids in friends:
        #         profile_temp = self.graph.get_object(friends_ids);
        #         print profile_temp['name'];
        # print "------------------------------------------------------------"
        return friends['data']

    def Post(self):
        print "------------------------------------------------------------"
        print "                       Recent Post                          "
        print "------------------------------------------------------------"
        self.post =self.graph.get_connections(self.object,'posts')
        print self.post

        print "------------------------------------------------------------"
        return self.post



    def Find(self, search):
        print "What are you searching for?"
        word = '/search/?q='+search+'&type=user&access_token='+self.token
        Result =  self.graph.request(word)
        if not Result:
            print "user not found"
        else:
            temp1 = Result['data'];
            user1 = [temp1['id'] for temp1 in temp1]
            for user in user1:
                self.getProfile(user)

            if 'next' in Result:
                Json = requests.get(Result['paging']['next'])

                print "------------------------------------------------------------"
                temp2 = Json.json()['data']
                user = [temp2['id'] for temp2 in temp2];

                for user in user:
                    self.getProfile(user)

        return Result['data']

    def taggedPost(self):
        print "------------------------------------------------------------"
        print "                       Tagged Post                          "
        print "------------------------------------------------------------"

        post = self.graph.get_connections(self.object, 'tagged')
        post_ids = [post['id'] for post in post['data']]

        print post
        if not post:
            print "Cant retrieve user tagged data"
        else:
            for post_ids in post_ids:
                post_temp = self.graph.get_object(post_ids);

        print "------------------------------------------------------------"

    def getProfile(self,id):
        profile = self.graph.get_object(id)
        return profile

    def setCache(self, bool):

        self.cache = bool
        print(self.cache , "is cache")

    def getCentre(self, location):
        lat , lng , count = 0, 0, 0
        for x,y in location:
            lat += x
            lng += y
            count+=1

        return x/count, y/count

@app.route("/")
def index():
    return "welcome"

# @app.route("/fb/search/<username>")
# def search(username):
#     x.post        = x.Post()
#     return render_template("search.html", result=[])

@app.route("/fb/search/<username>")
def search(username):
    result  = x.Find(username);
    print result
    return render_template("search.html", result=result)


@app.route("/fb/profile/<username>/relation/<id>")
def relation(username, id):
    cache_comment, cache_like = x.get_relation_post(id)
    return render_template("test.html", comment = cache_comment, like =cache_like)

@app.route("/fb/profile/<username>")
def profile(username):

    print "username adalah ", x.getUsername()

    if username == x.getUsername():
        print x.getUsername()
        print username
        x.setCache(True)
    else:
        print "new user not cach"
        x.setUsername(username)
        x.setCache(False)
        x.initialize()
        print "sekarang username adalah ", x.getUsername()

    profile     = x.getProfile(username)
    userID      = profile['id']
    x.object    = userID
    post        = x.Post()
    name        = profile['name']
    family      = x.Family()
    post = post['data']
    friends = x.Friends()

    return render_template("Facebook.html"
                           ,family=family
                           , friends=friends
                           , userID = userID
                           , name = name
                           , post=post)

@app.route('/test', methods = ["POST"])
@celery.task
def testAnaly():
    test = x.test()
    print(test)
    return jsonify({ 'Test': render_template('test.html', test = test)})

@app.route('/nextAnalysis', methods = ['POST'])
@celery.task
def getNextAnalysis():

    post = x.Post()
    if "paging" in post :
        reqData = requests.get(post['paging']['next'])
        postData = reqData.json()
        like , comment , location =x.get_post_like_comment_location(x.getGraph() , postData)
        print x.getCache()

        return jsonify({ 'LikesComments': render_template('TopFriends.html', likes=like, comments=comment)})

    return jsonify()


@app.route('/analysis', methods=['POST'])
@celery.task
def getAnalysis():

    like , comment , location =x.get_post_like_comment_location(x.getGraph() , x.Post())
    if location:
        lat, lng = x.getCentre(location)
        print(location)

        mymap = Map(
            identifier="view-side",
            lat=lng,
            lng=lat,
            markers=location
        )

    else:
        mymap = Map(
            identifier="view-side",
            lat=0,
            lng=0,
            markers=[0, 0]
        )

    # return jsonify({'map': render_template('Map.html',location = location) , 'LikesComments': render_template('TopFriends.html', likes=like, comments=comment)})
    return jsonify({ 'LikesComments': render_template('TopFriends.html', likes=like, comments=comment)})

if __name__ == "__main__":
    x = Facebook()
    x.Main()
    app.static_folder = 'static'
    app.run(debug=True)