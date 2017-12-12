from collections import Counter
from datetime import datetime
import facebook
import Visualization
from Sentiment_Analysis import nBayesTesting
from datetime import datetime
import TopicSentiment
import pytz    # $ pip install pytz
import tzlocal # $ pip install tzlocal
import json
import io, os


class tahi():
    address = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}
    day = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    hour = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [],
            15: [], 16: [], 17: [], 18: [], 19: [], 20: [], 21: [], 22: [], 23: [], 24: []}
    month = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}

    dir_path = os.path.dirname(os.path.realpath(__file__))

    token = 'EAACEdEose0cBAGoZCEXjxX0w52E4LGMKxLcfiZCEL50Bx2ZAIcBB5f1dMzgVEzZANda4Nmu5BnNKXvunMspExlq0fjNXxcUeEdMuFRG9aBtMo5BWvh0WScpHxWQVUbqrEW1qASDa2y2CeZBcjbPeOvh0KQXKUZAYsK9l5GAq7yZCXeddE5AZAfRgKCjqWFCwIAAZD'
    graph =  facebook.GraphAPI(access_token=token,version="2.10")


    tag = {u'id': u'1362815530452737_1551861968214758', u'message_tags': [
        {u'length': 16, u'offset': 0, u'type': u'user', u'id': u'1661021870583831', u'name': u'Irfan Kamaruddin'},
        {u'length': 13, u'offset': 17, u'type': u'user', u'id': u'10214804744656245', u'name': u'Raam Kanaisan'},
        {u'length': 11, u'offset': 31, u'type': u'user', u'id': u'1898030863542173', u'name': u'Hafiz Redha'},
        {u'length': 12, u'offset': 43, u'type': u'user', u'id': u'1587005678025949', u'name': u'Aida Baharun'}]}



    topic= {'spending': [{u'created_time': u'2017-11-24T15:47:36+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Kolej Kediaman Kelapan,Universiti Malaya.', u'id': u'1362815530452737_1554897484577873'}], 'travel': [], 'sports': [{u'created_time': u'2017-11-29T06:43:04+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Crystal Crown Hotel Petaling Jaya.', u'id': u'1362815530452737_1559629380771350'}, {u'created_time': u'2017-11-19T05:25:25+0000', u'message': u'Datang la support boling padang ulk pada 25/26 november', u'story': u'Khairul Albertado Danial is at Kompleks Sukan Negara Bukit Kiara.', u'id': u'1362815530452737_1549934008407554'}], 'politic': [{u'created_time': u'2017-11-29T06:43:04+0000', u'message': u'Last day at um academia community conference 2017', u'story': u'Khairul Albertado Danial is at Crystal Crown Hotel Petaling Jaya.', u'id': u'1362815530452737_1559629380771350'}, {u'created_time': u'2017-11-24T15:47:36+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Kolej Kediaman Kelapan,Universiti Malaya.', u'id': u'1362815530452737_1554897484577873'}, {u'created_time': u'2017-11-24T09:41:04+0000', u'message': u'Alhamdulillah , lots more to improve.. 1 more week towards integration. My team will do well... :Putnam:', u'story': u'Khairul Albertado Danial is at Kerinchi LRT station.', u'id': u'1362815530452737_1554649987935956'}, {u'created_time': u'2017-11-21T07:59:28+0000', u'message': u'Irfan Kamaruddin Raam Kanaisan Hafiz Redha Aida Baharun, actually this is how alzheimer brain looks like , it is good to know about all this topic', u'story': u"Khairul Albertado Danial shared Dr John's video.", u'id': u'1362815530452737_1551861968214758'}, {u'created_time': u'2017-10-16T12:44:58+0000', u'message': u'Hazim Kamaruzzaman Yeah manager', u'story': u"Khairul Albertado Danial shared Jawatankuasa Pelajar Luar Kampus Universiti Malaya's post.", u'id': u'1362815530452737_1519290884805200'}], 'education': [{u'created_time': u'2017-11-08T11:27:17+0000', u'message': u'Main lawn bowl bersama Raam Kanaisan Irfan Kamaruddin dan Hazim Kamaruzzaman\n\n#FYPpurpose', u'story': u'Khairul Albertado Danial is with Raam Kanaisan and 2 others at Malaysian Lawn Bowls Federation.', u'id': u'1362815530452737_1539814052752883'}], 'technology': [{u'created_time': u'2017-11-29T06:43:04+0000', u'message': u'Last day at um academia community conference 2017', u'story': u'Khairul Albertado Danial is at Crystal Crown Hotel Petaling Jaya.', u'id': u'1362815530452737_1559629380771350'}, {u'created_time': u'2017-11-24T15:47:36+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Kolej Kediaman Kelapan,Universiti Malaya.', u'id': u'1362815530452737_1554897484577873'}, {u'created_time': u'2017-11-21T07:59:28+0000', u'message': u'Irfan Kamaruddin Raam Kanaisan Hafiz Redha Aida Baharun, actually this is how alzheimer brain looks like , it is good to know about all this topic', u'story': u"Khairul Albertado Danial shared Dr John's video.", u'id': u'1362815530452737_1551861968214758'}, {u'created_time': u'2017-11-19T05:25:25+0000', u'message': u'Datang la support boling padang ulk pada 25/26 november', u'story': u'Khairul Albertado Danial is at Kompleks Sukan Negara Bukit Kiara.', u'id': u'1362815530452737_1549934008407554'}, {u'created_time': u'2017-11-08T11:27:17+0000', u'message': u'Main lawn bowl bersama Raam Kanaisan Irfan Kamaruddin dan Hazim Kamaruzzaman\n\n#FYPpurpose', u'story': u'Khairul Albertado Danial is with Raam Kanaisan and 2 others at Malaysian Lawn Bowls Federation.', u'id': u'1362815530452737_1539814052752883'}]}

    Hour = {}
    Day = {}

    def picture(self):
        post = self.graph.get_connections('me', 'posts', fields="created_time,full_picture, story,message",limit=50)
        print post['data']

    def writeToJSONFile(self, fileName, data):
        filePathNameWExt = self.dir_path+"/Cache/"+ fileName + '.json'
        print filePathNameWExt
        with open(filePathNameWExt, 'w') as fp:
            json.dump(data, fp)

    def readFromJSON(self,fileName):
        filePathNameWExt = self.dir_path + "/Cache/" + fileName + '.json'
        data = {"address_components": [
            {
                "long_name": "Sistem Penyuraian Trafik Kuala Lumpur Barat",
                "short_name": "E23",
                "types": ["route"]
            }]}
        if os.path.isfile(filePathNameWExt):
            with open(filePathNameWExt) as fp:
                    d = json.load(fp)
                    print d["day"]

            return True
        else :
            return False



    def testChart(self):
        data = {'spending': [{u'created_time': u'2017-11-24T15:47:36+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Kolej Kediaman Kelapan,Universiti Malaya.', u'id': u'1362815530452737_1554897484577873'}], 'travel': [], 'sports': [{u'created_time': u'2017-11-29T06:43:04+0000', u'message': u'Last day at um academia community conference 2017', u'story': u'Khairul Albertado Danial is at Crystal Crown Hotel Petaling Jaya.', u'id': u'1362815530452737_1559629380771350'}, {u'created_time': u'2017-11-19T05:25:25+0000', u'message': u'Datang la support boling padang ulk pada 25/26 november', u'story': u'Khairul Albertado Danial is at Kompleks Sukan Negara Bukit Kiara.', u'id': u'1362815530452737_1549934008407554'}], 'politic': [{u'created_time': u'2017-11-29T06:43:04+0000', u'message': u'Last day at um academia community conference 2017', u'story': u'Khairul Albertado Danial is at Crystal Crown Hotel Petaling Jaya.', u'id': u'1362815530452737_1559629380771350'}, {u'created_time': u'2017-11-24T15:47:36+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Kolej Kediaman Kelapan,Universiti Malaya.', u'id': u'1362815530452737_1554897484577873'}, {u'created_time': u'2017-11-24T09:41:04+0000', u'message': u'Alhamdulillah , lots more to improve.. 1 more week towards integration. My team will do well... :Putnam:', u'story': u'Khairul Albertado Danial is at Kerinchi LRT station.', u'id': u'1362815530452737_1554649987935956'}, {u'created_time': u'2017-11-21T07:59:28+0000', u'message': u'Irfan Kamaruddin Raam Kanaisan Hafiz Redha Aida Baharun, actually this is how alzheimer brain looks like , it is good to know about all this topic', u'story': u"Khairul Albertado Danial shared Dr John's video.", u'id': u'1362815530452737_1551861968214758'}, {u'created_time': u'2017-10-16T12:44:58+0000', u'message': u'Hazim Kamaruzzaman Yeah manager', u'story': u"Khairul Albertado Danial shared Jawatankuasa Pelajar Luar Kampus Universiti Malaya's post.", u'id': u'1362815530452737_1519290884805200'}], 'education': [{u'created_time': u'2017-11-08T11:27:17+0000', u'message': u'Main lawn bowl bersama Raam Kanaisan Irfan Kamaruddin dan Hazim Kamaruzzaman\n\n#FYPpurpose', u'story': u'Khairul Albertado Danial is with Raam Kanaisan and 2 others at Malaysian Lawn Bowls Federation.', u'id': u'1362815530452737_1539814052752883'}], 'technology': [{u'created_time': u'2017-11-29T06:43:04+0000', u'message': u'Last day at um academia community conference 2017', u'story': u'Khairul Albertado Danial is at Crystal Crown Hotel Petaling Jaya.', u'id': u'1362815530452737_1559629380771350'}, {u'created_time': u'2017-11-24T15:47:36+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Kolej Kediaman Kelapan,Universiti Malaya.', u'id': u'1362815530452737_1554897484577873'}, {u'created_time': u'2017-11-21T07:59:28+0000', u'message': u'Irfan Kamaruddin Raam Kanaisan Hafiz Redha Aida Baharun, actually this is how alzheimer brain looks like , it is good to know about all this topic', u'story': u"Khairul Albertado Danial shared Dr John's video.", u'id': u'1362815530452737_1551861968214758'}, {u'created_time': u'2017-11-19T05:25:25+0000', u'message': u'Datang la support boling padang ulk pada 25/26 november', u'story': u'Khairul Albertado Danial is at Kompleks Sukan Negara Bukit Kiara.', u'id': u'1362815530452737_1549934008407554'}, {u'created_time': u'2017-11-08T11:27:17+0000', u'message': u'Main lawn bowl bersama Raam Kanaisan Irfan Kamaruddin dan Hazim Kamaruzzaman\n\n#FYPpurpose', u'story': u'Khairul Albertado Danial is with Raam Kanaisan and 2 others at Malaysian Lawn Bowls Federation.', u'id': u'1362815530452737_1539814052752883'}]}

        print Visualization.pieChart(data)

    def testPosNeg(self):
        string = ['Fighting till the end. #finalWeek']
        print nBayesTesting.getListValue(string)

    def testTopic(self):
        print self.topic["spending"].count()

    def tagUser(self):

        if 'message_tags' in self.tag:
            for i in self.tag['message_tags']:
                print i['name']

    def decHour(self):

        print self.graph.search(type='user',q='Mark Zuckerberg')

        IS = 24

        for i in range(1,24) :
            self.Hour[i] = []
        print self.Hour

    def dateTime(self):
        for i in self.time:

            # date = datetime.strptime(i[0:16], '%Y-%m-%dT%H:%M')
            print i
            date = datetime.strptime(i[0:16], '%Y-%m-%dT%H:%M')
            self.Hour[int(date.hour)] = "sal",date.hour
            print date.weekday()




    def getDict(self):
        print self.dict

    def getTop5(self):
        self.dict.pop('top', None)
        self.dict['top'] = dict(Counter(self.dict).most_common(5))
        print self.dict['top']

    def callDict(self):
        self.dict[0] = ["sad","sdd"]
        self.dict[1] = ["hikta"]

    def addDict(self):
        self.dict[0].append("takjtak")

    def UTC(self):
        local_timezone = tzlocal.get_localzone()  # get pytz tzinfo
        i="2017-10-11T08:02:57+0000"
        utc_time = datetime.strptime(i[0:16], '%Y-%m-%dT%H:%M')

        print local_time

    def printTime(self):
        print self.hour



if __name__ == "__main__":
    x= tahi()
    # x.tagUser()
    x.printTime()
    # x.testChart()
    # filename = "1362815530452737"
    # data = {"address_components": [
    #     {
    #         "long_name": "Sistem Penyuraian Trafik Kuala Lumpur Barat",
    #         "short_name": "E23",
    #         "types": ["route"]
    #     }]}
    #
    #
    # if not x.readFromJSON(filename):
    #     x.writeToJSONFile(filename, data)

