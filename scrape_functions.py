import datetime
import sys

import ssl
import urllib.request
from bs4 import BeautifulSoup

from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import ebaysdk.shopping
import os
import re
import requests
import cloudscraper

APP_ID = '=====EBAY API APP_ID HERE====='

os.environ.setdefault("EBAY_YAML", "ebay.yaml")
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
psa_url = "https://www.psacard.com/cert/"
headers={'User-Agent':user_agent,} 
ssl._create_default_https_context = ssl._create_unverified_context

from PIL import Image

from pytesseract import image_to_string
import pytesseract


#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#im = urllib.request.urlopen('https://i.ebayimg.com/00/s/MTYwMFgxMjAw/z/WgYAAOSwrpNdFVM7/$_57.JPG?set_id=8800005007')
#text = re.findall(r'[0-9]{8}',image_to_string(Image.open(im)))
#print(text)


#gets the cert number from an image given that image url
def get_cert_number(url):
	im = urllib.request.urlopen(url)
	text = re.findall(r'[0-9]{8}',image_to_string(Image.open(im)))
	return text


#given an ebay listing id, return the first image
def get_image(id=333274691098):
	connection = ebaysdk.shopping.Connection(version='799', appid=APP_ID,config_file=os.environ.get('EBAY_YAML'))
	response = connection.execute('GetSingleItem', {
	                'ItemID': id
	            })

	result = response.dict()
	print(result['Item']['PictureURL'][0])

	return result['Item']['PictureURL'][0]




#returns sold listings, need to change api call to return current listings
def commence_search( query  ):
    
        try:
            search_term = query
            api = Connection(appid=APP_ID, config_file=None)
            response = api.execute('findItemsByKeywords', {'keywords':search_term})


            assert(response.reply.ack == 'Success')
            assert(type(response.reply.timestamp) == datetime.datetime)
            assert(type(response.reply.searchResult.item) == list)
            item = response.reply.searchResult.item

            search_results = response.dict()
            
            item = response.reply.searchResult.item[0]
            assert(type(item.listingInfo.endTime) == datetime.datetime)
            assert(type(response.dict()) == dict)
            #print (len(k['searchResult']['item']))

            #print (search_results['searchResult']['item'][0]['itemId'])
            #print (search_results['searchResult']['item'][1]['itemId'])
            
            item_list = [0] * len(search_results['searchResult']['item'])

            index = 0
            for listing in search_results['searchResult']['item'] :

            	listing = {'id':listing['itemId'],
            				'title':listing['title'],
            				'currency':listing['sellingStatus']['convertedCurrentPrice']['_currencyId'],
            				'price':listing['sellingStatus']['convertedCurrentPrice']['value'],
            				'start':listing['listingInfo']['startTime'],
            				'end':listing['listingInfo']['endTime'],
            				'offerEnabled':listing['listingInfo']['bestOfferEnabled'],
            				'buyItNowAvailable':listing['listingInfo']['buyItNowAvailable'],
            				'state':listing['sellingStatus']['sellingState']}
            	item_list[index] = listing
            	index += 1
            return item_list


        except ConnectionError as e:

            print(e)
            print(e.response.dict())




#@param query a string to search ebay
#@return psacards, an array with ebay listing info on all items and the cert number of the psa label in the listing image
def get_psa_cards_from_search(query):
    psa_cards = []

    results = test.commence_search(query)

    ids = []
    for item in results:
        ids.append(item['id'])
        l = item
        id_ = l['id']
        try:
            l['certNum'] = test.get_cert_number(test.get_image(id_))
            if (len(l['certNum']) != 1):
                continue
            psacards.append(l)
        except:
                continue

    print(psacards)
    return psacards



    
#scrapes psa's website to return info on card given cert number
def lookup_psa(cert_number):  
  
    url = psa_url + str(cert_number)
    print(url)

    

    scraper = cloudscraper.create_scraper()  
    page = scraper.get(url).content  
    soup = BeautifulSoup(page, 'lxml')
    


    psa_card_dict = {}
    for name in soup.find_all("td", class_="cert-grid-title"):
        label = name.parent.find_all('td')[0]
        label = label.get_text()
        value = name.parent.find_all('td')[-1]
        value = value.get_text()
        psa_card_dict[str(label)] = value


    
    return psa_card_dict











