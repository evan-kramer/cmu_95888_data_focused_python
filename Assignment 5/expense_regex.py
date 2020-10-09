'''
Team 12
Evan Kramer
evankram
Lexi Rutkowski
arutkows
'''
# Set up
team = 12
# List comprehension to create records
file_in = open('expenses.txt', mode = 'rt', encoding = 'utf-8')
records = [line for line in file_in]
file_in.close()

import re

# 1a
# pat = r'D'

# 1b 
# pat = r'\''

# 1c
# pat = r'"'

# 1d
# pat = r'^7'

# 1e
# pat = r'[rt]$'

# 1f
# pat = r'\.'

# 1g
# pat = r'r.*g'

# 1h
# pat = r'[A-Z][A-Z]'

# 1i
# pat = r'\,'

# 1j
# pat = r'[\,].*[\,].*[\,]'

# 1k
# pat = r'^[^v-zV-Z]*$'

# 1l
# pat = r'^[1-9][0-9]\.[0-9][0-9]'

# 1m
# pat = '^(?:(?!,).)*(?:,(?:(?!,).)*){3}$'
# pat = r'(,.*){3}'

# 1n
# pat = r'\('

# 1o
# pat = r'^[1-9][0-9][0-9]\.[0-9][0-9].*:.*meal.*:.*$'

# 1p
# pat = r'.*:[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]:.*$' # this assumes categories will contain only alphanumeric

# 1q
# pat = r'20[0-9][0-9]03[0-3][0-9]' # will work for future years

# 1r
# pat = r'a.*b.*c.*'

# 1s
# pat = r'(..).*\1.*\1'

# 1t
# pat = r'^.*:.*:.*:.*([0-9].*a|a.*[0-9]).*$'

# 1u
# pat = r'^[^A-Z]*$'

# 1v
pat = r'd.i|di'

for line in records:
    if re.search(pat, line) != None:
        print(line)
  
# Output everything and zip together
# Zip files together
from zipfile import ZipFile
import os
zipfilename = 'Team_' + str(team) + '_HW5.zip'
zip_object = ZipFile(zipfilename, 'w')
for file in os.listdir():
    if '.py' in file :
        zip_object.write(file)
    else:
        pass
zip_object.close()