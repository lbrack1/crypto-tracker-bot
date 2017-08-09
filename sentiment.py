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



# --------------------------------------------------------------------------
# Function to retrieve data from database

def get_data(x):
    
    # Open a database connection
    connection = MySQLdb.connect (host = "localhost", user = "leobrack", passwd = "password", db = "twitter")

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
    cursor.execute ("select text from twitter where created_at between '2017-08-09 09:59:30' and '2017-08-09 10:00:52';")

    # Fetch all of the rows from the query
    text = cursor.fetchall ()
        
    # Close the cursor object
    cursor.close ()

    # Close the connection
    connection.close ()

    return text
    


text = get_data(5)

for row in text:
    print row[0]


# Exit the program
sys.exit()