from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import MySQLdb
import time
import json
import os
import urllib2
import random

#wordnik connection
wordnikURLNoun = "http://api.wordnik.com/v4/words.json/randomWord?hasDictionaryDef=true&minCorpusCount=100&maxCorpusCount=-1&minDictionaryCount=30&maxDictionaryCount=-1&includePartOfSpeech=noun&excludePartOfSpeech=noun-plural,noun-posessive,proper-noun,proper-noun-plural,proper-noun-posessive,suffix,family-name,idiom,affix&minLength=5&maxLength=8&api_key=" + str(os.environ['WORDNIK_KEY']);

wordnikURLAdjective = "http://api.wordnik.com/v4/words.json/randomWord?minCorpusCount=10000&minDictionaryCount=20&excludePartOfSpeech=proper-noun%2Cproper-noun-plural%2Cproper-noun-posessive%2Csuffix%2Cfamily-name%2Cidiom%2Caffix&hasDictionaryDef=true&includePartOfSpeech=adjective&maxLength=7&api_key=" + str(os.environ['WORDNIK_KEY']);
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
		try:
			conn = MySQLdb.connect(os.environ['SERVER'],os.environ['USER_NAME'],os.environ['PASSWORD'],os.environ['DATABASE_NAME'])
			c = conn.cursor()
			sql = ("SELECT superheroname FROM superheronames WHERE user_id = " + str(id))
			c.execute(sql)
			superheroname = c.fetchone()[0]
			tweet = ("Hello " + superheroname + " @" + username)
			try:
				api.update_status(status=tweet)
			except Exception as e:
				print e
		except:
			superheroname = self.getRandomTitle() + ' ' + self.getSuperHeroName(wordnikURLAdjective) + ' ' + self.getSuperHeroName(wordnikURLNoun)
			c.execute("INSERT INTO superheronames (user_id, superheroname) VALUES (%s,%s)",
				(id, superheroname))
			conn.commit()
			tweet = ("Welcome to the club " + superheroname + " @" + username)
			api.update_status(status=tweet)
		return True

	def on_error(self, status):
		print (status)
		
	def getSuperHeroName(self, url):
		response = urllib2.urlopen(url).read()
		object = json.loads(response)
		output = object['word']
		output = output[:1].upper() + output[1:]
		print output
		return output
	
	def getRandomTitle(self):
		possible_titles = ['Captain','Super', 'Dr.', 'The', 'The', 'The']
		return random.choice(possible_titles)
		

		
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["@aSuperHeroClub"])


				  