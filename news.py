# Get relevant news
from newsapi import NewsApiClient
from config import news_api_key
from flask import Blueprint, request
import json

newsapi = NewsApiClient(api_key=news_api_key)
news = Blueprint('news', __name__)


def invalidSource(article):
    invalid_sources = ["youtube.com"]
    valid_sources = ["latimes.com"]

    name = article["source"]["name"].lower()
    if name in valid_sources: return False
    return name in invalid_sources

def getTopHeadlines(country=None, amount=2, query=None):
    # /v2/top-headlines
    query_item = ''
    if query != None: 
        query_item = ', {}'.format(query)

    # TODO: Make this more robust to actually display the most important articles.
    top_headlines = newsapi.get_top_headlines(q='coronavirus{}'.format(query_item),
                                            #   category='health',
                                              language='en',
                                              country=country)

    if top_headlines["status"] == "ok":
        # Chooses most important headlines using "ML"
        articles_list = top_headlines["articles"]

        # Filter article list
        idx_to_del = []
        for i in range(0, len(articles_list)):
            art = articles_list[i]
            if invalidSource(art): idx_to_del.insert(0, i)

        for i in idx_to_del:
            del articles_list[i]

        machine_learning = articles_list[0:amount]

        return machine_learning
    return []

def extract_urls(articles):
    return list(map(lambda i: i["url"], articles))

@news.route('/', methods=['GET'])
def get_news():
    query = None
    if "q" in request.args:
        query = request.args.get("q")
        print(query)

    articles = getTopHeadlines(query=query)
    # print(articles)
    return {
        'urls': extract_urls(articles),
        'articles': articles
    }

# print(getTopHeadlines())