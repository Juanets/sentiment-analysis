import json
import tweepy
from secrets import *
from textblob import TextBlob
    
# store sentiment
samples = []

class TwitterAPI():

	def __init__(self):
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)		
		self.api = tweepy.API(auth)


class Listener(tweepy.StreamListener):

    def on_data(self, data):
        try:
            # get tweet data
            all_data = json.loads(data)
            tweet = all_data['text']
            
            # avoid RTs
            if 'RT' not in tweet:
                tweet_analysis = TextBlob(tweet)
                self.average(tweet_analysis.sentiment)
        except Exception as e:
            pass
    
    
    def on_error(self, status_code):
        print(status_code)
    

    def average(self, s):
        global samples       

        # if analysis is strong enough and sentiment isn't neutral
        if s.subjectivity > .8 and s.polarity != 0.0:
            samples.append(s.polarity)
            average_sentiment = sum(samples) / float(len(samples))
            
            print("AVG: {}".format(average_sentiment))


# start stream of tweets
stream = tweepy.Stream(TwitterAPI().api.auth, Listener())
stream.filter(track=['obama'])