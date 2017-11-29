from collections import Counter
from datetime import datetime
import facebook
from datetime import datetime
import pytz    # $ pip install pytz
import tzlocal # $ pip install tzlocal

class tahi():
    token = 'EAAFyPKV2cOIBANz6EDcSV0CJAoKPt1YCeYGaWF5Tl6FLEmbELopL4XLUp5GZCS2OmwI1zNaa60D5MngsUGW4SZByLZB7w86wyZAZCR50ZAuGZC3dXZAZCLLZCAn5BDzj2UxkP1nlhZCvSmx9LAeZA3fHETSmAJIFZBZCSmooUZD'
    graph =  facebook.GraphAPI(access_token=token,version="2.10")

    tag = {u'id': u'1362815530452737_1551861968214758', u'message_tags': [
        {u'length': 16, u'offset': 0, u'type': u'user', u'id': u'1661021870583831', u'name': u'Irfan Kamaruddin'},
        {u'length': 13, u'offset': 17, u'type': u'user', u'id': u'10214804744656245', u'name': u'Raam Kanaisan'},
        {u'length': 11, u'offset': 31, u'type': u'user', u'id': u'1898030863542173', u'name': u'Hafiz Redha'},
        {u'length': 12, u'offset': 43, u'type': u'user', u'id': u'1587005678025949', u'name': u'Aida Baharun'}]}




    Hour = {}
    Day = {}

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



if __name__ == "__main__":
    x= tahi()
    # x.tagUser()
    x.UTC()
