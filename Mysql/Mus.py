import tweepy
import json
from TwitterSearch import *
import collections

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
tso = TwitterSearchOrder() # create a TwitterSearchOrder object
tso.set_keywords(['musfirah']) # let's define all words we would like to have a look for
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
        name = tweet['user']['screen_name']
        test = tweet['text']


        result = test.split(" ")
        intext = [s for s in result if "musfirah" in s]
        usertext.append(' '.join(intext))
        #print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text'] ) )

matching = [s for s in username if "musfirah" in s]
merge = usertext + matching
print   merge
usermerge = []
for x in merge:
    if x not in usermerge:
        usermerge.append(x)

print usermerge
print usermerge
counter = collections.Counter(merge)
#print counter.keys()
print counter

realuser = []
import httplib ##checking if name in usermerge is a real account
for x in usermerge:
    c = httplib.HTTPConnection('www.twitter.com/'+x)
    print c
    c.request("HEAD", '')
    if c.getresponse().status == 200:
        realuser.append(x)

print realuser