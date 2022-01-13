'''
Asteroid Hunter API Pipeline
Author: Dominic DiMarco
main_manual_input.py
Rev. 2.0
Input: NASA API 
Output: .json files as per below function calls:
    asteroid_closest_approach() -> closest_neo.json
    month_closest_approaches(top_month_count, year_to_test, month_to_test) -> closest_neo_per_month.json
    nearest_misses(top_count) -> number_closest_neo.json

*** Modifications on Rev 2.0 ***
-Refactor of testing blocks and data transform methods
-Create user-friendly input/output method on console for custom requests
'''

from api_func.browse_api_func import *
from api_func.feed_api_func import *
from helpers.console_output import *

console_welcome_message()

# User Parameters
try: 
    top_month_count = int(input("Provide # of closest NEO's per month requested: \n"))  
    month_to_test = int(input("Provide month (as a number) for requested NEO's: \n"))     
    year_to_test = int(input("Provide year (as a 4-digit number) for requested NEO's: \n"))   
    top_count = int(input("Provide # of closest NEO's in history requested: \n"))  

except:
    raise Exception("Not a valid entry. Please re-try with valid numbers.\n")

# Function Calls: Uncomment (if present) for accessing functions
asteroid_closest_approach()
nearest_misses(top_count)
month_closest_approaches(top_month_count, year_to_test, month_to_test)