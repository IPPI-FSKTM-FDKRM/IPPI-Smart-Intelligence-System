import os
import json
import facebook
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from celery import Celery

from datetime import datetime
from flask import Flask , render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


app = Flask(__name__)
broker_url = 'amqp://guest@localhost'
celery = Celery(app.name, broker=broker_url)


class Facebook():

    app.config['GOOGLEMAPS_KEY'] = "AIzaSyCQaXdeh30YGYlYPK6eqt9AcAJC4or5I8w"
    GoogleMaps(app)

    #original app token
    # token = 'EAAFyPKV2cOIBAM1GJtjCW7oIftQzwo8RxujFy9ZBLeYNPrSNpMiuUbMAcpzvEkH6sJ0F2ZAf5ey0yle7toaSLJ2wd3yqZACnXJjKXotl8YHZA8KCLNWPBMHlV2ZAcdD4M4p8Y7RqiXV43sF5rfZCa7pmwOaZBWB6qsZD';

    token = 'EAAFyPKV2cOIBANz6EDcSV0CJAoKPt1YCeYGaWF5Tl6FLEmbELopL4XLUp5GZCS2OmwI1zNaa60D5MngsUGW4SZByLZB7w86wyZAZCR50ZAuGZC3dXZAZCLLZCAn5BDzj2UxkP1nlhZCvSmx9LAeZA3fHETSmAJIFZBZCSmooUZD'
    # token = 'EAACEdEose0cBANkF7dXkK76lntZCWBgmS646s0QWcJBzoZAI7iai8xsEOPGU3EmZCOeUMknsuotMNozA429e6JOmOrsmIa7In1lPZBlRliDIPeRCYWH5uu4ZAAXWA1ZA6ZAYrtjY3hLzf7nDyeC6rHbj7p4DJ9hhDqprjrDtZBteEw0i8135ca7Ii8120wKw2skZD'
    graph = facebook.GraphAPI(token);
    object = 'me';

    @app.template_filter()
    def format_date(date):  # date = datetime object.
        date = datetime.strptime(date[0:16], '%Y-%m-%dT%H:%M')
        return date.strftime('%Y-%m-%d  %H:%M:%S')

    @app.template_filter()
    def get_picture(self, post_id):  # date = datetime object.
        picture_url = self.graph.get_object(id=post_id, fields="picture")
        print picture_url
        return picture_url

    def ExtendToken(self):
        app_id = '407079776317666'  # Obtained from https://developers.facebook.com/
        app_secret = 'f12509095067e4fde26fae23fdc0721f'  # Obtained from https://developers.facebook.com/
        # Extend the expiration time of a valid OAuth access token.
        extended_token = self.graph.extend_access_token(app_id, app_secret)



    def Main(self):
        profile = self.graph.get_object(self.object);
        print profile;
        #self.Find()
        # self.Friends()
        # self.Family()
        # self.taggedPost()
        # self.Post()

    def Family(self):
        print "------------------------------------------------------------"
        print "                       Family                               "
        print "------------------------------------------------------------"
        family = self.graph.get_connections(self.object, 'family');
        # family = [family['id'] for family in family['data']];

        # for family_ids in family:
        #     profile_temp = self.graph.get_object(family_ids);
        #     print profiltemp['name'];

        print "------------------------------------------------------------"
        return family['data']

    def Friends(self):

        print "------------------------------------------------------------"
        print "                       Friends                              "
        print "------------------------------------------------------------"

        friends = self.graph.get_connections(self.object,'friends');
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
        print "                       Recent Post                              "
        print "------------------------------------------------------------"

        post =self.graph.get_connections(self.object,'posts')
        print(post)
        print "----------------------------------------------------------"
        return post

    def get_post_like_comment_location(self, post):
        location = {}

        amount_likes = {}
        amount_comment = {}


        for post in post['data']:
            # likes = self.graph.get_object(id=post['id'], fields='likes')
            # comment = self.graph.get_object(id=post['id'], fields='comments')
            place = self.graph.get_object(id=post['id'], fields='place')


            if 'place' in place :
                location['name'] = place['place']['name']

                location['longitude']= place['place']['location']['longitude']
                location['latitude']= place['place']['location']['latitude']

        print(location)



            # print comment
            #
            # if 'likes' in likes :
            #     for likes in likes['likes']['data']:
            #         # print likes
            #
            #         if not likes['id'] in amount_likes:
            #             amount_likes[likes['id']] = 1;
            #         else:
            #             amount_likes[likes['id']] += 1;
            #
            # if 'comments' in comment:
            #
            #     for comments in comment['comments']['data']:
            #
            #         print comments['from']['id']
            #         print comments['message']
            #         if not comments['from']['id'] in amount_comment:
            #             amount_comment[comments['from']['id']] = 1;
            #         else:
            #             amount_comment[comments['from']['id']] += 1;

        if(amount_likes):
            amount_likes['top'] = max(amount_likes, key=amount_likes.get)

        if (amount_comment):
            amount_comment['top'] = max(amount_comment, key=amount_comment.get)

        return amount_likes, amount_comment, location

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
                # print post_temp['created_time']
                #
                # if 'message' in post_temp:
                #     print post_temp['message']
                # else:
                #     print post_temp['story']

        print "------------------------------------------------------------"

    def getProfile(self,id):
        profile = self.graph.get_object(id)
        return profile


@app.route("/")
def index():
    return "welcome"

@app.route("/search/<username>")
def search(username):
    result  = x.Find(username);
    print result
    return render_template("search.html", result=result)

@app.route("/tuna/<username>")
def tuna(username):
    x = Facebook();
    return x.getProfile(username)

@app.route("/profile/<username>")
def profile(username):


    profile = x.getProfile(username)
    userID = profile['id']
    x.object = userID
    post = x.Post()
    name = profile['name']
    # family = x.Family()
    likes , comments ,location= x.get_post_like_comment_location(post)
    post = post['data']
    friends = x.Friends()
    print location
    mymap = Map(
        identifier="view-side",
        lat=location['latitude'],
        lng=location['longitude'],
        markers=[(location['latitude'],location['longitude'])]
    )



    return render_template("profile.html", mymap=mymap,likes=likes, comments=comments, friends=friends, userID = userID, name = name, post=post)

if __name__ == "__main__":
    x = Facebook()
    x.Main()
    print x.Post()
    app.run(debug=True)