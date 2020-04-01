# Get relevant news
from newsapi import NewsApiClient
from config import news_api_key
import requests

newsapi = NewsApiClient(api_key=news_api_key)
global top_headlines

def getTopHeadlines(country=None):
    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(q='coronavirus',
                                              category='health',
                                              language='en',
                                              country=country)

    if top_headlines["status"] == "ok":
        # Chooses most important headlines using "ML"
        machine_learning = top_headlines["articles"][0:2]
        articles_to_share = list(map(lambda i: i["url"], machine_learning))
        return articles_to_share
    return []
    
# print(getTopHeadlines())

def getCovidWorldData():
    # Get relevant data. Uses https://github.com/javieraviles/covidAPI
    covid_all = requests.get('https://coronavirus-19-api.herokuapp.com/all')
    return covid_all.json()

def getCovidCountryData(country=''):
    covid_data = requests.get('https://coronavirus-19-api.herokuapp.com/countries/{}'.format(country))
    try: return covid_data.json() 
    except: return {}