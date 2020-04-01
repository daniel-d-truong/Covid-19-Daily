import tweepy as tp
from config import twitter_credentials

consumer_key = twitter_credentials["api_key"]
consumer_secret = twitter_credentials["api_secret_key"]
access_token = twitter_credentials["access_token"]
access_secret = twitter_credentials["access_secret_token"]

# login to twitter account api
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)

api.update_status("hello")
print(api)