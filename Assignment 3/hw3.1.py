# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 12:40:47 2020

@author: evan.kramer

Team 12
Evan Kramer
evankram

Chase Pasciuto
cpasciut
"""

team = '12'; hw = '3'
zipfilename = 'Team' + team + '_HW' + hw + '.zip'

# 1: Lists, Tuples, Sets, Dicts, and Comprehensions
# 1a: Create a Python script file named hw3.1.py. 
# Connect to files
file_in = open('expenses.txt', mode = 'rt', encoding = 'utf-8')

# In this script, define an empty list named records, then read the lines from expenses.txt and append each line (excluding its terminating newline character) to the records list. # Add code to display the lines from records
records = []
for line in file_in: 
    records.append(line.replace('\n', '')) # Confirm that the output is not double-spaced; that is, confirm that each line (string) in the records list does not include a terminating newline.
    print(line)

# 1b: Close the open expenses.txt file, then open expenses.txt again. Use list comprehension notation to create and initialize a new list, records2, from the lines in the expenses.txt file, excluding the terminating newline characters.  Confirm that you have done this correctly, by adding this code at the end of the script:
file_in.close()
file_in = open('expenses.txt', mode = 'rt', encoding = 'utf-8')
records2 = [line.replace('\n', '') for line in file_in]
print("\nrecords == records2:", records == records2, '\n') # This should display records == records2: True

# 1c: Close the open expenses.txt file, and open expenses.txt again. Learn about the str class’s split function. Fields in the expenses.txt file are separated with colon characters, ‘:’, since expense descriptions often contain commas. Use nested tuple conversion notation to create and initialize a new tuple of tuples, records3, in which each “inner” tuple has the form (amount,category,date,description), and the “outer” tuple contains one “inner” tuple for each line of input. We use a tuple of tuples because tuples are immutable, and we want to protect the input data from accidental change.
file_in.close()
file_in = open('expenses.txt', mode = 'rt', encoding = 'utf-8')
records3 = tuple(tuple(line.replace('\n', '').split(':')) for line in file_in)
for tup in records3:
    print(tup)

# 1d: Using set comprehension notation with records3, define: cat_set, the set of categories (do not include the string 'Category') in the expense records; and, date_set, the set of dates (again, do not include the string 'Date') in the expense records.  Add this code to display these two sets:
cat_set = {records3[i][1] for i in range(1, len(records3))}
date_set = {records3[i][2] for i in range(1, len(records3))}
print('Categories:', cat_set, '\n')
print('Dates:     ', date_set, '\n')

# 1e: Using dict comprehension notation with records3, define a dict named rec_num_to_record in which each entry’s key is the record (line) number, and each entry’s value is the tuple representing the data.  Hint: use a combination of range() and zip() along with records3.  In rec_num_to_record, store the field names as record number 0. Add this code to display rec_num_to_record:
rec_num_to_record = dict(zip(range(len(records3)), records3)) # dict comprehension using zip()
for rn in range(len(rec_num_to_record)):
    print('{:3d}: {}'.format(rn, rec_num_to_record[rn]))
# Add this code, using the items() iterable, to display rec_num_to_record:
for i in rec_num_to_record.items():
	print('{:3d}: {}'.format(i[0], i[1]))
# Alternatively, using tuple unpacking into two loop variables, you can use (for example):
for k, v in rec_num_to_record.items():
	print('{:3d}: {}'.format(k, v))
    
# 2 Variadic Functions 
# See additional scripts
    
# Zip files together
from zipfile import ZipFile
zip_object = ZipFile(zipfilename, 'w')
for file in ['hw3.1.py', 'mystats.py', 'my_stat_test.py', 'ch4.ipynb', 'ch4.html']:
    zip_object.write(file)
zip_object.close()
