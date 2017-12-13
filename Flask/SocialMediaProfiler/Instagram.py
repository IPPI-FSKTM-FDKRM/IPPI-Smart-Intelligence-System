import pytz, datetime, time
import TopicSentiment
from flask import Flask, render_template, url_for, redirect
from Sentiment_Analysis import nBayesTesting
from flask_googlemaps import GoogleMaps
from instagram.client import InstagramAPI
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

#------------------Database location-----------------
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/User/PycharmProjects/untitled1/database.db' #linux


class Instagram():
    profile = ""
    client_id = INSTACLIENT_ID
    api = InstagramAPI(access_token=INSTATOKEN, client_secret=INSTACLIENT_SECRET)

    app.config['GOOGLEMAPS_KEY'] = GOOGLEKEY
    GoogleMaps(app)

    #search profile
    def user_search(self,nama):
        profile = self.api.user_search(q = nama)

        return profile

    #display user's profile
    def user_media(self, userID):
        global topthelikes
        global ID_user
        ID_user = userID
        topthelikes = []

        recent_media , nextt = self.api.user_recent_media(user_id=userID, count=30)

        if not recent_media:
            print "Can't retrieve user media"
        else:
                for media in recent_media:
                    print "Id = " + media.id
                    print "Image = " + media.images['standard_resolution'].url
                    print "user"
                    if media.users_in_photo:
                        print media.users_in_photo
                        for use in media.users_in_photo:
                            print use.user.id
                            print use.user.full_name

                    # likes = self.api.media_likes(media_id=media.id)
                    # print "heheh"
                    # for likes in likes:
                    #     print likes.id
                    #     print likes.username
                    #     print likes.profile_picture

        return recent_media

    #display comment
    def comment_media(self, mediaID):
        recent_comment = self.api.media_comments(media_id=mediaID)
        if not recent_comment:
            print "Comments can't be found"
        else:
            for comment in recent_comment:
                print "Time : ", comment.created_at.astimezone(pytz.timezone('Asia/Kuala_Lumpur'))
                print comment

    #display user's profile
    def user_profile(self, userID):
        profile = self.api.user(user_id=userID)

        return profile

    #display location
    def location(self, userID):

        global locationInstaPost
        global monthloc
        locationInstaPost = []
        monthloc = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}

        recent_media, nextt = self.api.user_recent_media(user_id=userID, count=30)

        if not recent_media:
            print "Can't retrieve user media"
        else:
            for media in recent_media:
                try:
                    if media.location.name not in locationInstaPost:
                        print media.location
                        Malaysia = pytz.timezone('Asia/Kuala_Lumpur')
                        time = str(media.created_time.astimezone(Malaysia))

                        test = datetime.datetime.strptime(time[0:19], "%Y-%m-%d %H:%M:%S")
                        locationInstaPost.insert(0,[media.location.name, media.location.point.latitude, media.location.point.longitude, media.images['low_resolution'].url ])

                        Malaysia = pytz.timezone('Asia/Kuala_Lumpur')
                        time = str(media.created_time.astimezone(Malaysia))
                        test = datetime.datetime.strptime(time[0:19], "%Y-%m-%d %H:%M:%S")

                        monthaddress = str(test) + " " + media.location.name
                        print monthaddress

                        if test.month not in monthloc:
                             monthloc[test.month] = [monthaddress]
                        else:
                             monthloc[test.month].append(monthaddress)
                except Exception as e:
                    print e
        print locationInstaPost
        print "+++++++"
        print monthloc

    #get time post
    def get_created_post(self, userID):

        global Instatopic, Instaposnegneu
        global day, hour, month

        day = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        hour = {}
        month = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
        Instatopic = {}
        Instaposnegneu = {"positive": [], "negative": [], "neutral": []}

        recent_media, nextt = self.api.user_recent_media(user_id=userID, count=20)

        if not recent_media:
            print "Can't retrieve user media"
        else:
            for media in recent_media:

                if media.caption:
                    print media.caption.text
                    # postTopic = TopicSentiment.getArrayFromString()
                    #
                    # if postTopic:
                    #     if media.caption.text not in Instatopic[postTopic]:
                    #         Instatopic[postTopic].append(media.caption.text)

                    postTopic = TopicSentiment.getArrayFromString(media.caption.text)

                    if postTopic not in Instatopic:
                        Instatopic[postTopic] = [media.caption.text]
                    else:
                        if media.caption.text not in Instatopic[postTopic]:
                            Instatopic[postTopic].append(media.caption.text)

                    Instaposnegneu[nBayesTesting.getListValueString(media.caption.text)].append(media.caption.text)



                # print media.created_time
                Malaysia = pytz.timezone('Asia/Kuala_Lumpur')
                time = str(media.created_time.astimezone(Malaysia))

                print time
                test = datetime.datetime.strptime(time[0:19], "%Y-%m-%d %H:%M:%S")

                if media.caption:
                    if test.hour not in hour:
                        hour[test.hour] = [media.caption.text]
                    else:
                        hour[test.hour].append(media.caption.text)

                    if test.month not in month:
                        month[test.month] = [media.caption.text]
                    else:
                        month[test.month].append(media.caption.text)

                    if test.weekday() not in day:
                        day[test.weekday()] = [media.caption.text]
                    else:
                        day[test.weekday()].append(media.caption.text)

        print Instaposnegneu
        print "-----------------------------"
        print Instatopic
        print hour
        print day
        print month

    def getLocationInstaPost(self):
        return locationInstaPost

    def getTopic(self):
        return Instatopic

    def getPostNegNeu(self):
        return Instaposnegneu

    def getInstaHour(self):
        return hour

    def getInstaMonth(self):
        return month

    def getInstaDay(self):
        return day

    def getMonthLoc(self):
        return monthloc

    def getID_User(self):
        return ID_user

