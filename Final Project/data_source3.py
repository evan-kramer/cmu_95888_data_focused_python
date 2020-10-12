# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 21:46:30 2020

@author: evan.kramer
"""
# Scrape data from Grocery Bear
# Set up
import requests
import pandas as pd
cities = ['all',
                'Boise',
                'DC', # [Washington, DC]
                'Honolulu',
                'Houston',
                'LA',
                'LV', # [Las Vegas]
                'Phoenix', 
                'Portland', # Oregon, presumably
                'Seattle',
                'SF' # [San Francisco]
                ]
products = ['eggs', 'milk', 'bread', 'oj', 'rice', 'steak', 'butter'] # oj = orange juice

# Send request, with help from this URL: https://curl.trillworks.com/#python
headers = {
    'api-key': 'DD3BE1039406F4DE66D315170A27ED8A03083F3E5A0F8CF697A8993448BE3C54',
    'Content-Type': 'application/json',
}
data = '{"city":"all", "product":"bread", "num_days":0}' # can get all data with "num_days":0
response = requests.post('https://grocerybear.com/getitems', headers = headers, data = data)





# Loop through all products
df = pd.DataFrame() # initial'ize empty dataframe

for p in products:
    data = '{"city":"all", "product":"' + p + '", "num_days":1}'
    try: 
        response = requests.post('https://grocerybear.com/getitems', 
                                 headers = headers, data = data)
        if response.ok == True:
            r = response.json()
            for i in range(len(r)):
                # Append data
                df = pd.concat([df, pd.DataFrame(r[i], index = range(4))])
        else:
            print(response.reason)
    except: 
        print(response.reason)

# Clean data a bit more (i.e., split on '-')
df[['title', 'quantity']] = df.title.str.split('-', n = 2, expand = True)
for c in ['title', 'quantity']:
    df[c] = df[c].str.strip()

# Will need to look up UPCs here: https://www.barcodelookup.com/
items = df.title.unique()
# 9l43b331lyfk9x79wbgshy2c3hfjnp
# https://api.barcodelookup.com/v2/products?search=GPS%20Navigation%20System&formatted=y&key=9l43b331lyfk9x79wbgshy2c3hfjnp

# Merge with UPCs and output file
(pd.merge(pd.read_csv('upc_lookup.csv')[['title', 'upc']].drop_duplicates(),
          df, how = 'right', on = 'title')
 .to_csv('data_source3.csv', index = False))

# Output file
