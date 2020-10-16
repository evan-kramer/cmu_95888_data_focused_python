# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 20:55:06 2020
@author: evan.kramer
Evan Kramer
evankram
Shoukang Mao
shoukanm
Omar Othman
oothman
"""
# Set up
import numpy as np
import pandas as pd
import requests
import re
import difflib
import os
import datetime
import matplotlib.pyplot as plt
# import albertsons
# import target

# TODO: Visualizations (perhaps grocery store locations near zip code entered? Or counts by category?)
# TODO: Use NumPy
# TODO: Add summary statistics

# Load grocery data and set global objects
# Note: Will not include user-added items for now
grocery_data = pd.concat([pd.read_csv('albertsons.csv', index_col = 0), 
                          pd.read_csv('target.csv', index_col = 0)])
search_test, dwnld = False, False
num_searches = 0
num_items_added = 0
searches = {}
keys = open('keys.txt').readlines()
usps_key = re.search('USPS: (.*?)$', keys[0]).group(1)

# Define functions
# Add to database
def add_item_to_db(dataframe):
    # Product name
    db_product = input("What is the name of the product you want to add?\n").title().strip()
    # Price (and try to convert to float)
    price_test = False
    while price_test == False:
        db_price = input("How much does it cost?\n").strip()
        try:
            db_price = float(db_price)
            price_test = True
        except:
            print("\nMake sure you enter only numbers and a decimal point.")
    # Grocer name
    db_grocer = input("In which store did you find this price?\n").title().strip()
    # Add to database
    output = {'product': db_product, 'price': db_price, 'grocer': db_grocer}
    dataframe = dataframe.append(pd.DataFrame(output, index = [len(dataframe)]))
    return dataframe
# Download data
def download_data(dataframe, filename):
    download_test = False
    while download_test == False:
        download = input('Do you want to download a copy of these data?\n')
        if download.lower().strip() in ['1', 'True', True, 'y', 'yes']:
            dwnld = True
            dataframe.to_csv(filename, index = False)
            print('\nFile downloaded to: ', os.getcwd(), "/", filename, sep = "")
            download_test = True
        elif download.lower().strip() in ['0', 'False', False, 'n', 'no']:
            download_test = True
        else:
            print("\nSorry, I didn't get that. Please enter yes or no.")
# Search again
def search_again():
    search_test, search_again_test = False, False
    while search_again_test == False: 
        search_again = input("Do you want to search for something else?\n")
        if search_again.lower().strip() in ['1', 'True', True, 'y', 'yes']:
            search_again_test = True
        elif search_again.lower().strip() in ['0', 'False', False, 'n', 'no']:
            search_test, search_again_test = True, True
        else:
            print("\nSorry, I didn't get that. Please enter yes or no.")
    return search_test

# Overview message and enter zip code
print("Welcome to Forage! Let's get started.")
zip_test = False
while zip_test == False:
    zip = input('Please enter your zip code.\n')
    # Test: 5 digits
    if len(zip) != 5:
        print("Please enter your 5-digit zip code.")
    # Test: Only digits (no alpha)
    elif zip.isdigit() == False:
        print("Looks like you've got some non-numeric characters in there.")
    # 5 digits
    else:
        # Try getting a response from the USPS API
        try:
            xml = '''
            <CityStateLookupRequest USERID="{api_key}">
            <ZipCode ID='0'>
            <Zip5>{zip}</Zip5>
            </ZipCode>
            </CityStateLookupRequest>
            '''
            xml = xml.format(api_key = usps_key, zip = str(zip[:5])) # replace with first five of zip
            r = 'https://secure.shippingapis.com/ShippingAPI.dll?API=CityStateLookup&XML=' + xml
            city = re.search('<City>(.*?)</City>', requests.post(r).text).group(1).title()
            state = re.search('<State>(.*?)</State>', requests.post(r).text).group(1)
            text = "\nIt looks like you're in " + city + ", " + state + "."
            # confirm_zip = input(text)    
            print(text)
            zip_test = True
        # Otherwise try again
        except:
            print("Sorry, we couldn't find that zip code.")

# TODO: Scrape directly from store sites
# Define store to search
print('Forage can help you find the best prices on groceries near there.')

# Search for a product
# TODO: Handle options other than yes/no
# TODO: Accept a list or tuple as input
while search_test == False:
    # Initial search
    print("\nEnter the name of a product you're looking for.")
    search = input("You can also type \"All\" to get a list of all products, \"Common\" to get a list of top sellers, or \"Summary\" to summarize the data.\n")
    searches[num_searches] = search 
    best_match = difflib.get_close_matches(search, grocery_data['product'], cutoff = 0.3)
    literal_match = grocery_data[grocery_data['product'].str.lower().str.contains(search.lower().strip())]
    
    # Return a list of all items
    if search.lower().strip() == 'all':
        print("\nHere's a list of all the products in our database:")
        print(grocery_data)
        num_searches += 1
        # Option to download
        download_data(grocery_data, 'grocery_data.csv')
        # Search again? 
        search_test = search_again()
             
    # Return a list of common items
    elif search.lower().strip() == 'common': 
        # Return a list of common items by reading the search results of user_log
        # If no user_log: eggs, milk, bread, rice, butter, steak, orange juice
        num_searches += 1
        print("\nHere's what we found:")
        if 'user_log.csv' not in os.listdir() or len(best_match) == 0: 
            common_items = (pd.concat([grocery_data[(grocery_data['product'].str.lower().str.contains('eggs'))],
                                       grocery_data[grocery_data['product'].str.lower().str.contains('milk')],
                                       grocery_data[grocery_data['product'].str.lower().str.contains('bread')],
                                       grocery_data[grocery_data['product'].str.lower().str.contains('rice')],
                                       grocery_data[grocery_data['product'].str.lower().str.contains('butter')],
                                       grocery_data[grocery_data['product'].str.lower().str.contains('steak')],
                                       grocery_data[grocery_data['product'].str.lower().str.contains('orange juice')]]))
            print(common_items)
        else:
            common_items = ((pd.merge(pd.DataFrame(best_match, index = range(len(best_match)), 
                                                   columns = ['product']),
                                      grocery_data, 
                                      how = 'left', on = 'product')
                             .append(literal_match)))
            print(common_items)
        # Option to download
        download_data(common_items, 'common_items.csv')
        # Search again? 
        search_test = search_again()
        
    # TODO: Return visualizations and summary statistics
    elif search.lower().strip() == 'summary':
        print(grocery_data.describe())
        plt.hist(grocery_data['price'])
        plt.show()
        
    # Return best match
    else:
        # Find best match looking for literal matches and string distances
        num_searches += 1
        # Does the item appear in any entry? 
        # If none, ask whether to search again or add to database
        if len(best_match) == 0: 
            # Ask to add to database
            print("\nHm, we didn't find anything.")
            add_to_db_test = False
            while add_to_db_test == False:
                add_to_db = input("Do you want to add an item to the database?\n")
                if add_to_db.lower().strip() in ['1', 'True', True, 'y', 'yes']:
                    # Add item to database
                    grocery_data = add_item_to_db(grocery_data)
                    num_items_added += 1
                    add_to_db_test = True
                elif add_to_db.lower().strip() in ['0', 'False', False, 'n', 'no']:
                    add_to_db_test = True
                else: 
                    print("\nSorry, I didn't get that. Please enter yes or no.")
            # Ask to search again
            search_test = search_again()
            
        # Return best match
        else: 
            print("\nHere's what we found:")
            print((pd.merge(pd.DataFrame(best_match, index = range(len(best_match)), 
                                         columns = ['product']),
                            grocery_data, 
                            how = 'left', on = 'product')
                   .append(literal_match)))
            # Is that what you were looking for? 
            success_test = False
            while success_test == False:
                success = input('Is that what you were looking for?\n')
                if success.lower().strip() in ['y', 'yes', '1', 'True', True]:
                    print('Great!')
                    success_test = True
                # Ask to add to database
                elif success.lower().strip() in ['n', 'no', '0', 'False', False]:
                    success_test = True
                    add_to_db_test = False
                    while add_to_db_test == False:
                        add_to_db = input("Sorry about that. Do you want to add an item to the database?\n")
                        if add_to_db.lower().strip() in ['1', 'True', True, 'y', 'yes']:
                            # Add item to database
                            grocery_data = add_item_to_db(grocery_data)
                            num_items_added += 1
                            add_to_db_test = True
                        elif add_to_db.lower().strip() in ['0', 'False', False, 'n', 'no']:
                            add_to_db_test = True
                        else: 
                            pass
                else:
                    print("\nSorry, I didn't get that. Please enter yes or no.")
            # Search again?
            search_test = search_again()

# Exit program
print('\nThanks for using Forage!')

# Log user data 
user_log = {'zip': zip, 'city': city, 'state': state, 'num_searches': num_searches,
            'num_items_added': num_items_added, 'download': dwnld, 'searches': searches, 
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
if 'user_log.csv' not in os.listdir():
    pd.DataFrame(user_log).to_csv('user_log.csv', index = False)
else: 
    (pd.concat([pd.read_csv('user_log.csv'), pd.DataFrame(user_log)])
     .to_csv('user_log.csv', index = False))

# Output new items added
if num_items_added > 0:
    if 'grocery_data_additional_items.csv' in os.listdir():
        (pd.concat([grocery_data, 
                    pd.read_csv('grocery_data_additional_items.csv')])
         .drop_duplicates()).to_csv('grocery_data_additional_items.csv', index = False)
    else:
        grocery_data.to_csv('grocery_data_additional_items.csv', index = False)
else:
    pass