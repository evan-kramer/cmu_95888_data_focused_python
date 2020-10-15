# Forage
Final Project for 95-888 Data Focused Python
Evan Kramer (evankram)
Shoukang Mao (shoukanm)
Omar Othman (oothman)

## Overview 
This project scrapes data from a number of grocery store websites and tabulates them for users to search and compare.
This document is written in markdown and our code is available on GitHub [here](https://github.com/evan-kramer/cmu_95888_data_focused_python/tree/main/Final%20Project).

## Prerequisites
You will need to install the following modules in order to run the application: 
- [NumPy](https://numpy.org)
- [Pandas](https://pandas.pydata.org/)
- [requests](https://requests.readthedocs.io/en/master/)
- [re](https://docs.python.org/3/library/re.html)
- [difflib](https://docs.python.org/3/library/difflib.html)
- [os](https://docs.python.org/3/library/os.html)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [selenium](https://selenium-python.readthedocs.io/)
- [time](https://docs.python.org/3/library/time.html)

## Web Scraping
This application uses Selenium to scrape data from multiple national grocery store websites, including Albertsons and Target. Selenium relies on a webdriver to send requests to the server programmatically. 
We have included a copy of the Google Chrome webdriver in the .zip file. If you do not have Chrome installed, you can download the driver for your preferred browser and replace the code accordingly where the `driver` object is defined.

## API Keys
The app also takes user-entered zip codes to return locations to try to get more accurate prices. It obtains city and state information through the USPS API.
We have provided a sample API key inline in the code, so you do not need to register for your own account. However, you can follow the steps below to obtain an API key of your own if you'd like:
- Visit [this website](https://registration.shippingapis.com/)
- Enter the relevant and required personal details
- You'll receive an email with a user ID, which you'll use to replace the user ID element of the xml object on L105 of the `ui.py` script

Similarly, we use the [GROCERYBEAR API](https://www.grocerybear.com) to get a list of common products across various major markets. We have again included a sample API key, but you can register for a free API key of your own [here](https://grocerybear.com/).
It is worth noting that their site does not appear to be updated regularly, but we use it to get a list of the most common food items to compare across markets.

## Interacting with the Application
- Open `ui.py` from IDLE or Spyder
- Hit F5 or select "Run Module" from the "Run" menu 
- Follow the inline prompts and search to your heart's content

## Link to Video
[This video](https://www.loom.com/share/217bb40397194b4db0c12b90e106e7a6) demonstrates the high-level functionality of the application. 