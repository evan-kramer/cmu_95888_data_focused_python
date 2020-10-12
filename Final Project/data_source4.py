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
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
driver = webdriver.Chrome('C:/Users/evan.kramer/Documents/CMU/Code/chromedriver.exe')
products = pd.read_csv('data_source3.csv')['title'].unique()
driver.get('https://albertsons.com/')
time.sleep(3)

# Try adjusting zip code
driver.find_element_by_id('openFufillmentModalButton').click()

# Loop through products
for p in products[:5]: 
    # Enter zip code
    
    # Submit search
    element = driver.find_element_by_id('skip-main-content')
    element.click()
    element.send_keys(p)
    element.send_keys(Keys.ENTER)
    
    # Find prices
    try: 
        time.sleep(3)
        print(driver.find_element_by_class_name('product-title').text)
        print(driver.find_element_by_class_name('product-price-con').text)
    except:
        print('There was an error.')
    
    # Clear search
    element = driver.find_element_by_id('skip-main-content')
    element.click()
    element.send_keys(Keys.CONTROL, 'a')
    element.send_keys(Keys.BACKSPACE)
    
# Zip code



'''
bs = BeautifulSoup(urlopen(driver.current_url).read(), 'lxml')
file_out = open('temp.txt', 'wt', encoding = 'utf-8')
file_out.write(str(bs))
file_out.close()
'''

'''
ids = driver.find_elements_by_xpath('//*[@id]')
# ids = driver.find_elements_by_partial_link_text('product')
for i in ids:
    print(i.get_attribute('id'))
    try: 
        driver.find_element_by_id(i.get_attribute('id')).click()
    except:
        pass
'''    
# class='ProductTileFull_price w-100 mt1 header-4 fw-sb gray-20 dfx mb1 justify-center'
# class='ProductTileFull_unitinfo w-100 gray-40 small dfx justify-center '

'''
counter = 1
while counter < 1:
    for i in ids:
        if 'button' in i.get_attribute('id'):
            driver.find_element_by_id(i.get_attribute('id')).click()
            counter += 1
        else:
            pass
'''
    
    
# Click on result
# driver.find_element_by_id('fashion-item-tile-0').click()   
    
# id('searchProductResult)
# id('ProductTileGridView-0') # will need a try/except here in case there are no results
# Loop through products
'''
for p in products:
    # Find search element and search for product
    element = driver.find_element_by_name('search')
    element.send_keys(p)
    # time.sleep(2)
    element.send_keys(Keys.ENTER)
    time.sleep(5)
    
    # product and a product ID
    

    # Get all IDs
    ids = driver.find_elements_by_xpath('//*[@id]')
    counter = 0
    while counter < 1:
        for i in ids:
            if 'button' in i.get_attribute('id'):
                counter += 1
                element2 = driver.find_element_by_id('//' + i.get_attribute('id'))
                element2.click()
                time.sleep(5)
            else:
                pass
                
    # See what's in the content element? 

    # See what the IDs are now?
    ids = driver.find_elements_by_xpath('//*[@id]')
    for i in ids:
        print(i.get_attribute('id'))    # id name as stringelement2 = driver.find_element_by_id('result')
    '''