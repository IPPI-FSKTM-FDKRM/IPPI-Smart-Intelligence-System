from __future__ import division
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import tweepy
import json
from TwitterSearch import *
from libraryTesting import testing
from nltk.tokenize import word_tokenize
import collections
from collections import *

pos = []
neg = []
key2 = []
def search():
    print 'Enter keyword :'
    key = raw_input()
    key2 = word_tokenize(key)

    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(key2) # let's define all words we would like to have a look for
    #tso.set_language('de') # we want to see German tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    ts = TwitterSearch(
        consumer_key = 'BliBNXLccSPeltdwasVj97IVq',
        consumer_secret = 'xVPabuKZBk2Js6GNDdQOXmkUlKAiwl6idSmlSoGwWGrMnzpveF',
        access_token = '2839003009-D2zVcnyKpdQpI6motw2sdpFYt0YytOkCNE211k5',
        access_token_secret = 'iMsvjBeBHUJm0tPVwAEZQTOD7Vu8Gbv0UsoGUXvoOLugI'
        )
    for tweet in ts.search_tweets_iterable(tso):

            text = tweet['text']
            text = text.lower()
            print text
            val = testing(text)
            pos.append(val[0])
            neg.append(val[1])


''''
    import requests

    print "Suggested User: "
    for x in sortedUser:
        request = requests.get('http://www.twitter.com/'+x)
        if request.status_code == 200:
            print('http://www.twitter.com/'+x)
'''
search()

total = sum(pos) + sum(neg)*-1
if total>0:
    posTotal = (sum(pos)/total)*100
    negTotal = ((sum(neg)*-1)/total)*100
    print total, sum(pos), (sum(neg)*-1)
    print "positive: %.4f negative: %.4f" %(posTotal,negTotal)
else:
    print "Neutral, no data"