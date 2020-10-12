# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 20:55:06 2020
@author: evan.kramer
evankram
shoukanm
oothman
"""
# Set up
import pandas as pd
import numpy as np
import requests
import re

# Load data

# Overview message and enter zip code
print("Welcome to Forage! Let's get started.")
zip_test = False
while zip_test == False:
    zip = input('Please enter your zip code: ')
    # Confirm the first five characters are digits
    if zip[:5].isdigit() == True:
        # Try getting a response from the USPS API
        try:
            xml = '''
            <CityStateLookupRequest USERID="588CMU000141">
            <ZipCode ID='0'>
            <Zip5>99999</Zip5>
            </ZipCode>
            </CityStateLookupRequest>
            '''
            xml = xml.replace('99999', zip[:5]) # replace with first five of zip
            r = 'https://secure.shippingapis.com/ShippingAPI.dll?API=CityStateLookup&XML=' + xml
            city = re.search('<City>(.*?)</City>', requests.post(r).text).group(1).title()
            state = re.search('<State>(.*?)</State>', requests.post(r).text).group(1)
            text = "\nIt looks like you're in " + city + ", " + state + "."
            # confirm_zip = input(text)    
            print(text)
            zip_test = True
        except:
            print("Oops, we couldn't find that zip code.")
    else:
        print("Looks like you've got some non-numeric characters in there.")

# Define store to esarch
print('Forage can help you find the best prices on groceries near there.')


# Search for a product

search = input('What are you looking for? ')
search_test = False
while search_test == False:
    search = search.lower()
    # Was this what you were looking for? 
        # Cool! Do you want to search for something else?
        # Sorry to hear that; do you want to search again?
        # Still not finding it? Want to enter it into our database?
    search_test = True

# Log user data

# Albertsons
# Kroger
# Target


    
    
    
# We couldn't find this product; do you want to add it to our database? 
# Define a class