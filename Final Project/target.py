# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 21:46:30 2020

@author: evan.kramer
evankram
"""
# Scrape data from Target
# Set up
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
driver = webdriver.Chrome('chromedriver.exe')
# products = pd.read_csv('grocerybear.csv')['title'].unique()
products = pd.read_csv('upc.csv', encoding = 'cp1252')['title'].unique()
prices = {}

# Establish connection
driver.get('https://www.target.com/')
time.sleep(3)

# Enter zip code
# driver.find_element_by_class_name('CurrentModality ').click()

# Loop through products
for p in products[:3000]: 
    # Search
    element = driver.find_element_by_id('search')
    element.click()
    element.send_keys(p)
    element.send_keys(Keys.ENTER)
    
    # Find prices
    try: 
        time.sleep(3)
        product = driver.find_elements_by_xpath('.//a[@data-test="product-title"]')[0].text
        price = driver.find_elements_by_xpath('.//span[@class="h-text-bs"]')[0].text
        prices[product] = float(price.replace('$', ''))
    except:
        print("We couldn't find", p)
    
    # Clear search
    try:
        element = driver.find_element_by_id('search')
        element.click()
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.BACKSPACE)
    except:
        driver.refresh()
        time.sleep(3)
        element = driver.find_element_by_id('search')
        element.click()
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.BACKSPACE)

# Output file
driver.close()
df = (pd.DataFrame([prices.keys(), prices.values()])
      .transpose()
      .rename({0:'product', 1:'price'}, axis = 1))
df['grocer'] = 'Target'
df.to_csv('target.csv')