# Get relevant news
from newsapi import NewsApiClient
from config import news_api_key
import requests


newsapi = NewsApiClient(api_key=news_api_key)

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='coronavirus',
                                          category='health',
                                          language='en')

# Get relevant data. Uses https://github.com/javieraviles/covidAPI
covid_all = requests.get('https://coronavirus-19-api.herokuapp.com/all')

# print(top_headlines)
# print(covid_all.text)