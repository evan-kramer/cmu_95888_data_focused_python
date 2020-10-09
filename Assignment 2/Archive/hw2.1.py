# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 20:47:45 2020

@author: evan.kramer
"""

# Set up
import os
os.chdir("C:/Users/evan.kramer/Documents/CMU/Courses/2020-03/95888 - Data Focused Python/Assignments/Assignment 2")

# Connect to commodity futures 
date = '20200904'
url = 'ftp://ftp.cmegroup.com/pub/span/data/cme'
file_in = open('cme.20200904.c.pa2', mode = 'rt', encoding = 'utf-8')
file_out1 = open('CL_expirations_and_settlements1.txt', mode = 'wt', encoding = 'utf-8')
file_out2 = open('CL_expirations_and_settlements2.txt', mode = 'wt', encoding = 'utf-8')

# Write header records for each file
file_out1.write('Futures   Contract   Contract   Futures     Options   Options\n')
file_out1.write('Code      Month      Type       Exp Date    Code      Exp Date\n')
file_out1.write('-------   --------   --------   --------    -------   --------\n')
# Need to write these header records for the second file, too
file_out2.write('Futures   Contract   Contract   Strike   Settlement\n')
file_out2.write('Code      Month      Type       Price    Price     \n')
file_out2.write('-------   --------   --------   ------   ----------\n')

# Write lines
for line in file_in:
    # Parse based on record id
    # B records
    if line[:2] == 'B ':
        futures_code = line[99:109]
        contract_month = line[18:22] + '-' + line[22:24] # must be between 2020-11 and 2023-12
        contract_type = line[15:18].title()
        if contract_type == 'Fut':
            futures_exp_date = line[91:95] + '-' + line[95:97] + '-' + line[97:99]
            options_exp_date = ''
            options_code = ''
        else:
            futures_exp_date = ''
            options_exp_date = line[91:95] + '-' + line[95:97] + '-' + line[97:99]
            options_code = line[5:15]
        # Do not include contract months earlier than 2020-11 or later than 2023-12
        if futures_code.strip() == 'CL' and options_code.strip() in ['', 'LO'] and '2020-11' <= contract_month <= '2023-12':
            file_out1.write(futures_code + 
                       contract_month.ljust(11, ' ') + 
                       contract_type.ljust(11, ' ') + 
                       futures_exp_date.ljust(12, ' ') + 
                       options_code.ljust(10, ' ' ) + 
                       options_exp_date.ljust(10, ' ') + 
                       '\n')
    elif line[:2] == '81':
        futures_code = line[15:25]
        contract_month = line[29:33] + '-' + line[33:35]
        contract_type = line[25:29].title()
        strike_price = '{:,.2f}'.format(float(line[47:54]) / 100) # divide by 10000?
        settlement_price = '{:,.2f}'.format(float(line[108:122]) / 100) # divide by 10000?
        if contract_type == "Oofp":
            contract_type = "Put"
        elif contract_type == "Oofc":
            contract_type = "Call"
        else:
            strike_price = ''
        
        # Add an if condition for Fut vs. Put/Call and to filter dates
        if futures_code.strip() == 'CL' and '2020-11' <= contract_month <= '2023-12':
            file_out2.write(futures_code + 
                           contract_month.ljust(11, ' ') + 
                           contract_type.ljust(11, ' ') + 
                           strike_price.ljust(9, ' ') + 
                           settlement_price.ljust(10, ' ') + 
                           '\n')
   
# Close file connections
file_in.close()
file_out1.close()
file_out2.close()

# Reopen and combine two separate files I created
for file in ['CL_expirations_and_settlements1.txt', 'CL_expirations_and_settlements2.txt']:
    open('CL_expirations_and_settlements.txt', mode = 'w', encoding = 'utf-8').close()
    file_in = open(file, mode = 'rt', encoding = 'utf-8')
    file_out = open('CL_expirations_and_settlements.txt', mode = 'a+', encoding = 'utf-8')
    for line in file_in:
        file_out.write(line)
    file_in.close()
    os.remove(file) # remove file from disk
file_out.close()

# Zip files together
from zipfile import ZipFile
zip_object = ZipFile('Team11_HW2.zip', 'w')
for file in os.listdir():
    if '.zip' in file or '~' in file:
        pass
    else:
        zip_object.write(file)
zip_object.close()
