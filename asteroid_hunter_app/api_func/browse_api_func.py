'''
Asteroid Hunter API Pipeline
Author: Dominic DiMarco
browse_api_func.py
Rev. 2.0

API Request function for Browse API endpoint of NEOs. 
Input: Raw JSON data, contained by each NEO.
Output: .json files of top number of closest NEO(s) to Earth 
(via user input of qty)

*** Modifications on Rev 2.0 ***
-Refactor of functions from main executable
'''

import math, requests, json, os, sys
from helpers.console_output import *
from requests.exceptions import HTTPError
from api_func.apikey import user_api_key
from collections import deque

browse_api = 'https://api.nasa.gov/neo/rest/v1/neo/browse?'

# Error Function Definition 
def error_block(err):
    print(f"An error occured at: {err}")
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

# Get all asteroids and determine NEO with closest approach to Earth
def asteroid_closest_approach():
    try:
        closest_distance = math.inf      # Start default value where first added value will be new closest
        page_api = 0                     # API page start at 0
        page_api_closest = 0             # Page of closest NEO JSON Object

        # Write to external JSON file 
        file_closest_neo = open("closest_neo.json","w")

        # Get request to API for number of pages to loop through
        params = {
            'api_key':user_api_key
        }
        response = requests.get(browse_api, params=params).json() 
        response_str = json.dumps(response)
        load_json = json.loads(response_str)
        number_pages = load_json["page"]["size"]  # Extract available API pages

        # Iterate search across all API pages
        for page_api in range(0,number_pages+1):

            # API request for each page
            params = {
                'page':page_api,
                'api_key':user_api_key
            }
            response_per_page = requests.get(browse_api, params=params).json() 
            response_str_per_page = json.dumps(response_per_page)
            load_json_per_page = json.loads(response_str_per_page)

            # Iterate through all NEO's 
            for count, neo in enumerate(load_json_per_page["near_earth_objects"]):
                close_approach_data = neo["close_approach_data"]
                
                # Iterate through each NEO's close approach data
                for close_objects in close_approach_data:  
                    # Filtering parameters       
                    orbiting_body = close_objects["orbiting_body"]
                    approach_astro_float = float(close_objects["miss_distance"]["astronomical"])

                    # If NEO's closest approach is closer than previous, replace holder data and JSON output
                    if (approach_astro_float < closest_distance and orbiting_body == "Earth"):
                        closest_neo = load_json_per_page["near_earth_objects"][count]
                        closest_distance = approach_astro_float
                        page_api_closest = page_api
                        closest_neo["close_approach_data"] = close_objects
            console_closest_neo(page_api, closest_distance, page_api_closest)

        # Output JSON to file, then close file
        json.dump(closest_neo, file_closest_neo, indent = 2)
        file_closest_neo.close
        print('****End of asteroid_closest_approach()****')

    # Ensure no issues on API site
    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    # General error handler
    except Exception as err:
        error_block(err)

# Get top 10 nearest misses to Earth (past and future)
def nearest_misses(top_count):
    try:
        # Initialize default value where first added value will be new closest
        # Initialize arrays for top NEOs and comparison arrays via distance and epoch date
        closest_distance_array = deque([math.inf] * top_count)      
        closest_neos_array = deque([None] * top_count)
        closest_neos_epoch = deque([None] * top_count)
        page_api = 0                      # API page start at 0
        page_api_closest = 0              # Page of closest NEO JSON Object

        # Writing to external JSON file for extraction
        file_number_closest_neo = open("number_closest_neo.json","w")

        # API Get request for number of pages to loop
        params = {
            'api_key':user_api_key
        }
        response = requests.get(browse_api, params=params).json() 
        response_str = json.dumps(response)      
        load_json = json.loads(response_str)
        number_pages = load_json["page"]["size"]  # Extract available API pages

        # Iterate search across all API pages
        for page_api in range(0,number_pages+1):

            # API request for each page
            params = {
                'page':page_api,
                'api_key':user_api_key
            }
            response_per_page = requests.get(browse_api, params=params).json() 
            response_str_per_page = json.dumps(response_per_page)
            load_json_per_page = json.loads(response_str_per_page)

            # Iterate through NEO's
            for count, neo in enumerate(load_json_per_page["near_earth_objects"]):
                close_approach_data = neo["close_approach_data"]
                
                # Iterate through NEO's close approach data
                for close_objects in close_approach_data:
                    # Filtering parameters
                    orbiting_body = close_objects["orbiting_body"]
                    epoch_date_close_approach = close_objects["epoch_date_close_approach"]
                    approach_astro_float = float(close_objects["miss_distance"]["astronomical"])

                    # If current astronomical distance is larger than largest stored value, skip
                    if (approach_astro_float > max(closest_distance_array)):
                        continue
                    
                    # If current astronomical distance is smaller than smallest stored value, append to first index
                    elif (approach_astro_float < closest_distance_array[0] and orbiting_body == "Earth" ):
                        closest_neo = load_json_per_page["near_earth_objects"][count]
                        closest_neo["close_approach_data"] = close_objects
                        closest_distance_array.appendleft(approach_astro_float)
                        closest_distance_array.pop()
                        closest_neos_array.appendleft(closest_neo)
                        closest_neos_array.pop()
                        closest_neos_epoch.appendleft(epoch_date_close_approach)
                        closest_neos_epoch.pop()
                        page_api_closest = page_api

                    # If distance is between values in current close distance array: 
                    # Find where it goes and insert (JSON and distance arrays) and pop off rightmost values
                    elif (approach_astro_float > closest_distance_array[0] and approach_astro_float < max(closest_distance_array) and orbiting_body == "Earth"):
                        for jdx in range(0, len(closest_distance_array)-1):
                            if (approach_astro_float > closest_distance_array[jdx] and (approach_astro_float in closest_distance_array) and (epoch_date_close_approach in closest_neos_epoch)):
                                continue
                            if (approach_astro_float < closest_distance_array[jdx] and (approach_astro_float not in closest_distance_array) and (epoch_date_close_approach not in closest_neos_epoch)):
                                closest_neos_array.insert(jdx, closest_neo)
                                closest_neos_array.pop()
                                closest_distance_array.insert(jdx,approach_astro_float)
                                closest_distance_array.pop()
                                closest_neos_epoch.appendleft(epoch_date_close_approach)
                                closest_neos_epoch.pop()

            console_closest_neo_array(page_api, closest_distance_array, page_api_closest)

        # Output JSON to file, then close file
        json.dump(list(closest_neos_array), file_number_closest_neo, indent = 2)
        file_number_closest_neo.close
        print('****End of nearest_misses()****')

    # Ensure no issues on API site
    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    # General error handler
    except Exception as err:
        error_block(err)