#---------------------------------------------------------------------------
# Data Analysis - Copyright 2017, Leo Brack, All rights reserved.
#---------------------------------------------------------------------------
# This code takes data from the mysql data base and extracts the sentiment
#
#
# --------------------------------------------------------------------------
# Import modules

import MySQLdb
import sys
import datetime
import nltk
import re
import string
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords

# -------------------------------------------------------y-------------------
# Function to retrieve data from database

def get_data(x):
    
    # Open a database connection
    connection = MySQLdb.connect (host = "localhost", user = "leobrack", passwd = "password", db = "crypto_db")

    # Prepare a cursor object using cursor() method
    cursor = connection.cursor ()
    
    #Get last x seconds of tweets from mysql
    nowtime = datetime.datetime.now()
    prevtime = nowtime - datetime.timedelta(seconds=x)
    nowtimestr = nowtime.strftime('%Y-%m-%d %H:%M:%S.%f')
    prevtimestr = prevtime.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    # Execute the SQL query using execute() method.
    #cursor.execute ("select text from twitter where created_at between '" + nowtimestr + "' and '" + prevtimestr + "';")

    # FOR DEVELOPMENT! Execute the SQL query using execute() method.
    cursor.execute ("select text from raw_tweets where created_at between '2016-08-09 09:59:30' and '2018-09-01 13:50:32';")

    # Fetch all of the rows from the query
    text = cursor.fetchall ()
        
    # Close the cursor object
    cursor.close ()

    # Close the connection
    connection.close ()

    return text
    
# --------------------------------------------------------------------------

text = get_data(5)

# --------------------------------------------------------------------------
# This can be put into twitter_streamer.py 
# as preprocessing. Won't need to loop over tweets

# Import list of stop words
stop_words = set(stopwords.words('english'))

# Import tokenizer that takes care of punctuation
tokenizer = RegexpTokenizer(r'\w+')

# List to hold all words
all_words = []
table = string.maketrans("","")
# Loop over all tweets in section
for row in text:
    #try:
    
    # Remove useless stuff
    result = re.sub(r"http\S+", "", row[0]) # Links
    result1 = re.sub(r"@\S+", "", result) # Usernames
    result2 = result1.translate(table, string.punctuation) # Punctuation
    result3 = re.sub(r"RT+", "", result2) # "RT"
    result4 = re.sub("\d+", " ", result3) # numbers
    result5 = re.sub(r"\+", "", result4)
    result6 = result5.lower() # Lowercase
      
    # Tokenize (removes punctuation)     
    word_tokens = word_tokenize(result6)
            
    # Removes stop words and recreates tweet
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
           filtered_sentence.append(w)  
    print(filtered_sentence)
    
    # Adds every word to a list
    for w in filtered_sentence:
        all_words.append(w.lower())
            
    #except:
     #   print "ERROR", row[0]

# Process list of words
all_words = nltk.FreqDist(all_words)
print(all_words.most_common(15))
    
# Exit the program
sys.exit()