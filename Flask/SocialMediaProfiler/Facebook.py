import facebook
import pytz
import requests
import tzlocal
import TopicSentiment
import json


from collections import Counter
from datetime import datetime
from celery import Celery
from flask import Flask
from flask_googlemaps import GoogleMaps
from Sentiment_Analysis import nBayesTesting
import os


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

class Facebook():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    app.config['GOOGLEMAPS_KEY'] = "AIzaSyCQaXdeh30YGYlYPK6eqt9AcAJC4or5I8w"
    GoogleMaps(app)
    global cache_comments
    global cache_likes
    global user_id
    global location
    global amount_comment
    global amount_likes
    global hour, day, month
    global topic
    global locationPost
    global cache
    global locationRelation
    global address
    global posnegneu

    posnegneu = {}
    address = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[]}
    day = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}
    hour = {}
    month = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[]}
    topic= {}
    locationPost = []
    locationRelation = {}
    current_username = ""

    cache = False
    amount_likes = {}
    amount_comment = {}
    cache_likes = {}
    cache_comments = {}
    location = []
    post = []
    tagpost = []
    # original app token
    # token = 'EAAFyPKV2cOIBAM1GJtjCW7oIftQzwo8RxujFy9ZBLeYNPrSNpMiuUbMAcpzvEkH6sJ0F2ZAf5ey0yle7toaSLJ2wd3yqZACnXJjKXotl8YHZA8KCLNWPBMHlV2ZAcdD4M4p8Y7RqiXV43sF5rfZCa7pmwOaZBWB6qsZD';
    token = 'EAAFyPKV2cOIBADfar33ktp4UZCPKSZBv6waYUad5GQPimSIc31nrkgjuLDwFIEjU6YgZCdGFHOHq5ZA8cLsDPF0DwJnwS4xJBvhLUvZCxCn8ztRKrMtJNpcQ01PS6AFCaykVPZBhFQoNXKsbilqjdPd1lpw0o1DNj6nMzL9NjhcAZDZD'
    # token = 'EAACEdEose0cBAAUIMQRAwIEWQ5x9CoiiVdnDDYfzQJKI4ZAvrZBUuAg63vFkN94dwe6gikAMmrRCNdVC9ZCZBelfaHcljC2zoSD6i9NPztrX0crfEVsOM2SUJYiTG42twmJJjK3KihpxLmJaaNm9pLLe7sDP2VRoADghhZBEt0NtDhA8opJX7M3oKSGRXmfQZD'
    graph = facebook.GraphAPI(token);

    def loadCache(self, fileName):

        filePathNameWExt = self.dir_path + "/Cache/" + fileName + '.json'

        if os.path.isfile(filePathNameWExt):
            with open(filePathNameWExt) as fp:
                global cache_comments
                global cache_likes
                global location
                global amount_comment
                global amount_likes
                global hour, day, month
                global topic, posnegneu
                global locationPost
                global cache
                global locationRelation
                global address

                d = json.load(fp)
                day = d["day"]
                hour = d["hour"]
                month = d["month"]
                topic = d["topic"]
                posnegneu = d["posnegneu"]
                locationPost = d["locationPost"]
                locationRelation = d["locationRelation"]
                cache_likes = d["cache_likes"]
                cache_comments = d["cache_comments"]
                amount_comment = d["amount_comment"]
                amount_likes = d["amount_likes"]
                address = d["address"]
                cache = True

            return True
        else :
            return False


    def initialize(self):
        print("initializing")
        global cache_comments
        global cache_likes
        global location
        global amount_comment
        global amount_likes
        global hour, day, month
        global topic , posnegneu
        global locationPost
        global cache
        global locationRelation
        locationRelation = {}
        address = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
        day = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        hour = {}
        month = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
        topic = {}
        posnegneu = {}
        locationPost = []
        self.cache = False
        amount_likes = {}
        amount_comment = {}
        cache_likes = {}
        cache_comments = {}
        location = []
        self.post = [];
        locationPost = []
        self.current_username = ""

    def ExtendToken(self):
        app_id = '407079776317666'  # Obtained from https://developers.facebook.com/
        app_secret = 'f12509095067e4fde26fae23fdc0721f'  # Obtained from https://developers.facebook.com/
        # Extend the expiration time of a valid OAuth access token.
        extended_token = self.graph.extend_access_token(app_id, app_secret)

    def getUsername(self):
        return self.current_username

    def setCache(self, bool):
        self.cache = bool
        print(self.cache, "is cache")

    def setUsername(self, username):
        self.current_username = username

    def getCacheCommentsAndLikes(self):
        return cache_comments, cache_likes

    def getAmountLikesAndComments(self):
        return amount_likes , amount_comment


    def get_picture(self, post_id):
        picture_url = self.graph.get_object(id=post_id, fields="picture")
        return picture_url

    def getGraph(self):
        return self.graph

    def isCache(self):
        return self.cache

    def isSameUser(self):
        return self.sameUser

    @celery.task(bind=True)
    def get_post_like_comment_location(self, cacheNow, graph, post):
        if not cacheNow:
            cache_com = {}
            cache_like = {}
            cache_com, cache_like = cache_comments, cache_likes
            local_timezone = tzlocal.get_localzone()  # get pytz tzinfo
            print post
            for post in post['data'] :

                utc = datetime.strptime(post['created_time'][0:16], '%Y-%m-%dT%H:%M')
                date = utc.replace(tzinfo=pytz.utc).astimezone(local_timezone)


                if date.hour not in hour:
                    hour[date.hour] = [post]
                else:
                    hour[date.hour].append(post)

                if date.month not in month:
                    month[date.month] = [post]
                else:
                    month[date.month].append(post)

                if date.weekday() not in day:
                    day[date.weekday()] = [post]
                else:
                    day[date.weekday()].append(post)

                likes = graph.get_object(id=post['id'], fields='likes')
                comment = graph.get_object(id=post['id'], fields='comments')
                place = graph.get_object(id=post['id'], fields='place')
                tag = graph.get_object(id=post['id'], fields='message_tags')

                if 'message' in post:
                    print post['message']
                    postTopic = TopicSentiment.getArrayFromString(post['message'])

                    print topic

                    if postTopic not in topic:
                        topic[postTopic] = [post]
                    else:
                        if post not in topic[postTopic]:
                            topic[postTopic].append(post)

                    for i in nBayesTesting.getListValue([post['message']]):
                        if i not in posnegneu:
                            posnegneu[i] = [post]
                        else:
                            posnegneu[i].append(post)

                if 'place' in place:
                    tagUser = []
                    street = ""
                    city = ""
                    country = ""
                    if "street" in place['place']['location']:
                        street = place['place']['location']['street']+" , "

                    if "city" in place['place']['location']:
                        city   = place['place']['location']['city']+" , "

                    if "country" in place['place']['location']:
                        country = place['place']['location']['country'] + " , "

                    print str(utc)

                    locationAddress = str(date)+" : "+place['place']['name']+" , "+street+city+country

                    print locationAddress
                    if date.month not in address:
                        address[date.month] = [locationAddress]
                    else:
                        address[date.month].append(locationAddress)

                    if 'message_tags' in tag:
                        for i in tag['message_tags']:
                            tagUser.append(i['id'])
                            if i['id'] not in locationRelation:
                                locationRelation[i['id']] = [{"address":locationAddress ,"lat": place['place']['location']['latitude'], "lng": place['place']['location']['longitude'], "post": post }]
                            else:
                                locationRelation[i['id']].append({"address": locationAddress ,"lat": place['place']['location']['latitude'], "lng": place['place']['location']['longitude'] , "post":post})

                    if 'message' in post:
                        locationPost.insert(0, [post['id'], post['message'], place['place']['location']['latitude'],
                                                place['place']['location']['longitude'], tagUser])

                if 'likes' in likes:
                    for likes in likes['likes']['data']:

                        if not likes['id'] in amount_likes:
                            amount_likes[likes['id']] = 1;
                            cache_like[likes['id']] = [post]
                        else:
                            amount_likes[likes['id']] += 1;
                            cache_like[likes['id']].append(post)

                if 'comments' in comment:
                    for comments in comment['comments']['data']:

                        if not comments['from']['id'] in amount_comment:
                            cache_com[comments['from']['id']] = [comments]
                            amount_comment[comments['from']['id']] = 1;
                        else:
                            cache_com[comments['from']['id']].append(comments)
                            amount_comment[comments['from']['id']] += 1;

        # get top commentator and likers
        if (amount_likes):
            if 'top' in amount_likes:
                amount_likes.pop('top', None)
            amount_likes['top'] = dict(Counter(amount_likes).most_common(5))

        if (amount_comment):
            if 'top' in amount_comment:
                amount_comment.pop('top', None)
            amount_comment['top'] = dict(Counter(amount_comment).most_common(5))

        if amount_likes and amount_comment:
            return amount_likes['top'], amount_comment['top'], location

        else:
            return [], [], None

    def getLocationAddress(self):
        return address

    def getTimePost(self):
        return hour, month, day

    def getTopic(self):
        return topic

    def getPostNegNeu(self):
        return posnegneu

    def get_relation_post(self, id):
        cache_com, cache_loc = self.getCacheCommentsAndLikes()
        if id in cache_com:
            cache_com = cache_com[id]
        else:
            cache_com = []

        if id in cache_loc:
            cache_loc = cache_loc[id]
        else:
            cache_loc = []
        return cache_com, cache_loc

    def getProfile(self, id):
        profile = self.graph.get_object(id)
        return profile

    def getAbout(self,id):
        return

    def getProfileInstance(self, id):
        return self.graph.get_object(id)

    def getLocationPost(self):
        return locationPost

    def getLocationRelatioin(self):
        return locationRelation


    #######################################################
    # Basic facebook profile data                         #
    #######################################################

    def Family(self):
        family = self.graph.get_connections(self.object, 'family')
        return family['data']

    def getRelationShipStatus(self):
        relationship = self.graph.get_object(self.object, fields='relationship_status')
        # print self.graph.get_object(self.object, fields='email')
        # print self.graph.get_object(self.object, fields='education')
        # print self.graph.get_object(self.object, fields='work')


        return relationship


    def Friends(self):
        friends = self.graph.get_connections(self.object, 'friends');
        print friends
        return friends['data']

    def Post(self):
        self.post = self.graph.get_connections(self.object, 'posts', fields="created_time,full_picture, story,message",limit=50)

        return self.post

    def getPost(self):
        return self.post

    def getPageDetails(self,id):
        pagedetails=  self.graph.get_object(self.object, fields="about,category,birthday,fan_count")
        print pagedetails
        return pagedetails

    def taggedPost(self):
        self.tagpost = self.graph.get_connections(self.object, 'tagged')
        return self.tagpost

    def FindUser(self, search):
        word = '/search/?q=' + search + '&type=user&access_token=' + self.token
        Result = self.graph.request(word)

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

    def FindPage(self, search):
        word = '/search/?q=' + search + '&type=page&access_token=' + self.token
        Result = self.graph.request(word)

        temp1 = Result['data'];
        user1 = [temp1['id'] for temp1 in temp1]
        for user in user1:
            self.getProfile(user)
            print self.getProfile(user)

        if 'next' in Result:
            Json = requests.get(Result['paging']['next'])

            print "------------------------------------------------------------"
            temp2 = Json.json()['data']
            user = [temp2['id'] for temp2 in temp2];

            for user in user:
                self.getProfile(user)

        return Result






