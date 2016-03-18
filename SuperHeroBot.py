from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from wordnik import *
import tweepy
import MySQLdb
import time
import json
import os

#wordnik connection
apiUrl = 'http://api.wordnik.com/v4'
apiKey = ['WORDNIK_KEY']
client = swagger.ApiClient(apiKey, apiUrl)
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

wordApi = WordApi.WordApi(client)

class listener(StreamListener):
	def on_data(self,data):
		all_data = json.loads(data)
		tweet_from_user = all_data["text"]
		username = all_data["user"]["screen_name"]
		id = all_data["user"]["id"]
		id = int(id)
		superheroname = ""
		tweet = "" 
		print(self.getNoun())
		try:
			sql = ("SELECT superheroname FROM superheronames WHERE user_id = " + str(id))
			c.execute(sql)
			superheroname = c.fetchone()[0]
			tweet = ("Hello " + superheroname + " @" + username)
			api.update_status(status=tweet)
		except:
			superheroname = self.getNoun()
			c.execute("INSERT INTO superheronames (user_id, superheroname) VALUES (%s,%s)",
				(id, superheroname))
			conn.commit()
			tweet = ("Welcome to the club " + superheroname + " @" + username)
			api.update_status(status=tweet)
		return True

	def on_error(self, status):
		print (status)
		
	def getNoun(self):
		noun = wordApi.getNoun()
		return noun.text
		
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["@aSuperHeroClub"])


				  