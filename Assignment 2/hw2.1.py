# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 20:47:45 2020
@author: evan.kramer

Team 11
Assignment 2
Jason Hwang and Evan Kramer


"""
# Import required modules
import os
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO

# Concatenate FTP file URL
ftp_url = 'ftp://ftp.cmegroup.com/pub/span/data/cme' 
file_date = '20200904'
file_url = ftp_url + '/cme.' + file_date + '.c.pa2.zip'

# Download file to disk from FTP site, unzip, and extract all parts of the zip file
with urlopen(file_url) as zip_response:
    with ZipFile(BytesIO(zip_response.read())) as zip_file:
        zip_file.extractall('')

# Connect to commodity futures/options input and output files
file_in = open('cme.20200904.c.pa2', mode = 'rt', encoding = 'utf-8')
file_out = open('CL_expirations_and_settlements.txt', mode = 'wt', encoding = 'utf-8')

# Write header records for B files
file_out.write('Futures   Contract   Contract   Futures     Options   Options\n')
file_out.write('Code      Month      Type       Exp Date    Code      Exp Date\n')
file_out.write('-------   --------   --------   --------    -------   --------')

counter = 0 # set counter to write header records for the second table only once
# Write each line
for line in file_in:
    # B records, WTI crude oil futures
    if line[:2] == 'B ' and line[2:5] == 'NYM' and line[5:15].strip() == 'CL' and '202011' <= line[18:24] <= '202312': # make sure the record is in the specified date range and for the correct commodity
        file_out.write('\n' + 
                       line[99:109] + # Futures code
                       (line[18:22] + '-' + line[22:24]).ljust(11, ' ') + # Contract month
                       line[15:18].title().ljust(11, ' ') + # Contract type
                       (line[91:95] + '-' + line[95:97] + '-' + line[97:99]).ljust(12, ' ') + # Futures expiration date
                       ''.ljust(10, ' ') + # Nothing for futures (options)
                       ''.ljust(10, ' ')) # Nothing for futures (options)
    # B records, WTI crude oil options
    elif line[:2] == 'B ' and line[2:5] == 'NYM' and line[5:15].strip() == 'LO' and '202011' <= line[18:24] <= '202312':
        file_out.write('\n' + 
                       line[99:109] + # Futures code
                       (line[18:22] + '-' + line[22:24]).ljust(11, ' ') + # Contract month
                       'Opt'.ljust(11, ' ') + 
                       ''.ljust(12, ' ') + 
                       line[5:15].ljust(10, ' ') + 
                       (line[91:95] + '-' + line[95:97] + '-' + line[97:99]).ljust(12, ' ')) # Futures expiration date
    # 81 records
    elif line[:2] == '81' and line[2:5] == 'NYM' and line[15:25].strip() == 'CL' and line[5:15].strip() in ['CL', 'LO'] and '202011' <= line[29:35] <= '202312' and counter == 0:
        # Write header records if first instance
        file_out.write('\nFutures   Contract   Contract   Strike   Settlement\n')
        file_out.write('Code      Month      Type       Price    Price     \n')
        file_out.write('-------   --------   --------   ------   ----------')
        counter += 1 # iterate 
        
        # Put/call switch
        if line[25:29] == 'OOFC':
            contract_type = 'Call'.ljust(11, ' ')
            strike_price = '{:,.2f}'.format(float(line[47:54]) / 100).ljust(9, ' ')
        elif line[25:29] == 'OOFP':
            contract_type = 'Put'.ljust(11, ' ')
            strike_price = '{:,.2f}'.format(float(line[47:54]) / 100).ljust(9, ' ')
        else:
            contract_type = line[25:29].title().ljust(11, ' ')
            strike_price = ''.ljust(9, ' ')
        
        # Write lines
        file_out.write('\n' + 
                       line[15:25] + # Futures code
                       (line[29:33] + '-' + line[33:35]).ljust(11, ' ') + # Contract month
                       contract_type + # Contract type
                       strike_price + # Strike price
                       '{:,.2f}'.format(float(line[108:122]) / 100).ljust(10, ' ')) # Settlement price
    # 81 records (without header records)
    elif line[:2] == '81' and line[2:5] == 'NYM' and line[15:25].strip() == 'CL' and line[5:15].strip() in ['CL', 'LO'] and '202011' <= line[29:35] <= '202312' and counter >= 1:
        if line[25:29] == 'OOFC':
            contract_type = 'Call'.ljust(11, ' ')
            strike_price = '{:,.2f}'.format(float(line[47:54]) / 100).ljust(9, ' ')
        elif line[25:29] == 'OOFP':
            contract_type = 'Put'.ljust(11, ' ')
            strike_price = '{:,.2f}'.format(float(line[47:54]) / 100).ljust(9, ' ')
        else:
            contract_type = line[25:29].title().ljust(11, ' ')
            strike_price = ''.ljust(9, ' ')
        
        # Write lines
        file_out.write('\n' + 
                       line[15:25] + # Futures code
                       (line[29:33] + '-' + line[33:35]).ljust(11, ' ') + # Contract month
                       contract_type + # Contract type
                       strike_price + # Strike price
                       '{:,.2f}'.format(float(line[108:122]) / 100).ljust(10, ' ')) # Settlement price
    else: 
        pass

# Close file connections
file_in.close()
file_out.close()

# Zip files together
zip_object = ZipFile('Team11_HW2.zip', 'w')
for file in os.listdir():
    if '.zip' in file or '~' in file or 'Archive' in file: # exclude the zip directory, any open files, and the 'Archive' folder
        pass
    else:
        zip_object.write(file)
zip_object.close()