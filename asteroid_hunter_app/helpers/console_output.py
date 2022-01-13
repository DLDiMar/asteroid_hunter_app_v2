'''
Asteroid Hunter API Pipeline
Author: Dominic DiMarco
console_output.py
Rev. 2.0

Console Output blocks for user verification and manual input guidance

*** Modifications on Rev 2.0 ***
-Refactor of testing blocks and data transform methods
-Create user-friendly input/output method on console for custom requests
'''

# Welcome Message
def console_welcome_message():
    print("Welcome to the NASA API Transform Pipeline.")
    print("This pipeline outputs the closest Near-Earth Objects (NEO's) ever, and closest ones in a given month.")
    print("The pipeline outputs the requested data into .json files for extraction and/or analysis.\n")

#Output Verification Block: page, closest distance
def console_closest_neo(page_api, closest_distance, page_api_closest):
    print('-------')
    print(f'Current page: {page_api}')
    print(f'Closest astronomical distance: {closest_distance}')
    print(f'Closest NEO page: {page_api_closest}')

#Output Verification Block: page, closest distance array
def console_closest_neo_array(page_api, closest_distance_array, page_api_closest):
    print('-------')
    print(f'Current page: {page_api}')
    print(f'Closest astronomical distance array: {closest_distance_array}')
    print(f'Closest NEO page: {page_api_closest}')

# Verify search band for API request
def console_days_and_elements(idx, beginning_day, ending_day, element_count, total_neos_in_month):
    print('-------')
    print(f'First day of week {int(idx) + 1}: {beginning_day}')
    print(f'Last day of week{int(idx) + 1}: {ending_day}')
    print(f'Elements in week {int(idx) + 1}: {element_count}')
    print(f'Total elements so far: {total_neos_in_month}')

# Output Test Block: page, closest distance, index of closest approach
def console_closest_neos_at_dates(date_check, closest_distance_array):
    print('-------')
    print(f'{date_check}')
    print(f'Array of closest Neo distances: {closest_distance_array}')

