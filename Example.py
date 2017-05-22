import tweepy
import json
from TwitterSearch import *
import collections
from collections import *

# Authentication details. To  obtain these visit dev.twitter.com
#--------- LIVE STREAM CODE --------------------------------------------------------------#

# This is the listener, resposible for receiving data
#class StdOutListener(tweepy.StreamListener):
#       # Twitter returns data in JSON format - we need to decode it first
#        decoded = json.loads(data)
#
#        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
#       print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
#        print ''
#        return True

#    def on_error(self, status):
#        print status

#if __name__ == '__main__':
#    l = StdOutListener()
#    auth = tweepy.OAuthHandler('BliBNXLccSPeltdwasVj97IVq', 'xVPabuKZBk2Js6GNDdQOXmkUlKAiwl6idSmlSoGwWGrMnzpveF')
#    auth.set_access_token('2839003009-D2zVcnyKpdQpI6motw2sdpFYt0YytOkCNE211k5', 'iMsvjBeBHUJm0tPVwAEZQTOD7Vu8Gbv0UsoGUXvoOLugI')

#    print "Showing all new tweets for #programming:"

#    # There are different kinds of streams: public stream, user stream, multi-user streams
#    # In this example follow #programming tag
#    # For more details refer to https://dev.twitter.com/docs/streaming-apis
#    stream = tweepy.Stream(auth, l)
#    stream.filter(track=['Nurul'])

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def search():
    print 'Enter keyword :'
    key = raw_input()

    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords([key]) # let's define all words we would like to have a look for
    #tso.set_language('de') # we want to see German tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    ts = TwitterSearch(
        consumer_key = 'BliBNXLccSPeltdwasVj97IVq',
        consumer_secret = 'xVPabuKZBk2Js6GNDdQOXmkUlKAiwl6idSmlSoGwWGrMnzpveF',
        access_token = '2839003009-D2zVcnyKpdQpI6motw2sdpFYt0YytOkCNE211k5',
        access_token_secret = 'iMsvjBeBHUJm0tPVwAEZQTOD7Vu8Gbv0UsoGUXvoOLugI'
        )
    username = []
    usertext = []
    for tweet in ts.search_tweets_iterable(tso):

            name = tweet['user']['screen_name'].encode('utf-8')
            text = tweet['text'].encode('utf-8')
            name2 = name.lower()
            text2 = text.lower()
            result = text2.split(" ")
            resultOri = text.split(" ")
            intext = [s for s in resultOri if key in s] #filter @ in tweet
            if intext:
                for y in intext:
                    n = [s for s in intext if '@' in s]
                    if n:
                        for x in n:
                            usertext.append(x[1:])
            username.append(name)
            n2 = [s for s in result if '@' in s] #filter username without keyword
            if n2:
                for x in n2:
                    usertext.append(x[1:])
                    #print x[1:]
                    username.append(name)

            #print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text'] ) )
    merge = usertext + username
    nonDupUser = []
    for x in merge:
        if x not in nonDupUser:
            nonDupUser.append(x)

    sortedUser = []
    sorted = Counter(merge).most_common()
    for x in sorted:
        for y in x:
            if isinstance(y,(int)) == False:
                sortedUser.append(y)

    import requests

    print "Suggested User: "
    for x in sortedUser:
        request = requests.get('http://www.twitter.com/'+x)
        if request.status_code == 200:
            print('http://www.twitter.com/'+x)

search()
