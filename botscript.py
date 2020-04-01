import tweepy as tp
import atexit
from config import twitter_credentials
from apscheduler.schedulers.blocking import BlockingScheduler

# Credentials
consumer_key = twitter_credentials["api_key"]
consumer_secret = twitter_credentials["api_secret_key"]
access_token = twitter_credentials["access_token"]
access_secret = twitter_credentials["access_secret_token"]

# login to twitter account api
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)

def tweet():
    api.update_status("hello")

# Starts scheduler
sched = BlockingScheduler()
sched.start()
sched.add_job(func=tweet, trigger="interval", hours=7)

atexit.register(lambda: sched.shutdown())