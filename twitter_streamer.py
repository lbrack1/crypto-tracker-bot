#---------------------------------------------------------------------------
# Twitter Streaming Bot - Copyright 2017, Leo Brack, All rights reserved.
#---------------------------------------------------------------------------
# This code tracks keyword mentions by streaming real time data from the 
# the twitter API. 
# The number of tweets per second are then streamed to the plotly interface
# allowing for real time insight into keyword mentions
# To view plot visit: https://plot.ly/~lbrack1/4
#
# --------------------------------------------------------------------------

import tweepy,time,json,datetime
import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
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
    db=MySQLdb.connect(host='localhost', user='leobrack', passwd='password', db='twitter', charset="utf8mb4")
    cursor = db.cursor()
    insert_query = "INSERT INTO twitter (tweet_id, screen_name, created_at, text) VALUES (%s, %s, %s, %s)"
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
            print created_at 
        
            #Filter tweet, uncomment line below for filtering
            #self.filter_tweet(tweet)
        
            #Define counter as global variable
            global num_tweets
            num_tweets += 1 #Add 1 to count as we have a new tweet!
            
            store_data(created_at, text, screen_name, tweet_id)
                
            # Convert UTF-8 to ASCII and print details to screen
            #print '@%s: %s\n' % (tweet['user']['screen_name'], tweet['text'].encode('ascii', 'ignore'))
        
            # Save data to file
            #self.output.write(data)
          
            # Print stats and plot every "update_time"
            # If there is no tweet recieved within this time block the plot will not update
            # Instead it will update next time it recieves a tweet
            if elapsed_time - self.update_time()  > 0:
                
                # Keep track of the number of points in data array
                global num_points
                num_points = num_points + 1
                
                # Calculate tweets per second
                tweets_per_sec = num_tweets/elapsed_time
                x.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
                y.append(tweets_per_sec)
                
                # Send data to the plotly server to plot
                s.write(dict(x=x, y=y))
                
                self.print_stats(num_tweets,elapsed_time)
                start_time = time.time() 
                num_tweets = 0
                
                # Keep a maximum of x points on graph
                if (num_points > 10):
                    x.pop(0) # Remove first data point
                    y.pop(0)
            
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
   
    # Function to print statistics
    def print_stats(self,counter,elapsed_time):
        print "-----------------------"
        print "Elapsed Time: ", elapsed_time
        print "Number of tweets: ", counter
        print "Tweets/second: %.2f" % (counter/elapsed_time)
       
    # Error handling                   
    def on_error(self, status):
        print(status)
        return True
    
    

#---------------------------------------------------------------------------
# Main
#---------------------------------------------------------------------------
           
if __name__ == '__main__':
    
    
    #---------------------------------------------------------------------------
    # PLOTLY SET UP
    #---------------------------------------------------------------------------
    
    stream_ids = tls.get_credentials_file()['stream_ids']
    
    # Get stream id from stream id list 
    stream_id = stream_ids[0]
    
    # Make instance of stream id object 
    stream_1 = go.Stream(
        token=stream_id,  # link stream id to 'token' key
        maxpoints=10     # keep a max of 80 pts on screen
        )
    
    # Initialize trace of streaming plot by embedding the unique stream_id
    trace1 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
        stream=stream_1         # (!) embed stream id, 1 per trace
    )
    
    data = go.Data([trace1])
    
    # Add title to layout object
    layout = go.Layout(title='Frequency (tweets/sec) of tweets mentioning bitcoin', xaxis={'title':'Time'}, yaxis={'title':'Mentions per Second'})

    # Make a figure object
    fig = go.Figure(data=data, layout=layout)

    # Send fig to Plotly, initialize streaming plot, open new tab
    py.iplot(fig, filename='Bitcoin Mentions')

    # Provide the stream link object the same token that's associated with the trace we wish to stream to
    s = py.Stream(stream_id)

    # Open a connection
    s.open()
    


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

    
#192.168.0.104
    


