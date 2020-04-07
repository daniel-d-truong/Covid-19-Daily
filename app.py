from flask import Flask
from flask_cors import CORS
from twitter.botscript import bot
from data import data
from news import news
from twilio import twilio

app = Flask(__name__)

app.register_blueprint(bot, url_prefix="/bot")
app.register_blueprint(data, url_prefix="/data")
app.register_blueprint(news, url_prefix="/news")
app.register_blueprint(twilio, url_prefix="/twilio")

CORS(app)

@app.route('/', methods=['GET'])
def main():
    return "Hello world"

app.run()
print("app run")