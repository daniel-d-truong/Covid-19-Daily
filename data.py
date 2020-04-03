from bs4 import BeautifulSoup
from flask import Blueprint, request
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import requests

live_data = {}
yday_data = {}
data = Blueprint('data', __name__)

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


# TODO: Check trends with the day before to check whether we are exponentiall growing or not
# def compareRateWithYesterday():

def getCovidData(country='total', yday=False):
    # if country value passed in is "all", then return all the data
    if country == "all":
        return live_data
    data = live_data[country]
    if yday:
        data = yday_data[country]
    return data
    # covid_data = requests.get('https://coronavirus-19-api.herokuapp.com/countries/{}'.format(country))
    # try: return covid_data.json()
    # except: return {}

def getCovidStatesData(state=None):
    covid_data = requests.get('https://corona.lmao.ninja/states')
    try:
        return covid_data.json() if state == None else covid_data.json()[state]
    except:
        return "Unable to fetch from the API"

@data.route('/<country>', methods=['GET'])
def get_data(country):
    yday_status = request.args.get('day')

    # Can probably write this better
    if yday_status == None:
        return getCovidData(country=country)
    else:
        yday_status = True if yday_status=="yday" else False
        return getCovidData(country=country, yday=yday_status)

@data.route('/', methods=['GET'])
def get_data_world():
    return getCovidData()

webScrapeData(get_yesterday=True)

# Starts scheduler
sched = BackgroundScheduler({'apscheduler.timezone': 'America/Los_Angeles'})
sched.add_job(func=webScrapeData, trigger="interval", minutes=3)
sched.add_job(func=lambda: webScrapeData(get_yesterday=True), trigger="cron", hour=23, minute=30)
sched.start()

atexit.register(lambda: sched.shutdown())