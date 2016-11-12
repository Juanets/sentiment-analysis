import json
import tweepy
from secrets import *
from textblob import TextBlob
from plot import Plot

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
        global plt_stream    

        # if analysis is strong enough and sentiment isn't neutral
        if s.subjectivity > .8 and s.polarity != 0.0:
            samples.append(s.polarity)
            average_sentiment = sum(samples) / float(len(samples))
            
            # add to stream
            plt_stream.write(dict(y=[average_sentiment]))


def start_stream():
    # start stream of tweets
    stream = tweepy.Stream(TwitterAPI().api.auth, Listener())
    stream.filter(track=['trump'], async=True)

    # open plotly stream
    p.init_plot('trump')
    plt_stream.open()

if __name__ == '__main__':
    start_stream()
