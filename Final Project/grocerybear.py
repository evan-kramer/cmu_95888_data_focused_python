# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 21:46:30 2020

@author: evan.kramer
"""
# Scrape data from Grocery Bear
# Set up
import requests
import pandas as pd
import re
keys = open('keys.txt').readlines()
gb_key = re.search('GROCERYBEAR: (.*?)$', keys[1]).group(1)
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
    'api-key': gb_key,
    'Content-Type': 'application/json',
}
data = '{"city":"all", "product":"bread", "num_days":0}' # can get all data with "num_days":0
response = requests.post('https://grocerybear.com/getitems', headers = headers, data = data)

# Loop through all products
df = pd.DataFrame() # initial'ize empty dataframe

for p in products:
    data = '{"city":"all", "product":"' + p + '", "num_days":0}'
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

items = df.title.unique()

# Merge with UPCs and output file
(pd.merge(pd.read_csv('upc_lookup.csv')[['title', 'upc']].drop_duplicates(),
          df, how = 'right', on = 'title')
 .to_csv('grocerybear.csv', index = False))