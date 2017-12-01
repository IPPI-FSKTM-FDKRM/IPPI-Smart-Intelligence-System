from datetime import datetime
from collections import Counter
import TopicSentiment
import json
import facebook
import requests
from celery import Celery
from flask import Flask, render_template, jsonify, url_for, request, Blueprint
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import pytz    # $ pip install pytz
import tzlocal # $ pip install tzlocal


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
    global hour , day , month
    global topic
    global locationPost
    global cache

    day = {}
    hour = {}
    month = {}
    topic = {}
    locationPost = []
    current_username = ""

    cache = False
    amount_likes = {}
    amount_comment = {}
    cache_likes = {}
    cache_comments = {}
    location = []

    #original app token
    # token = 'EAAFyPKV2cOIBAM1GJtjCW7oIftQzwo8RxujFy9ZBLeYNPrSNpMiuUbMAcpzvEkH6sJ0F2ZAf5ey0yle7toaSLJ2wd3yqZACnXJjKXotl8YHZA8KCLNWPBMHlV2ZAcdD4M4p8Y7RqiXV43sF5rfZCa7pmwOaZBWB6qsZD';

    token = 'EAAFyPKV2cOIBAGNxJZBXQxdIMZB3sZBAafeXMTS5mRyXwyuBsnZCL14P4o3EdzHZAcMbVUtOF7pfBmdYczTqcmFfNLWOpUqZCXT35aPVMueySyOd6qBhjvCtARx5UyCSb2bM3fwO1ne1OnlMtkxnUTcesZCHIyYdREZD'
    # token = 'EAACEdEose0cBANRykZCQNIoZAj7zFS5qVyGFNEYSexsjTfiHAwNyRnQF33ZBtXddkKt85AW7jNHcvgyUyvZCl4afOBnfJaLzvC7dezvOJxKBNxcE2wnii9WV27vs1jWTqfJYzNU9HIeIdDeHKZAfnP9CscJ7WL1Bx5xvBwiHPy1wOCVmpKdqLc1ElaZCXuz14ZD'
    graph = facebook.GraphAPI(token);
    print graph
    object = 'me';
    post = [];

    def initialize(self):
        print("initializing")
        global cache_comments
        global cache_likes
        global user_id
        global location
        global amount_comment
        global amount_likes
        global locationPost
        global day , hour ,month

        locationPost = []
        current_username=""
        day = {}
        hour = {}
        month = {}
        amount_likes = {}
        amount_comment = {}
        cache_likes = {}
        cache_comments = {}
        cache = False
        location = []
        self.post = [];

    def getUserID(self):
        return user_id

    def getUsername(self):
        return self.current_username

    def setUsername(self, username):
        self.current_username = username

    def getCache(self):
        return cache_comments , cache_likes

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
    def get_post_like_comment_location(self, cacheNow, graph , post):
        print amount_likes
        print amount_comment
        print "adakah cache?",cache
        if not cacheNow:
            print post['data']
            cache_com = {}
            cache_like = {}
            cache_com , cache_like = cache_comments , cache_likes
            local_timezone = tzlocal.get_localzone()  # get pytz tzinfo

            print cache_com, cache_like
            for post in post['data']:
                utc = datetime.strptime(post['created_time'][0:16], '%Y-%m-%dT%H:%M')
                date = utc.replace(tzinfo=pytz.utc).astimezone(local_timezone)

                if date.hour not in hour:
                    hour[date.hour] = [post]
                else:
                    # print date.hour , "sudah ada"
                    hour[date.hour].append(post)
                if date.month not in month:
                    month[date.month] = [post]
                else:
                    month[date.month].append(post)

                if date.weekday() not in day:
                    day[date.weekday()]=[post]
                else:
                    day[date.weekday()].append(post)

                # print hour, month ,day

                likes = graph.get_object(id=post['id'], fields='likes')
                comment = graph.get_object(id=post['id'], fields='comments')
                place = graph.get_object(id=post['id'], fields='place')
                tag = graph.get_object(id=post['id'], fields='message_tags')
                #
                # if 'message' in post:
                #     print TopicSentiment.getArray([post['message']])

                if 'place' in place:
                    tagUser = []
                    if 'message_tags' in tag:
                        for i in tag['message_tags']:
                            tagUser.append(i['id'])
                    if 'message' in post:
                        locationPost.insert(0,[post['id'],post['message'], place['place']['location']['latitude'],place['place']['location']['longitude'], tagUser])



                # location.insert(0 , ( place['place']['location']['latitude'],place['place']['location']['longitude']))


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

                        if not comments['from']['id'] in amount_comment:
                            cache_com[comments['from']['id']] = [comments]
                            amount_comment[comments['from']['id']] = 1;
                        else:
                            cache_com[comments['from']['id']].append(comments)
                            amount_comment[comments['from']['id']] += 1;

        #get top commentator and likers
        if (amount_likes):
            if 'top' in amount_likes:
                amount_likes.pop('top', None)
            amount_likes['top'] = dict(Counter(amount_likes).most_common(5))

        if (amount_comment):
            if 'top' in amount_comment:
               amount_comment.pop('top', None)
            amount_comment['top'] = dict(Counter(amount_comment).most_common(5))

        if amount_likes and amount_comment :
            return amount_likes['top'] , amount_comment['top'], location

        else:
            return [], [] , None

    def getTimePost(self):
        return hour, month , day

    def get_relation_post(self, id):
        cache_com , cache_loc = self.getCache()
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

    def Main(self):
        print "starting Facebook Module"
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
        print "dyens"
        word = '/search/?q='+search+'&type=user&access_token='+self.token
        print word
        Result =  self.graph.request(word)
        print Result
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

        return Result

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

    def getLocationPost(self):
        return locationPost

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

