# Get relevant news
from newsapi import NewsApiClient
from config import news_api_key
from flask import Blueprint, request
import json
import datetime

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
    country_item = ''
    if query != None: 
        query_item = ', {}'.format(query)
    if country != None:
        country_item = ', {}'.format(country)

    # Checks if country is only one word
    # if len(country.split(" ")) == 1 and country != "world":
    #     top_headlines = newsapi.get_top_headlines(q='coronavirus, covid',
    #                                               language='en',
    #                                               country=country)
    top_headlines = newsapi.get_top_headlines(q='coronavirus, covid{}, {}'.format(query_item, country_item),
                                                #   category='health',
                                                language='en')
                                            #   country=country_item) # issue is that the news api only takes in certain country names

    # idea, if there are no top_headlines, resort to using ALL ARTICLES

    if top_headlines["status"] == "ok":
        # Chooses most important headlines using "ML"
        articles_list = top_headlines["articles"]
        if len(articles_list) == 0:
            today = datetime.date.today()
            yday = today - datetime.timedelta(days=1)

            news_articles = newsapi.get_everything(q='coronavirus, covid{},{}'.format(query_item, country_item),
                                                   from_param=yday,
                                                   sort_by="relevancy",
                                                   language="en")
            if news_articles["status"] == "ok":
                articles_list = news_articles["articles"]

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
    country = None
    if "q" in request.args:
        query = request.args.get("q")
        print("q = " + query)

    if "c" in request.args:
        country = request.args.get("c")
        print("c = " + country)

    articles = getTopHeadlines(country=country, query=query)
    # print(articles)
    return {
        'urls': extract_urls(articles),
        'articles': articles
    }

# print(getTopHeadlines())