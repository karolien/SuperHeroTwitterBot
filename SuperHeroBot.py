from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import MySQLdb
import time
import json
import os
import urllib2

#wordnik connection
wordnikURLNoun = "http://api.wordnik.com:80/v4/words.json/randomWord?hasDictionaryDef=false&minCorpusCount=0&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&&includePartOfSpeech=noun&minLength=5&maxLength=-1&api_key=" + str(os.environ['WORDNIK_KEY']);

wordnikURLAdjective = "http://api.wordnik.com:80/v4/words.json/randomWord?hasDictionaryDef=false&minCorpusCount=0&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&&includePartOfSpeech=adjective&minLength=5&maxLength=-1&api_key=" + str(os.environ['WORDNIK_KEY']);
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
		id = int(id)
		superheroname = ""
		tweet = "" 
		self.getSuperHeroName()
		try:
			conn = MySQLdb.connect(os.environ['SERVER'],os.environ['USER_NAME'],os.environ['PASSWORD'],os.environ['DATABASE_NAME'])
			c = conn.cursor()
			print("inside try statement")
			sql = ("SELECT superheroname FROM superheronames WHERE user_id = " + str(id))
			c.execute(sql)
			print("sql passed")
			superheroname = c.fetchone()[0]
			print("got superhero name")
			tweet = ("Hello " + superheroname + " @" + username)
			print(tweet)
			try:
				api.update_status(status=tweet)
				print("tweeted!")
			except Exception as e:
				print e
		except:
			print("exception raised")
			superheroname = self.getSuperHeroName()
			c.execute("INSERT INTO superheronames (user_id, superheroname) VALUES (%s,%s)",
				(id, superheroname))
			conn.commit()
			tweet = ("Welcome to the club " + superheroname + " @" + username)
			api.update_status(status=tweet)
		return True

	def on_error(self, status):
		print (status)
		
	def getSuperHeroName(self):
		response = urllib2.urlopen(wordnikURLNoun).read()
		object = json.loads(response)
		print object['word']
		return object['word']
		
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["@aSuperHeroClub"])


				  