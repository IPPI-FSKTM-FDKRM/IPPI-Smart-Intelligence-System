import os
import json
import facebook
import requests
from flask import Flask , render_template

app = Flask(__name__)

class Facebook():
    #original token
    token = 'EAAFyPKV2cOIBAM1GJtjCW7oIftQzwo8RxujFy9ZBLeYNPrSNpMiuUbMAcpzvEkH6sJ0F2ZAf5ey0yle7toaSLJ2wd3yqZACnXJjKXotl8YHZA8KCLNWPBMHlV2ZAcdD4M4p8Y7RqiXV43sF5rfZCa7pmwOaZBWB6qsZD';


    token = 'EAACEdEose0cBAP6q51GCFqQwyAedwZAz0FF0ZC1IgPGNyiMcIk2mZB3nUtBH2UMnBNkIAQ0lvwgwPCm3NelZC58KP0W9GxB8uImgl4BNdc9EWBri8vRO9kjcUiedYCgQHhmuDGfCskwtbycBQ4XUhGZC2WRPZCUNG5Pk7Mnhz325b4VZA1wCFQBuWyQ9rdDs0sZD'
    graph = facebook.GraphAPI(token);
    object = 'me';

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
        #     print profile_temp['name'];

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
        # post_ids = [post['id'] for post in post['data']]
        # if 'paging' in post:
        #     Json = requests.get(post['paging']['next']);
        #     print Json.json()['data']
        #
        # if not post:
        #     print "Cant retrieve user post data"
        # else:
        #     for post_ids in post_ids:
        #         post_temp = self.graph.get_object(post_ids);
        #         print post_temp['created_time']
        #
        #         if 'message' in post_temp:
        #             print post_temp['message']
        #         else:
        #             print post_temp['story']

        print "----------------------------------------------------------"
        return post

    def getLikesComments(self, post):

        amount_likes = {}

        for post in post['data']:
            

            if 'likes' in post:

                likes = post['likes']['data']
                for likes in likes:

                    if not likes['id'] in amount_likes:
                        amount_likes[likes['id']] = 1;
                    else:
                        amount_likes[likes['id']] += 1;
        if(amount_likes):
            amount_likes['top'] = max(amount_likes, key=amount_likes.get)

        print "Top Likers : "

        return amount_likes

    def getComments(self,post):

        amount_comment = {}
        print post
        for post in post['data']:
            if 'comments' in post:
                comments = post['comments']['data']
                for comments in comments:
                    print comments['from']['id']
                    print comments['message']
                    if not comments['from']['id'] in amount_comment:
                        amount_comment[comments['from']['id']] = 1;
                    else:
                        amount_comment[comments['from']['id']] += 1;

        if(amount_comment):
            amount_comment['top'] = max(amount_comment, key=amount_comment.get)

        print "Top Commentator : "

        return amount_comment


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
    family = x.Family()
    likes  = x.getComments(post)
    comments = x.getLikesComments(post)
    post = post['data']
    print likes
    print comments
    print family
    friends = x.Friends()
    return render_template("profile.html",likes=likes , comments=comments, friends=friends,family=family, userID = userID ,name = name, post=post)

if __name__ == "__main__":
    x = Facebook()
    x.Main()
    print x.Post()
    app.run(debug=True)