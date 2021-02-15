
import json
import boto3
from botocore.vendored import requests

import re
import json



def findTruePrice(id):

	error_value = {
		"bin_price":"error getting item",
		"actual_price":"no price available"
	}

	#extract the id number from listing
	id = re.findall('\d{12}',id)
	try:
	 	id = id[0]
	except:
		return json.dumps(error_value)


	try:
		#generate URL containing the tax exclusive price
		url = "https://www.ebay.com/itm/" + id + "?orig_cvip=true&nma=true&nordt=true&rt=nc"
		r = requests.get(url)
		url_text = r.text
		
		#extract image url
		image_pattern = '<img id="icImg" .*?itemprop="image" src="(.*?).jpg"'
		match_image = re.findall(image_pattern,url_text)
		image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/400px-Question_mark_%28black%29.svg.png'
		try:
			image_url = match_image[0] + ".jpg"
		except:
			pass

		#extract the actual price
		actual_price_pattern = '"taxExclusivePrice":"(.*?)"'
		
		match = re.findall(actual_price_pattern,url_text)
		
		actual_price = match[0]

		#extract listed price
		bin_price_pattern = '"binPrice":"(.*?)"'
		match = re.findall(bin_price_pattern,url_text)
		bin_price = match[0]

		#return value containing BIN price and actual price
		prices = {
			"bin_price":bin_price,
			"actual_price":actual_price,
			"image_url":image_url
		}

		return(json.dumps(prices))
		


	except:
		return json.dumps(error_value)
		
def respond(res):
	return{
		'statusCode':'200',
		'body': res,
		'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Content-Type':'application/json'
        },
		
	}
	
def lambda_handler(event, context):
  
    #body = event['body']
    
    listing_id = event['queryStringParameters']['listing_id']
    
    return respond(findTruePrice(listing_id))
    
