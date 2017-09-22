#---------------------------------------------------------------------------
# Twitter Post Processing - Copyright 2017, Leo Brack, All rights reserved.
#---------------------------------------------------------------------------
# This code loads data from the raw_tweets database and analyses it ready 
# for website display
# Data saved to new database processed_tweets
# --------------------------------------------------------------------------

from __future__ import division
import time,json,datetime
import MySQLdb
import pandas as pd

import nltk
import re
import string
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords

#Define how often the script updates the data
update_time = 5 #seconds

#---------------------------------------------------------------------------
# DATABASE FUNCTIONS
#---------------------------------------------------------------------------

# This function takes the 'created_at', 'text', 'screen_name' and 'tweet_id' and stores it
# into a MySQL database
def store_data(tps, word_freq, now_time):
    db=MySQLdb.connect(host='localhost', user='leobrack', passwd='password', db='crypto_db', charset="utf8mb4")
    cursor = db.cursor()
    insert_query = "INSERT INTO processed_tweets (tps, word_freq, now_time) VALUES (%s, %s, %s)"
    #try:
    cursor.execute(insert_query, (tps, word_freq, now_time))
    db.commit()
    cursor.close()
    db.close()
    #except:
        #print "Unexpected error when saving tweet to database", sys.exc_info()[0]
    #return

# This function reads tweet data from tweets that in the database raw_tweets and created at between
# start and end variables   
def read_data(start,end):
    db=MySQLdb.connect(host='localhost', user='leobrack', passwd='password', db='crypto_db', charset="utf8mb4")
    cursor = db.cursor()
    read_query = "SELECT created_at, text FROM raw_tweets WHERE created_at BETWEEN %s AND %s "
    cursor.execute(read_query, (start,end))
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

def read_data_pandas(start,end):
    db=MySQLdb.connect(host='localhost', user='leobrack', passwd='password', db='crypto_db', charset="utf8mb4")
    read_query = " SELECT created_at, text FROM raw_tweets WHERE created_at BETWEEN %s AND %s "
    df = pd.read_sql(read_query, params = (start,end), con=db)
    return df
    
    
#---------------------------------------------------------------------------
# PROCESSING FUNCTIONS
#---------------------------------------------------------------------------   
    
# Function to calculate tweets per second
def tweets_per_sec(tweet_df, update_time):
    num_tweets = len(tweet_df.index)
    tps = update_time/num_tweets
    return tps

# Function to calculate words that appear most frequently  
def word_freq(tweet_df):

    # Import list of stop words
    stop_words = set(stopwords.words('english'))
    
    # Import tokenizer that takes care of punctuation
    tokenizer = RegexpTokenizer(r'\w+')

    # List to hold all words
    all_words = []
    table = string.maketrans("","")
    
    
    # Loop over all tweets in section
    for row in tweet_df.text:
        
        
        word_tokens = word_tokenize(row)
        print word_tokens
        
        
        

    # Process list of words
    all_words = nltk.FreqDist(all_words)
    print(all_words.most_common(15))
    
    
    
    


#---------------------------------------------------------------------------
# MAIN
#---------------------------------------------------------------------------

# Code runs continuously, processes new data from database every x seconds

# Read tweets created between these dates
start = datetime.date(2017,9,21)
end = datetime.date(2017,9,22)

# Get data in pandas dataframe format
data = read_data(start,end)

# Processing 
#tps = tweets_per_sec(tweet_df, update_time)
word_freq(data)

