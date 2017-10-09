#---------------------------------------------------------------------------
# Twitter Post Processing - Copyright 2017, Leo Brack, All rights reserved.
#---------------------------------------------------------------------------
# This code loads data from the raw_tweets database and analyses it ready 
# for website display
# Data saved to new database processed_tweets
# Script scheduled to be executed every 5 seconds by using python anyhwere scheduler
# --------------------------------------------------------------------------

from __future__ import division
import time,json,datetime
import MySQLdb
import pandas as pd

import nltk
import re
import string
import time
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#Define how often the script updates with new data
update_time = 5 #seconds

#---------------------------------------------------------------------------
# DATABASE FUNCTIONS
#---------------------------------------------------------------------------

# This function takes the 'created_at', 'text', 'screen_name' and 'tweet_id' and stores it
# in a MySQL database
def store_data(time, most_common, tps):
    #db=MySQLdb.connect(host='localhost', user='leobrack', passwd='password', db='crypto_db', charset="utf8mb4")
    db=MySQLdb.connect(host='brackl1.mysql.pythonanywhere-services.com', user='brackl1', passwd='database', db='brackl1$crypto_db', charset="utf8mb4")
    cursor = db.cursor()
    insert_query = "INSERT INTO processed_tweets (time, most_common, tps) VALUES (%s, %s, %s)"
    #try:
    cursor.execute(insert_query, (time, most_common, tps))
    db.commit()
    cursor.close()
    db.close()
    #except:
        #print "Unexpected error when saving tweet to database", sys.exc_info()[0]
    #return

# This function reads tweet data from tweets in the database raw_tweets if they are created at between
# start and end variables   

def read_data_pandas(start,end):
    #db=MySQLdb.connect(host='localhost', user='leobrack', passwd='password', db='crypto_db', charset="utf8mb4")
    db=MySQLdb.connect(host='brackl1.mysql.pythonanywhere-services.com', user='brackl1', passwd='database', db='brackl1$crypto_db', charset="utf8mb4")
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
    
# Function to strip links from tweet
def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')    
    return text

# Function to strip entities from tweet
def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

# Function to calculate words that appear most frequently  
def word_freq(tweet_df):

    # Import list of stop words
    stop_words = set(stopwords.words('english'))

    # List to hold all words
    all_words = []
      
    # Loop over all tweets in section
    for row in tweet_df.text:
                
        result = strip_all_entities(strip_links(row)) # remove links and entities
        result1 = re.sub(r"RT+", "", result) # remove "RT"
        
        word_tokens = word_tokenize(result1)

        # Removes stop words and recreates tweet
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)  
    
        # Adds every word to a list
        for w in filtered_sentence:
            all_words.append(w.lower())
        
    # Process list of words, calculate frequency distribution
    all_words = nltk.FreqDist(all_words)
    most_common = all_words.most_common(15)
    most_common_json = json.dumps(most_common)
    return most_common_json
    

#---------------------------------------------------------------------------
# MAIN CODE
#---------------------------------------------------------------------------
# This script runs forever, updating every 5 seconds

while True:
    
        print '----------------'
        # TESTING ONLY -Read tweets created between these dates
        #start = datetime.date(2017,9,21)
        #end = datetime.date(2017,9,22)

        # RUN TIME - Get datetime string corresponding to last 5 seconds
        start = datetime.datetime.now() - datetime.timedelta(seconds=5) 
        end = datetime.datetime.now()
        print start
        # Get data in pandas dataframe format
        data = read_data_pandas(start,end)

        # Processing 
        tps = tweets_per_sec(data, update_time)
        most_common = word_freq(data)
        print tps
        print most_common

        store_data(start,most_common, tps)
        print '----------------'
        
        time.sleep(5)

        