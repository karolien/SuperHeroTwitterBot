from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import MySQLdb
import time
import json
import os

#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.

conn = MySQLdb.connect(os.environ['SERVER'],os.environ['USER_NAME'],os.environ['PASSWORD'],os.environ['DATABASE_NAME'])
c = conn.cursor()

#consumer key, consumer secret, access token, access secret.
ckey=os.environ['CONSUMER_KEY']
csecret=os.environ['CONSUMER_SECRET']
atoken=os.environ['ACCESS_TOKEN']
asecret=os.environ['ACCESS_SECRET']

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)
api.verify_credentials

class listener(StreamListener):
	def on_data(self,data):
		all_data = json.loads(data)
		tweet_from_user = all_data["text"]
		username = all_data["user"]["screen_name"]
		id = all_data["user"]["id"]
		superheroname = ""
		tweet = "" 

		try:
			c.execute("SELECT superheroname FROM superheronames WHERE user_id = " + id)
			superheroname = c.fetchone()
			tweet = ("Hello " + superheroname + " @" + username)
			api.update_status(tweet)
		except:
			superheroname = "Super Man"
			c.execute("INSERT INTO superheronames (user_id, superheroname) VALUES (%d,%s)",
				(id, superheroname))
			conn.commit()
			tweet = ("Welcome to the club " + superheroname + " @" + username)

		return True

	def on_error(self, status):
		print status
		
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["@aSuperHeroClub"])