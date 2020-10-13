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
import difflib
import os
import datetime
# import target
# import albertsons

# Load data
df = pd.concat([pd.read_csv('albertsons.csv', index_col = 0), 
                pd.read_csv('target.csv', index_col = 0)])
# TODO: Add additional product, price, and grocer data

# Overview message and enter zip code
print("Welcome to Forage! Let's get started.")
zip_test = False
while zip_test == False:
    zip = input('Please enter your zip code: ')
    # Test: 5 digits
    if len(zip) != 5:
        print("Please enter your 5-digit zip code.")
    # Test: Only digits (no alpha)
    elif zip.isdigit() == False:
        print("Looks like you've got some non-numeric characters in there.")
    # Confirm the first five characters are digits
    # elif len(zip) == 5 and zip.isdigit() == True:
    else:
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
            print("Sorry, we couldn't find that zip code.")

# Define store to search
print('Forage can help you find the best prices on groceries near there.')
# TODO: Scrape directly from store sites

# Search for a product
# TODO: Add a list of 'common' products?
# TODO: Strip quotes from entered text
# TODO: Handle options other than yes/no
# TODO: Accept a list or tuple as input
# TODO: Get all price data to print
# TODO: Log user data
search_test = False
num_searches = 0
searches = {}
while search_test == False:
    # Initial search
    search = input('What are you looking for?\nType the name of the item you want, or type "All" to get a list of all items.\n')
    searches[num_searches] = search
    
    # Return a list of all items
    if search.lower() == 'all':
        print("Here's a list of all the products in our database:")
        print(df)
        num_searches += 1
        # Option to download
        download = input('Do you want to download a copy of these data?\n')
        if download.lower() in ['1', 'True', True, 'y', 'yes']:
            dwnld = True
            df.to_csv('grocery-data.csv')
            print('File downloaded to: ', os.getcwd(), "/grocery-data.csv", sep = "")
        else:
            dwnld = False
        
        # Search again? 
        search_again = input("Do you want to search for something else?\n")
        if search_again.lower() in ['1', 'True', True, 'y', 'yes']:
            pass
        else:
            search_test = True
    
    # Return a list of common items
    elif search.lower() == 'common': 
        # TODO: Add a list of common items
        num_searches += 1
        pass
    
    # Return best match
    else:
        # Find best match
        num_searches += 1
        best_match = difflib.get_close_matches(search, df['product'], cutoff = 0.1)
        # If none, ask whether to search again or add to database
        if len(best_match) == 0: 
            # Ask to add to database
            add_to_db = input("We didn't find anything. Do you want to add an item to the database?\n")
            if add_to_db.lower() in ['1', 'True', True, 'y', 'yes']:
                # TODO: Create class and add to database
                pass
            else: 
                pass
            # Ask to search again
            search_again = input("Do you want to search again?\n")
            if search_again.lower() in ['1', 'True', True, 'y', 'yes']:
                pass
            else:
                search_test = True
        # Return best match
        else: 
            print("\nHere's what we found: ")
            print(pd.merge(pd.DataFrame(best_match, index = range(len(best_match)), 
                                columns = ['product']),
                           df, 
                           how = 'left', on = 'product'))
            # Is that what you were looking for? 
            success = input('\nIs that what you were looking for?\n')
            if success.lower() in ['y', 'yes', '1', 'True', True]:
                print('Great!')
            else:
                # Ask to add to database
                add_to_db = input("Sorry about that. Do you want to add an item to the database?\n")
                if add_to_db.lower() in ['1', 'True', True, 'y', 'yes']:
                    # TODO: Create class and add to database
                    pass
                else: 
                    pass
            # Search again?
            search_again = input("Do you want to search again?\n")
            if search_again.lower() in ['1', 'True', True, 'y', 'yes']:
                pass
            else:
                search_test = True

# Exit program
print('Thanks for using Forage!')

# Log user data
user_log = {'zip': zip, 'city': city, 'state': state, 'num_searches': num_searches,
            'download': dwnld, 'searches': searches, 
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
if 'user_log.csv' not in os.listdir():
    pd.DataFrame(user_log).to_csv('user_log.csv')
else: 
    (pd.concat([pd.read_csv('user_log.csv'), pd.DataFrame(user_log)])
     .to_csv('user_log.csv'))


