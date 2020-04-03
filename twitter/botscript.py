import tweepy as tp
import atexit
from config import twitter_credentials, bot_request_credentials
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Blueprint, request
from twitter.create_tweet import format_tweet

bot = Blueprint('bot', __name__)

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
    try:
        tweet_format = format_tweet()
        api.update_status(tweet_format)
        print("just tweeted. check account.")
        return True
    except Exception as err: 
        print(err)
        return False

# tweet()
@bot.route("/", methods=['POST'])
def post_tweet():
    try:
        json_req = request.json

        if 'id' not in json_req or 'password' not in json_req:
            raise Exception("Did not pass in credentials into the request.")
        
        user = json_req['id']
        pw = json_req['password']

        if user != bot_request_credentials['bot_username'] or pw != bot_request_credentials['bot_password']:
            raise Exception("Credentials passed in are incorrect. Check them again. ")

        return "Just tweeted. " if tweet() else "Tweet failed. Check debug messages. "
    
    except Exception as err:
        return "{}".format(err)

# Starts scheduler
sched = BackgroundScheduler()
sched.add_job(func=tweet, trigger="interval", hours=7)
sched.start()

atexit.register(lambda: sched.shutdown())