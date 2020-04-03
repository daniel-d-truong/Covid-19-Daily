# Get relevant news
from newsapi import NewsApiClient
from config import news_api_key
from bs4 import BeautifulSoup
import requests

newsapi = NewsApiClient(api_key=news_api_key)
live_data = {}
yday_data = {}

def invalidSource(article):
    invalid_sources = ["youtube.com"]
    return article["source"]["id"] == None or article["source"]["name"] in invalid_sources

def getTopHeadlines(country=None, amount=2):
    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(q='coronavirus',
                                              category='health',
                                              language='en',
                                              country=country)

    if top_headlines["status"] == "ok":
        # Chooses most important headlines using "ML"
        articles_list = top_headlines["articles"]
        articles_iter = iter(articles_list)
        
        # Filter article list
        idx_to_del = []
        for i in range(0, len(articles_list)):
            art = articles_list[i]
            if invalidSource(art): idx_to_del.append(i)

        counter = 0
        for i in idx_to_del:
            idx = i - counter
            del articles_list[idx]
            counter = counter + 1

        machine_learning = articles_list[0:amount]

        articles_to_share = list(map(lambda i: i["url"], machine_learning))
        return articles_to_share
    return []

def getRowsInScrapedData(html_tree, storage):
    col_order = ("region", "total_cases", "new_cases", "total_deaths", "new_deaths", "total_recovered", "active_cases", "serious_critical", "total_per_million", "deaths_per_million")
    tbody_tags = html_tree.find('div').find('table').findAll('tbody')

    def setTableColData(row):
        area_info = {}
        col_iter = iter(col_order) 

        for col in row.findAll('td'):
            col_name = next(col_iter)
            try:
                area_info[col_name] = float(col.text)
            except:
                # Deal with the encoding later
                area_info[col_name] = col.text.encode('utf8').lower().replace(":", "")

        region = area_info.pop("region")
        storage[region] = area_info  

    for row in tbody_tags[0].findAll('tr'):
        setTableColData(row)

    total_world_row = tbody_tags[1].find('tr')
    setTableColData(total_world_row)
    
def webScrapeData(get_yesterday = False):
    # TODO: WOrk this with US States as well
    page = requests.get('https://www.worldometers.info/coronavirus/')
    soup = BeautifulSoup(page.content, 'html5lib')
    today_info = soup.find('div', attrs = {'id':'nav-today'})
    
    getRowsInScrapedData(today_info, live_data)

    if get_yesterday:
        yday_info = soup.find('div', attrs = {'id':'nav-yesterday'})
        getRowsInScrapedData(yday_info, yday_data)


# def compareRateWithYesterday():


def getCovidWorldData():
    # Get relevant data. Uses https://github.com/javieraviles/covidAPI
    # covid_all = requests.get('https://coronavirus-19-api.herokuapp.com/all')
    data = live_data["total"]
    print(live_data["total"])
    print(yday_data["total"])
    return data

def getCovidCountryData(country=''):
    covid_data = requests.get('https://coronavirus-19-api.herokuapp.com/countries/{}'.format(country))
    try: return covid_data.json()
    except: return {}

def getCovidStatesData(state=None):
    covid_data = requests.get('https://corona.lmao.ninja/states')
    try:
        return covid_data.json() if state == None else covid_data.json()[state]
    except:
        return "Unable to fetch from the API"

webScrapeData(get_yesterday=True)
getCovidWorldData()

print(getTopHeadlines())