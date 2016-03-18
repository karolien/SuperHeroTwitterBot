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
wordnikURL = "http://api.wordnik.com:80/v4/words.json/randomWord?hasDictionaryDef=false&minCorpusCount=0&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&minLength=5&maxLength=-1&api_key=2e0e51ea24b90900f600d0a4db3044f1fc4fba36fa243228c";
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

wordApi = WordsApi.WordsApi(client)

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
			sql = ("SELECT superheroname FROM superheronames WHERE user_id = " + str(id))
			c.execute(sql)
			superheroname = c.fetchone()[0]
			tweet = ("Hello " + superheroname + " @" + username)
			api.update_status(status=tweet)
		except:
			#superheroname = self.getSuperHeroName()
			superhername = wordApi.getRandomWords(includePartOfSpeech='noun', limit='1')[0].text
			c.execute("INSERT INTO superheronames (user_id, superheroname) VALUES (%s,%s)",
				(id, superheroname))
			conn.commit()
			tweet = ("Welcome to the club " + superheroname + " @" + username)
			api.update_status(status=tweet)
		return True

	def on_error(self, status):
		print (status)
		
	def getSuperHeroName(self):
		response = urllib2.urlopen(wordnikURL).read()
		object = json.loads(response)
		print object['word']
		return object['word']
		
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["@aSuperHeroClub"])


				  