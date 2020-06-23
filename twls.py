import tweepy
from conf import read_conf
import re




consumer_key = read_conf("cfg.ini","consumer_key")
consumer_secret = read_conf("cfg.ini","consumer_secret")
access_token = read_conf("cfg.ini","access_token")
access_token_secret = read_conf("cfg.ini","access_token_secret")




auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def get_tweets():
    data = tweepy.Cursor(api.user_timeline).items()
    tweets = []

    for status in data:


        tweet_json = status._json
        tweet_id = tweet_json['id']
        text = status.text
        url = f"https://twitter.com/realabja/status/{tweet_id}"
        tweets.append(f"{text} \n\n {url}")

    return tweets

get_tweets()

