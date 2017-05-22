

from twitter import *

try:
    import json
except ImportError:
    import simplejson as json

config = {}
execfile("config.py", config)

class Twitter():


    twitter = Twitter(
		auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

    username = raw_input("Enter username to search: @")

    def getUserProfile(self):
        user = self.twitter.users.search(q = self.username)
        for user in user:
            print "Username: @%s" % user["screen_name"]
            print "Name: %s" % user["name"]
            print "Twitter ID: %s" % user["id"]
            print "Bio: %s" % user["description"]
            print "Followers: %s " % user["followers_count"]
            print "Account created since: %s" %  user["created_at"]
            print "Profile image: %s" % user["profile_image_url"]





    def getConnections(self):
        friends = self.twitter.friends.ids(screen_name=self.username)
        print "Follows %d accounts: " % (len(friends["ids"]))
        for n in range(0, len(friends["ids"]), 100):
            ids = friends["ids"][n:n+100]
        #
        # 	#-----------------------------------------------------------------------
        # 	# create a subquery, looking up information about these users
        # 	# twitter API docs: https://dev.twitter.com/rest/reference/get/users/lookup
        # 	#-----------------------------------------------------------------------
            subquery = self.twitter.users.lookup(user_id = ids)
            #print subquery
            for user in subquery:
        # 		#-----------------------------------------------------------------------
        # 		# now print out user info, starring any users that are Verified.
        # 		#-----------------------------------------------------------------------
        		print " [%s] %s - %s [%s]" % ("*" if user["verified"] else " ", user["screen_name"], user["location"], user["description"])

    def getTweets(self):
        tweet = self.twitter.statuses.user_timeline(q = self.username, exclude_replies = "true")
        for tweet in tweet:
            print "Tweet: %s" % tweet["text"]
            print "Source: %s" % tweet["source"]
            print "Reply to user: @%s" % tweet["in_reply_to_screen_name"] if tweet["in_reply_to_screen_name"]!="None" else "---"
            print "Tweet location: %s" % tweet["coordinates"] if tweet["coordinates"]!="None" else "---"


x = Twitter()
x.getUserProfile()
x.getConnections()
x.getTweets()


