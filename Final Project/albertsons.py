# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 21:46:30 2020

@author: evan.kramer
evankram
"""
# Scrape data from Grocery Bear
# Set up
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time
driver = webdriver.Chrome('chromedriver.exe')
products = pd.read_csv('grocerybear.csv')['title'].unique()
prices = {}

# Enter zip code
# driver.find_element_by_id('openFulfillmentModalButton').click()

# Loop through products
# Albertsons
driver.get('https://albertsons.com/')
time.sleep(3)
for p in products: 
    # Search
    element = driver.find_element_by_id('skip-main-content')
    element.click()
    element.send_keys(p)
    element.send_keys(Keys.ENTER)
    
    # Find prices
    try: 
        time.sleep(3)
        product = driver.find_element_by_class_name('product-title').text
        price = driver.find_element_by_class_name('product-price-con').text
        prices[product] = float(re.search('\$(.*?) /', price).group(1))
    except:
        print("We couldn't find", p)
    
    # Clear search
    element = driver.find_element_by_id('skip-main-content')
    element.click()
    element.send_keys(Keys.CONTROL, 'a')
    element.send_keys(Keys.BACKSPACE)

# Output file
driver.close()
df = (pd.DataFrame([prices.keys(), prices.values()])
      .transpose()
      .rename({0:'product', 1:'price'}, axis = 1))
df['grocer'] = 'Albertsons'
df.to_csv('albertsons.csv')