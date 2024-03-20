
from promptflow import tool
import requests
import json
from datetime import datetime


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def call_api(user_intent: str) -> dict:
    # using the json in format
    #{
    #    latitude: 0,
    #    longitude: 0,
    #    start_date='',
    #    end_date='',
    #    temperature_unit: ''
    #}
    # call the weather api which looks like this
    # https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2024-02-27&end_date=2024-03-12&hourly=temperature_2m&temperature_unit=fahrenheit
    # and return the response

    # anything from the LLM is a string so load the JSON
    user_intent_dict = json.loads(user_intent)
    request_date = datetime.strptime(user_intent_dict['start_date'], '%Y-%m-%d')
    base_uri = "https://api.open-meteo.com/v1/forecast"

    if ( datetime.now() - request_date ).days > 1:
        # historical
        base_uri = "https://archive-api.open-meteo.com/v1/archive"


    url = f"{base_uri}?latitude={user_intent_dict['latitude']}&longitude={user_intent_dict['longitude']}&start_date={user_intent_dict['start_date']}&end_date={user_intent_dict['end_date']}&hourly=temperature_2m&temperature_unit={user_intent_dict['temperature_unit']}"
    
    print("full_url: ", url)
    return requests.get(url).json()