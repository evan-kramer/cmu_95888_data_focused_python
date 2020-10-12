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
import re
import time
driver = webdriver.Chrome('C:/Users/evan.kramer/Documents/CMU/Code/chromedriver.exe')
products = pd.read_csv('grocerybear.csv')['title'].unique()
prices = {}

# Establish connection
driver.get('https://www.target.com/')
time.sleep(3)

# Enter zip code
# driver.find_element_by_class_name('CurrentModality ').click()

# Loop through products
for p in products: 
    # Search
    element = driver.find_element_by_id('search')
    element.click()
    element.send_keys(p)
    element.send_keys(Keys.ENTER)
    
    # Find prices
    try: 
        time.sleep(3)
        # product2 = driver.find_element_by_class_name('h-display-flex').text
        product = driver.find_elements_by_xpath('.//a[@data-test="product-title"]')[0].text
        price = driver.find_elements_by_xpath('.//span[@class="h-text-bs"]')[0].text
        prices[product] = price
        # print("Product:", product)
        # print("Product2:", product2)
        # print("Price:", price)
    except:
        print("We couldn't find", p)
    
    # Clear search
    element = driver.find_element_by_id('search')
    element.click()
    element.send_keys(Keys.CONTROL, 'a')
    element.send_keys(Keys.BACKSPACE)

driver.close()
print(prices)
df = pd.DataFrame([prices.keys(), prices.values()]).transpose()
df.to_csv('target.csv')