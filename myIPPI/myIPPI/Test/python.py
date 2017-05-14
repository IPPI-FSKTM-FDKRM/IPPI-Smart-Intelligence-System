import os
import json
import facebook
import requests
from flask import Flask , render_template

app = Flask(__name__)

class Facebook():
    #original token
    #token = 'EAAFyPKV2cOIBAM1GJtjCW7oIftQzwo8RxujFy9ZBLeYNPrSNpMiuUbMAcpzvEkH6sJ0F2ZAf5ey0yle7toaSLJ2wd3yqZACnXJjKXotl8YHZA8KCLNWPBMHlV2ZAcdD4M4p8Y7RqiXV43sF5rfZCa7pmwOaZBWB6qsZD';


    token = 'EAACEdEose0cBAEwZAeumdWm2ZBzSlvfylP7hX1BgeKpiUVrZBIo8SsKaZATVmyZAVpjhDGD90AZCM1x8Lzw3jjtsFs7CnNdZAZBhVES4JnhLTw3hjvLNuZARH58tWZBzPtXEqpaWvr0nnNNf0xI6WZBeWindxtjAfSHrQxy4fUgJDIZAqOuwfs6a3TZAPfqrRjqNBJucZD'
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
        family = [family['id'] for family in family['data']];

        # for family_ids in family:
        #     profile_temp = self.graph.get_object(family_ids);
        #     print profile_temp['name'];

        print "------------------------------------------------------------"
        return family

    def Friends(self):

        print "------------------------------------------------------------"
        print "                       Friends                              "
        print "------------------------------------------------------------"

        friends = self.graph.get_connections(self.object,'friends');
        friends = [friends['id'] for friends in friends['data']];

        if not friends:
            print "cant fetch friends data"
        else:
            for friends_ids in friends:
                profile_temp = self.graph.get_object(friends_ids);
                print profile_temp['name'];
        print "------------------------------------------------------------"
        return friends

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

        print "------------------------------------------------------------"
        return post

    def Find(self):
        print "What are you searching for?"
        search =  raw_input()
        word = '/search/?q='+search+'&type=user&access_token='+self.token
        Result =  self.graph.request(word)
        if not search:
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


@app.route("/tuna/<username>")
def tuna(username):
    x = Facebook();
    return x.getProfile(username)

@app.route("/profile/<username>")
def profile(username):
    profile = x.getProfile(username)
    userID = profile['id']
    x.object = userID
    post = x.Post()['data']
    name = profile['name']
    family = x.Family()
    friends = x.Friends()
    return render_template("profile.html",friends=friends,family=family, userID = userID ,name = name, post=post)

if __name__ == "__main__":
    x = Facebook()
    x.Main()
    print x.Post()
    app.run(debug=True)