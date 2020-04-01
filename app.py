from flask import Flask
from flask_cors import CORS
from twitter.botscript import bot

app = Flask(__name__)
app.register_blueprint(bot, url_prefix="/bot")

CORS(app)

@app.route('/', methods=['GET'])
def main():
    return "Hello world"

app.run()
print("app run")