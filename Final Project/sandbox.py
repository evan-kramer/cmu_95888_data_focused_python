# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 20:55:06 2020

@author: evan.kramer
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 15:22:31 2020

@author: maosk
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
# import csv
import xlsxwriter
with xlsxwriter.Workbook('data.xlsx') as workbook:
# fout = open('detail2.txt','wt',encoding='utf-8')
# raw_excel = csv.writer(open("output.csv", "w"))
# clean_excel = csv.writer(open("clean_output.csv", "w"))
    clean = workbook.add_worksheet("clean")
    raw = workbook.add_worksheet("raw")
    clean.write(0, 0, 'name')
    clean.write(0, 1, 'gtin13')
    clean.write(0, 2, 'price')
    # clean_excel.write(0,0,"name")
    # clean_excel.write(1,0,"gtin13")
    # clean_excel.write(2,0,"price")
    for i in range(1,2):#there are 21 pages in juice and here is one
        html = urlopen('https://www.safeway.com/shop/aisles/beverages/juice-smoothies.3132.html?sort=&page='+str(i))
        bsyc = BeautifulSoup(html.read(),'lxml')
        # fout = open('bsyc_temp.txt','wt',encoding='utf-8')
        # fout.write(str(bsyc))
        # fout.close()
        count = 0
        product_list = bsyc.findAll('h3')
        for i in range(len(product_list)):
            for c in product_list[i].children:
                c = str(c)
                webpage = re.search("href=\"\/(.*?)\" id",c)
                if webpage:
                    webpage = webpage.group(1)
                    product_detail = "https://www.safeway.com/" + webpage
                    count+=1
                    # fout.write(product_detail+"\n")
                    detail_html = urlopen(product_detail)
                    detail_bsyc = BeautifulSoup(detail_html.read(),'lxml')
                    s = detail_bsyc.find('script', type="application/ld+json")
                    item_info = json.loads(s.string)
                    # print(item_info)
                    price = {"price":item_info["offers"]["price"]}
                    raw_info = {key: item_info[key] for key in item_info.keys() 
                                       & {'gtin13','name','@context','@type','description'}}
                    raw_info.update(price)
                    for i,(key, val) in enumerate(raw_info.items(), start=1):
                        raw.write(count, i-1, val)
                    # print(item_info)
                    # for key, val in item_info.items():
                    #     raw_excel.writerow([key, val])
                    
                    clean_info = {key: item_info[key] for key in item_info.keys() 
                                       & {'gtin13','name'}}
                    clean_info.update(price)
                    # for data in clean_info:
                    #     clean_excel.writerow(data)
                    for i,(key, val) in enumerate(clean_info.items(), start=1):
                        clean.write(count, i-1, val)
print("job done")
# fout.close()
# clean_excel.close()
# raw_excel.close()
# print(len(product_list))