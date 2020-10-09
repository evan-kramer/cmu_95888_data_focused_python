'''
Team 12
Evan Kramer
evankram
Anqi Luo
anqiluo
'''
# Set up
team = 12
from urllib.request import urlopen  
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime

html = urlopen('https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldYear&year=2020')
bsyc = BeautifulSoup(html.read(), "lxml")

# 1a
# Removed intermediate outputs
# Accumulate list of lists
daily_yield_curves = []
for c in bsyc.findAll('table', { "class" : "t-chart" })[0].children:
    temp_list = [r.contents[0] for r in c.children]
    daily_yield_curves.append(temp_list)
# Convert to float and output file for 2020
file_out = open('daily_yield_curves.txt', 'wt', encoding = 'utf-8')
for li in daily_yield_curves:
    # Convert to floats
    for i in range(1, len(li)):
        try:
            li[i] = float(li[i])
        except:
            pass
    # Output file
    file_out.write(str(li))
    file_out.write('\n')
# Close connection to file
file_out.close()

# 1b
# 3D surface and wireframe plot of daily yield curves - https://matplotlib.org/Matplotlib.pdf
# Create 2d arrays (why do they have to be 2D?)
# x = TRADING days since 1/2/2020
x_dict = {daily_yield_curves[i][0]: i for i in range(1, len(daily_yield_curves))}
x_array = np.array(range(1, len(daily_yield_curves)))
# y = months to maturity
months = []
for i in daily_yield_curves[0]:
    if 'mo' in i:
        months.append(int(i[:2]))
    elif 'yr' in i:
        months.append(int(i[:2]) * 12)
    else:
        pass
y_dict = dict(zip(daily_yield_curves[0][1:len(daily_yield_curves[0])], months))
y_array = np.array(months)
# z = rate
rates = []
for i in range(len(daily_yield_curves)):
    if i == 0:
        pass
    else:
        rates.append([daily_yield_curves[i][j] for j in range(1, len(daily_yield_curves[i]))])
z_array = np.array(rates)
# Wireframe plot
fig = plt.figure()
ax = fig.gca(projection = '3d')
ax.set_xlabel('Trading Days since Start of Year')
ax.set_ylabel('Months to Maturity')
ax.set_zlabel('Rate')
Y, X = np.meshgrid(y_array, x_array) # make sure to check dimensions with .shape
Z = np.array(rates)
ax.plot_wireframe(X, Y, Z)
plt.show()
# Surface plot
fig = plt.figure()
ax = fig.gca(projection = '3d')
surf = ax.plot_surface(X, Y, Z, cmap = 'PiYG')
ax.set_xlabel('Trading Days since Start of Year')
ax.set_ylabel('Months to Maturity')
ax.set_zlabel('Rate')
fig.colorbar(surf, shrink = 0.5, aspect = 5)
plt.show()

# 1c
# Trading dates as rows and bond maturities as columns
# Index/row labels should be dates
yield_curve_df = pd.DataFrame(daily_yield_curves[1:len(daily_yield_curves)], 
                               index = [daily_yield_curves[i][0] for i in range(1, len(daily_yield_curves))], 
                              columns = daily_yield_curves[0]).drop(columns = 'Date')
# Plot df
yield_curve_df.plot(title = 'Interest Rate Time Series, ' + 
                    str(datetime.today().year))
# Transpose then plot; looks a mess (intentionally)
yield_curve_df.transpose().plot()
# Create by_day_yield_curve_df with every 20th day and plot
by_day_yield_curve_df = (yield_curve_df[0:len(yield_curve_df):20]
 .transpose()
 .set_index(pd.Index(y_dict.values())))
(by_day_yield_curve_df
 .plot(title = str(datetime.today().year) + ' Yield Curves, 20 Day Intervals')
 .legend(loc = 'lower right'))

# Output everything and zip together
# Zip files together
from zipfile import ZipFile
import os
zipfilename = 'Team_' + str(team) + '_HW4.zip'
zip_object = ZipFile(zipfilename, 'w')
for file in os.listdir():
    if '~' in file or '.zip' in file or 'DFP' in file:
        pass
    else:
        zip_object.write(file)
zip_object.close()
