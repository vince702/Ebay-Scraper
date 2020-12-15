import test
import os
import json
import time

previous = []

#print(test.lookup_psa(42603776))



results = test.commence_search("pokemon gold star psa 10")

ids = []
for item in results:
	ids.append(item['id'])
	l = item
	id_ = l['id']
	try:
		l['certNum'] = test.get_cert_number(test.get_image(id_))
		if (len(l['certNum']) != 1):
			continue
		print(l)
	except:
			continue


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


'''
with open('test_file.txt', 'a') as f:

	previous = []
	while(True):

		x = test.commence_search([""],"", '')
		ids = []


		for item in x:
			ids.append(item['id'])

		for item in x:
			if (item['id'] in previous):
				break
			else:
				l = item
		
				id_ = l['id']
				try:
					l['certNum'] = test.get_cert_number(test.get_image(id_))
					if (len(l['certNum']) != 1):
						continue
				except:
					continue

				json.dump(l, f)
				f.write(os.linesep)

		previous = ids
		

		time.sleep(300)
'''