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
import pandas as pd
import requests
import re
import difflib
import os
import datetime
# import target
# import albertsons

# Load data
# TODO: Should this include user-added items?
df = pd.concat([pd.read_csv('albertsons.csv', index_col = 0), 
                pd.read_csv('target.csv', index_col = 0)])
# TODO: Add additional product, price, and grocer data

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

# TODO: Scrape directly from store sites
# Define store to search
print('Forage can help you find the best prices on groceries near there.')

# Search for a product
# TODO: Handle options other than yes/no
# TODO: Accept a list or tuple as input
search_test = False
num_searches = 0
num_items_added = 0
searches = {}
while search_test == False:
    # Initial search
    search = input('What are you looking for?\nYou can also type "All" to get a list of all products or "Common" to get a list of top sellers.\n')
    searches[num_searches] = search 
    dwnld = False
    
    # Return a list of all items
    if search.lower().strip() == 'all':
        print("\nHere's a list of all the products in our database:")
        print(df)
        num_searches += 1
        # Option to download
        download_test = False
        while download_test == False:
            download = input('Do you want to download a copy of these data?\n')
            if download.lower().strip() in ['1', 'True', True, 'y', 'yes']:
                dwnld = True
                df.to_csv('grocery_data.csv')
                print('\nFile downloaded to: ', os.getcwd(), "/grocery_data.csv", sep = "")
                download_test = True
            elif download.lower().strip() in ['0', 'False', False, 'n', 'no']:
                download_test = True
            else:
                print("\nSorry, I didn't get that. Please enter yes or no.")
        
        # Search again? 
        search_again_test = False
        while search_again_test == False: 
            search_again = input("Do you want to search for something else?\n")
            if search_again.lower().strip() in ['1', 'True', True, 'y', 'yes']:
                search_again_test = True
            elif search_again.lower().strip() in ['0', 'False', False, 'n', 'no']:
                search_test, search_again_test = True, True
            else:
                print("\nSorry, I didn't get that. Please enter yes or no.")
                
    # Return a list of common items
    elif search.lower().strip() == 'common': 
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
            add_to_db_test = False
            while add_to_db_test == False:
                add_to_db = input("\nWe didn't find anything. Do you want to add an item to the database?\n")
                if add_to_db.lower().strip() in ['1', 'True', True, 'y', 'yes']:
                    # Add item to database
                    df = add_item_to_db(df)
                    num_items_added += 1
                    add_to_db_test = True
                elif add_to_db.lower().strip() in ['0', 'False', False, 'n', 'no']:
                    add_to_db_test = True
                else: 
                    print("\nSorry, I didn't get that. Please enter yes or no.")
            # Ask to search again
            search_again_test2 = False
            while search_again_test2 == False: 
                search_again = input("Do you want to search again?\n")
                if search_again.lower().strip() in ['1', 'True', True, 'y', 'yes']:
                    search_again_test2 = True
                elif search_again.lower().strip() in ['0', 'False', False, 'n', 'no']:
                    search_test, search_again_test2 = True, True
                else:
                    print("\nSorry, I didn't get that. Please enter yes or no.")
        # Return best match
        else: 
            print("\nHere's what we found:")
            print(pd.merge(pd.DataFrame(best_match, index = range(len(best_match)), 
                                columns = ['product']),
                           df, 
                           how = 'left', on = 'product'))
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
                            df = add_item_to_db(df)
                            num_items_added += 1
                            add_to_db_test = True
                        elif add_to_db.lower().strip() in ['0', 'False', False, 'n', 'no']:
                            add_to_db_test = True
                        else: 
                            pass
                else:
                    print("\nSorry, I didn't get that. Please enter yes or no.")
            # Search again?
            search_again_test3 = False
            while search_again_test3 == False:
                search_again = input("Do you want to search again?\n")
                if search_again.lower().strip() in ['1', 'True', True, 'y', 'yes']:
                    search_again_test3 = True
                elif search_again.lower().strip() in ['0', 'False', False, 'n', 'no']: 
                    search_test, search_again_test3 = True, True
                else:
                    print("\nSorry, I didn't get that. Please enter yes or no.")

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
        (pd.concat([df, 
                    pd.read_csv('grocery_data_additional_items.csv')])
         .drop_duplicates()).to_csv('grocery_data_additional_items.csv', index = False)
    else:
        df.to_csv('grocery_data_additional_items.csv', index = False)
else:
    pass