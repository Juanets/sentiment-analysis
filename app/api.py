import json
import tweepy
from secrets import *
from plot import Plot
from textblob import TextBlob

# plotly objects
p = Plot()
plt_stream = p.s

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
            
            # avoid RTs
            if (not all_data['retweeted'] 
                and 'RT @' not in all_data['text']
                and 'http' not in all_data['text']):

                tweet = all_data['text']
                tweet_analysis = TextBlob(tweet)
                self.average(tweet_analysis)
        except Exception as e:
            print(e)
            pass
    
    
    def on_error(self, status_code):
        print(status_code)
    

    def average(self, tweet):
        # translate tweet if language isn't english
        language = tweet.detect_language()
        if language is not 'en':
            tweet = tweet.translate(from_lang=language, to='en')

        print(tweet)

        # if analysis is strong enough and sentiment isn't neutral
        if tweet.sentiment.subjectivity > .6 and tweet.sentiment.polarity != 0.0:
            samples.append(tweet.sentiment.polarity)
            average_sentiment = sum(samples) / float(len(samples))
            
            # add to stream
            plt_stream.write(dict(y=[average_sentiment]))


def start_stream(topic):
    # start stream of tweets
    stream = tweepy.Stream(TwitterAPI().api.auth, Listener())
    stream.filter(track=[topic], async=True)

    # open plotly stream
    p.init_plot(topic)
    plt_stream.open()