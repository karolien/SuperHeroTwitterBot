from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
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

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"]
        
        username = all_data["user"]["screen_name"]
        
        c.execute("INSERT INTO superheronames (id, superheroname, username) VALUES (null,%s,%s)",
            ("bob brown", username))

        conn.commit()

        print((username,tweet))
        
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"])