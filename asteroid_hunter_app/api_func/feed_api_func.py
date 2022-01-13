'''
Asteroid Hunter API Pipeline
Author: Dominic DiMarco
feed_api_func.py
Rev. 2.0

API Request function for Feed API endpoint of NEOs. 
Input: Raw JSON data, contained by date.
Output: .json file of top number of closest NEOs to Earth 
(via user input of dates and qty per month)

*** Modifications on Rev 2.0 ***
-Refactor of functions from main executable
'''

import math, requests, json, os, sys
from helpers.month_information import *
from helpers.console_output import *
from requests.exceptions import HTTPError
from api_func.apikey import user_api_key
from collections import deque

feed_api = 'https://api.nasa.gov/neo/rest/v1/feed?'
days_per_query = 7    # Max return on Feed API

# Error Function Definition 
def error_block(err):
    print(f"An error occured at: {err}")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

# Get closest number of NEOs to Earth in given month
def month_closest_approaches(top_month_count, year_to_test, month_to_test):
    try:
        # Writing to external JSON file
        file_closest_neo_month = open("closest_neo_per_month.json","w")

        # Initialize default value where first added value will be new closest
        # Initialize arrays for top NEOs and comparison arrays via distance and epoch date
        closest_distance_array = deque([math.inf] * top_month_count) 
        closest_neos_array = deque([None] * top_month_count)
        closest_neos_epoch = deque([None] * top_month_count)  
        total_neos_in_month = 0 
        MonthClass = MonthInfo(year_to_test, month_to_test)

        # Determine number of weeks in month for iteration
        number_weeks_month = math.floor(int(MonthClass.end_day) / days_per_query)

        # Iterate search across all weeks in month
        for idx in range(0,number_weeks_month+1):
            beginning_day = (idx * days_per_query) + 1
            ending_day = (idx * days_per_query) + 7
            if ending_day > int(MonthClass.end_day):
                ending_day = int(MonthClass.end_day)
            if beginning_day > int(MonthClass.end_day):
                break

            # API Get request for each week to get API data
            params = {
                'start_date': f'{year_to_test:04d}-{month_to_test:02d}-{beginning_day:02d}',
                'end_date': f'{year_to_test:04d}-{month_to_test:02d}-{ending_day:02d}',
                'api_key':user_api_key
            }
            response = requests.get(feed_api, params=params).json() 
            response_str = json.dumps(response)
            load_json = json.loads(response_str)  

            # Output for Element Count of NEO's in month
            element_count = int(load_json["element_count"])
            total_neos_in_month += element_count

            console_days_and_elements(idx, beginning_day, ending_day, element_count, total_neos_in_month)

            # Iterate through all NEO's by date
            for date_neo in load_json["near_earth_objects"]:
                date_check = date_neo

                for count, neo_choice in enumerate(load_json["near_earth_objects"][f'{date_check}']):
                    close_approach_data = neo_choice["close_approach_data"]

                    for close_objects in close_approach_data:
                        orbiting_body = str(close_objects["orbiting_body"])
                        epoch_date_close_approach = close_objects["epoch_date_close_approach"]
                        approach_astro_float = float(close_objects["miss_distance"]["astronomical"])

                        # If distance is larger than largest value in current close distance array, skip
                        if (approach_astro_float > max(closest_distance_array)):
                            continue

                        # If current astronomical distance is smaller than smallest stored value, append to first index
                        elif (approach_astro_float < closest_distance_array[0] and orbiting_body == "Earth"):
                            close_neo = load_json["near_earth_objects"][f'{date_check}'][count]
                            close_neo["close_approach_data"] = close_objects
                            closest_neos_array.appendleft(close_neo)
                            closest_neos_array.pop()
                            closest_distance_array.appendleft(approach_astro_float)
                            closest_distance_array.pop()
                            closest_neos_epoch.appendleft(epoch_date_close_approach)
                            closest_neos_epoch.pop()
            
                        
                        # If distance is between values in current close distance array: 
                        # Find where it goes and insert (JSON and distance arrays) and pop off rightmost values
                        elif (approach_astro_float > closest_distance_array[0] and approach_astro_float < max(closest_distance_array) and orbiting_body == "Earth"):
                            for jdx in range(0, len(closest_distance_array)-1):
                                if (approach_astro_float > closest_distance_array[jdx] and (approach_astro_float in closest_distance_array) and (epoch_date_close_approach in closest_neos_epoch)):
                                    continue
                                if (approach_astro_float < closest_distance_array[jdx] and (approach_astro_float not in closest_distance_array) and (epoch_date_close_approach not in closest_neos_epoch)):
                                    closest_neos_array.insert(jdx, close_neo)
                                    closest_neos_array.pop()
                                    closest_distance_array.insert(jdx,approach_astro_float)
                                    closest_distance_array.pop()
                                    closest_neos_epoch.appendleft(epoch_date_close_approach)
                                    closest_neos_epoch.pop()
                console_closest_neos_at_dates(date_check, closest_distance_array)

        # Output JSON to file, then close file
        json.dump(list(closest_neos_array), file_closest_neo_month, indent = 2)
        file_closest_neo_month.close
        print('****End of month_closest_approaches()****')
        
    # Ensure no issues on API site        
    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    # General error handler
    except Exception as err:
        error_block(err)
