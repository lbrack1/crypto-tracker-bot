#Configuration file
#Edit tracked words and enter API consumer keys


class configure:
    
    def __init__(self):
        
        #Update this with the words you want to track
        self.track1 = ['bitcoin']
        self.update_time = 5
        
        
    def gettrack_1(self):
        return self.track1
    def getupdate_time(self):
        return self.update_time



class authentication:

    def __init__(self):
        # Go to http://apps.twitter.com and create an app.
        # The consumer key and secret will be generated for you after
        self.consumer_key ='gtEM5GbUrtxlHwvbSq48Sxavu'
        self.consumer_secret='AdgQzRSgk4oMNzX6eu0CcHisoUjNGkWaVyN6c5Zromsqad5T6K'
        # After the step above, you will be redirected to your app's page.
        # Create an access token under the the "Your access token" section
        self.access_token='881438260605714433-TlDTZrztbkDXGV2BGHQTf8sPvF8sAnv'
        self.access_token_secret='488NKcMrjvBqldc0YYpMJ5hnhAE5AWoo2XUBm3EtbYqSO'

    def getconsumer_key(self):
        return self.consumer_key
    def getconsumer_secret(self):
        return self.consumer_secret
    def getaccess_token(self):
        return self.access_token
    def getaccess_token_secret(self):
        return self.access_token_secret