'''
Asteroid Hunter API Pipeline
Author: Dominic DiMarco
test_asteroid_hunter_app.py
Rev. 2.0

Unit Testing at requests and helper functions

*** Modifications on Rev 2.0 ***
-Refactor of testing blocks and data transform methods
'''

import json, math, requests
from asteroid_hunter_app.api_func import apikey
from asteroid_hunter_app.helpers.month_information import MonthInfo
from asteroid_hunter_app import __version__, main_manual_input


def test_version():
    assert __version__ == '0.1.0'

def test_near_misses():
    # Test JSON type output of functions
    assert type(main_manual_input.nearest_misses()) == json
    assert type(main_manual_input.asteroid_closest_approach()) == json
    assert type(main_manual_input.month_closest_approaches()) == json

    # Test HTTP Request statuses of API's
    params = {
        'api_key':apikey.user_api_key
    }
    assert (requests.get(main_manual_input.browse_api, params=params)).status_code ==  200
    assert (requests.get(main_manual_input.feed_api, params=params)).status_code == 200

    responseStr = json.dumps(requests.get(main_manual_input.browse_api, params=params).json())
    loadJson = json.loads(responseStr)
    numberPages = loadJson["page"]["size"]  
    assert (numberPages) == 20

    # Test Output JSON file for asteroid_closest_approach()
    fileOpen1 = open('closest_neo.json') 
    loadJsonOutput1 = json.load(fileOpen1)
    assert(loadJsonOutput1["id"]) == "2099942"

    # Test Output JSON file for nearest_misses()
    fileOpen2 = open('ten_closest_neo.json')
    loadJsonOutput2 = json.load(fileOpen2)
    assert(loadJsonOutput2[0]["id"]) == "2099942"

    # Test Month Information Class parameters and methods
    monthTest1 = MonthInfo(2021, 1)
    assert (monthTest1.start_date) == 1
    assert (monthTest1.end_date) == 31
    assert (monthTest1.days_in_month()) == 31
    numberWeeksMonth1 = math.floor(int(monthTest1.end_day) / main_manual_input.days_per_query)
    assert (numberWeeksMonth1) == 5

    monthTest2 = MonthInfo(2021, 2)
    assert (monthTest2.end_date) == 28
    assert (monthTest2.days_in_month()) == 28
    numberWeeksMonth2 = math.floor(int(monthTest2.end_day) / main_manual_input.days_per_query)
    assert (numberWeeksMonth2) == 4

    monthTest3 = MonthInfo(2020, 2)
    assert (monthTest3.end_date) == 29
    assert (monthTest3.days_in_month()) == 29
    numberWeeksMonth3 = math.floor(int(monthTest3.end_day) / main_manual_input.days_per_query)
    assert (numberWeeksMonth3) == 5