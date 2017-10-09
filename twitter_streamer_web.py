#---------------------------------------------------------------------------
# Twitter Streaming Bot - Copyright 2017, Leo Brack, All rights reserved.
#---------------------------------------------------------------------------
# This code tracks keyword mentions by streaming real time data from the 
# the twitter API.
# Tweet data is saved to database
# --------------------------------------------------------------------------

import tweepy,time,json,datetime
import MySQLdb

# Import twitter API keys and words to track from "authentication.py"
from authentication import authentication
from authentication import configure

# Global variables to keep track of tweets
num_tweets = 0
num_points = 0
start_time = time.time()
elapsed_time = 0
total_time = 0
x = []
y = []

#---------------------------------------------------------------------------
# DATABASE FUNCTIONS
#---------------------------------------------------------------------------

# This function takes the 'created_at', 'text', 'screen_name' and 'tweet_id' and stores it
# into a MySQL database
def store_data(created_at, text, screen_name, tweet_id):
    db=MySQLdb.connect(host='localhost', user='leobrack', passwd='password', db='crypto_db', charset="utf8mb4")
    cursor = db.cursor()
    insert_query = "INSERT INTO raw_tweets (tweet_id, screen_name, created_at, text) VALUES (%s, %s, %s, %s)"
    #try:
    cursor.execute(insert_query, (tweet_id, screen_name, created_at, text))
    db.commit()
    cursor.close()
    db.close()
    #except:
        #print "Unexpected error when saving tweet to database", sys.exc_info()[0]
    #return
    
#---------------------------------------------------------------------------
# Tweeter Streamer Class
#---------------------------------------------------------------------------

# Define class to handle incoming tweets 
class MyListener(tweepy.StreamListener):
    
    def __init__(self, api = None, update_time = 5):
        self.api = api
        self.update_time = update_time
            
            
    # This function is called when we recieve a tweet       
    def on_data(self, data):
        try:        
            # Get time stamp for tweet
            global start_time
            elapsed_time = time.time() - start_time  
          
            #Load data from json format
            tweet = json.loads(data)
            text = tweet['text']
            screen_name = tweet['user']['screen_name']
            tweet_id = tweet['id']
            created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        
            #Filter tweet, uncomment line below for filtering
            #self.filter_tweet(tweet)
        
            #Define counter as global variable
            global num_tweets
            num_tweets += 1 #Add 1 to count as we have a new tweet!
            print num_tweets  #Check response 
            
            store_data(created_at, text, screen_name, tweet_id)
                            
            return True 
            
        except Exception, e:
            print e
            pass
 
       
    # Function to filter out retweets   
    def filter_tweet(self,tweet):
        if 'RT' in tweet['text']:
            print 'Retweet'
            return
        else:
            pass 
   
    # Error handling                   
    def on_error(self, status):
        print(status)
        return True
        
        
        
#---------------------------------------------------------------------------
# Main
#---------------------------------------------------------------------------
           
if __name__ == '__main__':       
        
        
        
    #---------------------------------------------------------------------------
    # STREAMER SET UP
    #---------------------------------------------------------------------------
     
     
    auth = authentication()
    config = configure()
    
    # Import words to track as variable 'track'        
    track = config.gettrack_1()
    update_time = config.getupdate_time   
                  
    consumer_key = auth.getconsumer_key()
    consumer_secret = auth.getconsumer_secret()

    access_token = auth.getaccess_token()
    access_token_secret = auth.getaccess_token_secret()

    # tweepy handles accessing the API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    twitter_stream = tweepy.Stream(auth, MyListener(api, update_time))

    # Import words to track as variable 'track'        
    track = config.gettrack_1()
    update_time = config.getupdate_time
    
    # Start streaming tweets from twitter
    twitter_stream.filter(track = track)