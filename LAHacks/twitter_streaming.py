# encoding: utf-8
#immporting the required methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy

# Simple program that demonstrates how to invoke Azure ML Text Analytics API: key phrases, language and sentiment detection.
import urllib2
import urllib
import sys
import base64
import json

# Azure portal URL.
base_url = 'https://westus.api.cognitive.microsoft.com/'
# Your account key goes here.
account_key = '9beccad39f3d42b2b7a2aec48e724f52'

headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}
            
input_texts = '{"documents":[{"id":"1","text":"hello world"},{"id":"2","text":"hello foo world"},{"id":"three","text":"hello my world"},]}'


#variables that contain user credentials to access the Twitter API
access_key = '3503362290-vJqr2AmMqZLfIIemvpCk6Tvj2bfFze99fxYvMf8'
access_secret = '5VE0naJPQi48M8J2ETd2zRXksfujI8EyQtTVsFqC0DCVn'
consumer_key = 'qG3qDulRMJLi3uhehHtqRnx5I'
consumer_secret = 'F96GON8vjUYCdTBtllQTYWUe2jl8s1UWx6r4enKs9KPLUZUIiD'


def get_all_tweets(screen_name,prev_tweets_to_get):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=prev_tweets_to_get)
	
	#save most recent tweets
	alltweets.extend(new_tweets)

	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [tweet.text.encode("utf-8") for tweet in alltweets]
	
	return outtweets


if __name__ == '__main__':
	#pass in the username of the account you want to download
    outtweets = get_all_tweets("elonmusk",10)
    # Detect sentiment.
    batch_sentiment_url = base_url + 'text/analytics/v2.0/sentiment'
    i = 0
    input_texts_dict = '{"documents":['
    for tweet in outtweets:
        input_texts_dict += '{"id":"' + str(i) + '", "text":"' + tweet + '"}'
        if i < len(outtweets)-1:
            input_texts_dict += ','
        #input_texts_dict["documents"].append({"id":str(i), "text":tweet})
        i += 1
    req = urllib2.Request(batch_sentiment_url, str(input_texts_dict), headers) 
    response = urllib2.urlopen(req)
    result = response.read()
    obj = json.loads(result)
    sentiment_values = []
    for sentiment_analysis in obj['documents']:
       sentiment_values.append(sentiment_analysis['score'])
    
     