from data import *
from news import *
from datetime import datetime

def format_tweet():
    articles = getTopHeadlines()
    current_date = datetime.now()

    current_world_data = getCovidData()
    articles = extract_urls(getTopHeadlines())

    tweet = ("[WORLDWIDE] Daily stats for the world during {date}.\n\n"
             "{total_cases} total cases with {active_cases} active cases.\n"
             "{total_deaths} total deaths with {new_deaths} new deaths.\n\n"
             "COVID-19 News:\n{article1}\n{article2}".format(date=current_date.strftime("%m/%d/%Y @ %H:%M PST"),
                                                                                  total_cases=current_world_data["total_cases"],
                                                                                  active_cases=current_world_data["active_cases"],
                                                                                  total_deaths=current_world_data["total_deaths"],
                                                                                  new_deaths=int(current_world_data["new_deaths"]),
                                                                                  article1=articles[0], article2=articles[1]))
    return tweet