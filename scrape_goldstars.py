
import os
import copy
import re
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time 

import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 

import os

from datetime import datetime

#url of the page we want to scrape 
urls = []

url = "https://www.psacard.com/pop/tcg-cards/2006/pokemon-ex-crystal-guardians/87132"
urls.append(url)

url = "https://www.psacard.com/pop/tcg-cards/2007/pokemon-pop-series-5/101536"
urls.append(url)

url = 'https://www.psacard.com/pop/tcg-cards/2005/pokemon-japanese-golden-sky-silvery-ocean/100014'
urls.append(url)

url = "https://www.psacard.com/pop/tcg-cards/2006/pokemon-ex-dragon-frontiers/87126"
urls.append(url)

# initiating the webdriver. Parameter includes the path of the webdriver. 

with open('gold_stars.csv', "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(['name','1','2','3','4','5','6','7','8','9','10','Total_pop','date'])




def get_pop(url):
    driverpath = os.path.realpath(r'/usr/local/bin/chromedriver')
    chrome_options = Options()  

    driver = webdriver.Chrome(driverpath, options=chrome_options) 
    driver.get(url)  
      
    # this is just to ensure that the page is loaded 
    time.sleep(5)  
      
    html = driver.page_source 
      
    # this renders the JS code and stores all 
    # of the information in static HTML code. 
      
    # Now, we could simply apply bs4 to html variable 
    soup = BeautifulSoup(html, "html.parser") 


    n = 0

    text = ''

    for k in soup.find_all('td'):
        temp = []
        
        text += k.get_text()


    text = text.split('\n')

    indeces = [0,12,20,24,28,32,36,40,44,48,52,56]

    data = []
    i = 59
    
    
    today = datetime.today()

    date = ''
    date += (str(today.year) + '-' + str(today.month)) 

    set_name = url.split('/')
    set_name = set_name[-2]
    set_name = set_name[8:]

    while i < len(text):
      entry = []
      temp = text[i:(i+62)]
      temp[0] = temp[0] + ' ' + temp[1]
      entry = []
      for k in indeces:
         entry.append(temp[k].strip())

      entry.append(set_name)
      entry.append(date)

      data.append(entry)
      i += 62



 

    today = datetime.today()


    file_name = set_name +  '.csv'
    

    with open(file_name, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(['name','1','2','3','4','5','6','7','8','9','10','Total_pop','date'])
        for i in data:
            wr.writerow(i)


    with open('gold_stars.csv', "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        for i in data:
            if "Gold Star" in i[0]:
                wr.writerow(i)
        




    print(data)

        
        
    driver.close()



for url in urls:
    get_pop(url)


