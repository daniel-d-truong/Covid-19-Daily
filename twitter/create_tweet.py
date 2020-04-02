from data import *
from datetime import datetime

def format_tweet():
    articles = getTopHeadlines()
    relevant_data = getCovidWorldData()
    current_date = datetime.now()

    current_world_data = getCovidWorldData()
    tweet = ("Daily stats for the world during {date}.\n\n"
             "{total_cases} total cases with {active_cases} active cases.\n"
             "{total_deaths} total deaths with {new_deaths} new deaths.\n".format(date=current_date.strftime("%m/%d/%Y @ %H:%M PST"),
                                                                                  total_cases=current_world_data["total_cases"],
                                                                                  active_cases=current_world_data["active_cases"],
                                                                                  total_deaths=current_world_data["total_deaths"],
                                                                                  new_deaths=current_world_data["new_deaths"]))
    return tweet