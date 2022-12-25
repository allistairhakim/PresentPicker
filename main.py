from flask import Flask, render_template, request, jsonify, make_response
import json
import requests
from lxml import html, etree
import math
import secrets
import string
import firebase_admin
from firebase_admin import credentials, db
from collections import OrderedDict

cred = credentials.Certificate(
 "presentpicker-300bf-firebase-adminsdk-xjd57-7f498a83ff.json")
firebase_admin.initialize_app(
 cred,
 {'databaseURL': 'https://presentpicker-300bf-default-rtdb.firebaseio.com/'})
ref = db.reference("/")
# with open("book_info.json", "r") as f:
# 	file_contents = json.load(f)
# ref.set(file_contents)
#ref.push().set(json.loads('{"dude": "lol"}'))

app = Flask(
 __name__,
 template_folder='templates',  # Name of html file folder
 static_folder='static'  # Name of directory for static files
)


@app.route('/')
def index():
	return render_template("home.html")


config = {
 'apiKey': "AIzaSyC5zpV2c0vGtnjYasp8oUGAMHncIv2QMTE",
 'authDomain': "presentpicker-300bf.firebaseapp.com",
 'projectId': "presentpicker-300bf",
 'storageBucket': "presentpicker-300bf.appspot.com",
 'messagingSenderId': "341951316963",
 'appId': "1:341951316963:web:2bcf7369542cd01931d6d6",
 'measurementId': "G-2FZBRC83PR"
}

dummy_data = [
 {
  "name":
  "Alex",
  "list": [
   {
    "title": "Xbox 360",
    "image":
    "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcSVYZd1WVBRUv4jZKcwcLun45k2ShqgbK33p_Xza27bQb8Qclk8x0-tN2UAixcruK1PF5TMu2-selNH67Ci2BmNUtcgT1X6VNfgION2rVQ0zwcJRqKcLjKB&usqp=CAE",
    "price": 359.99,
    "link":
    "https://www.ebay.com/itm/334658371723?chn=ps&mkevt=1&mkcid=28&srsltid=AeTuncp8f9W6PWesSdlJtl-azpjdoasrDV5XzPDR3F-dXsYorhu1atoqiuc",
    "stars": 4.2,
   },
   {
    "title": "Xbox X",
    "image":
    "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQwW8jaTfeaJ95Sm9o4trNhDHYh481Z3gdl2k5tmXooo1OGRCOxnyvbAoltQCrIk-VaNzmqQDHoXMCgRCTkOBT58mImxdqM_pBEi5exez1_lr-Ngg2S7Cx5KQ&usqp=CAE",
    "price": 599.99,
    "link":
    "https://www.google.com/url?q=https://monoshopy.com/product/xbox-series-x-1tb-ssd-console-extra-xbox-wireless-controller-halo-infinite/%3Futm_source%3DGoogle%2BShopping%26utm_medium%3Dcpc%26utm_campaign%3Dfeedtest&sa=U&ved=0ahUKEwjBwvujl5H8AhXNTjABHd47BXwQgOUECI4F&usg=AOvVaw3PXKdMRozoECxWVccm6oe4",
    "stars": 3.9,
   },
   {
    "title": "Xbox 360",
    "image":
    "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcSVYZd1WVBRUv4jZKcwcLun45k2ShqgbK33p_Xza27bQb8Qclk8x0-tN2UAixcruK1PF5TMu2-selNH67Ci2BmNUtcgT1X6VNfgION2rVQ0zwcJRqKcLjKB&usqp=CAE",
    "price": 359.99,
    "link":
    "https://www.ebay.com/itm/334658371723?chn=ps&mkevt=1&mkcid=28&srsltid=AeTuncp8f9W6PWesSdlJtl-azpjdoasrDV5XzPDR3F-dXsYorhu1atoqiuc",
    "stars": 4.2,
   },
  ]
 },
 {
  "name":
  "Mary",
  "list": [
   {
    "title": "Xbox 360",
    "image":
    "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcSVYZd1WVBRUv4jZKcwcLun45k2ShqgbK33p_Xza27bQb8Qclk8x0-tN2UAixcruK1PF5TMu2-selNH67Ci2BmNUtcgT1X6VNfgION2rVQ0zwcJRqKcLjKB&usqp=CAE",
    "price": 359.99,
    "link":
    "https://www.ebay.com/itm/334658371723?chn=ps&mkevt=1&mkcid=28&srsltid=AeTuncp8f9W6PWesSdlJtl-azpjdoasrDV5XzPDR3F-dXsYorhu1atoqiuc",
    "stars": 4.2,
   },
   {
    "title": "Xbox X",
    "image":
    "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcQwW8jaTfeaJ95Sm9o4trNhDHYh481Z3gdl2k5tmXooo1OGRCOxnyvbAoltQCrIk-VaNzmqQDHoXMCgRCTkOBT58mImxdqM_pBEi5exez1_lr-Ngg2S7Cx5KQ&usqp=CAE",
    "price": 599.99,
    "link":
    "https://www.google.com/url?q=https://monoshopy.com/product/xbox-series-x-1tb-ssd-console-extra-xbox-wireless-controller-halo-infinite/%3Futm_source%3DGoogle%2BShopping%26utm_medium%3Dcpc%26utm_campaign%3Dfeedtest&sa=U&ved=0ahUKEwjBwvujl5H8AhXNTjABHd47BXwQgOUECI4F&usg=AOvVaw3PXKdMRozoECxWVccm6oe4",
    "stars": 3.9,
   },
  ]
 },
]

#setup request
headers = {
 "User-Agent":
 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
 'VIEWPORT-WIDTH': '1918'
}
params = {"hl": "en", 'gl': 'us'}


#AUXILIARRY FUNCS
#Getting all of the data
def get_page_data(page_content):
	result = []
	curr = html.fromstring(page_content.content).xpath(
	 '//*[@id="spch"]')[0].getnext().getnext().getnext()
	img_dict = {}
	while not curr is None:
		out = str(etree.tostring(curr)).replace('\\x3d',
		                                        '=').replace('\\x26',
		                                                     '&').replace('\\', '')
		if "_u='" not in out:
			break
		img_dict.update(
		 {out.split("_i='")[1].split("'")[0]: out.split("_u='")[1].split("'")[0]})
		curr = curr.getnext()
	for j in range(
	  1,
	  len(
	   html.fromstring(page_content.content).xpath(
	    "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div"
	   ))):
		if (len(
		  html.fromstring(page_content.content).xpath(
		   "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div["
		   + str(j) + "]/div")) <= 0):
			break
		result_dict = {}
		result_dict.update({
		 'Name':
		 str(
		  etree.tostring(
		   html.fromstring(page_content.content).xpath(
		    "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div["
		    + str(j) + "]/div/div[2]/span/a/div/h3")[0])).split('>')[1].split('<')[0]
		})
		result_dict.update({
		 'Price':
		 str(
		  etree.tostring(
		   html.fromstring(page_content.content).xpath(
		    "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div["
		    + str(j) + "]/div/div[2]/div[2]/span/div/a/div[2]/span/span/span/span")
		   [0])).split('>')[1].split('<')[0]
		})
		result_dict.update({
		 'Link':
		 str(
		  etree.tostring(
		   html.fromstring(page_content.content).xpath(
		    "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div["
		    + str(j) + "]/div/div[2]/div[2]/span/div/a")[0])).split(
		     'href="/url?url=')[1].split('"')[0]
		})
		result_dict.update({
		 'Image':
		 img_dict[str(
		  etree.tostring(
		   html.fromstring(page_content.content).xpath(
		    "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div["
		    + str(j) + "]")[0])).split('docid="')[1].split('"')[0]]
		})
		result.append(result_dict.copy())
		# print(result_dict['Name'])
		# print(result_dict['Price'])
		# print(result_dict['Link'])
		# print(result_dict['Image'])
	return result


def highest_price(page_content):
	with open('content.txt', 'w', encoding='utf-8') as f:
		f.write(page_content.text)
	curr = html.fromstring(page_content.content).xpath(
	 '//*[@id="spch"]')[0].getnext().getnext().getnext()
	img_dict = {}
	output = []
	while not curr is None:
		out = str(etree.tostring(curr)).replace('\\x3d',
		                                        '=').replace('\\x26',
		                                                     '&').replace('\\', '')
		if "_u='" not in out:
			break
		img_dict.update(
		 {out.split("_i='")[1].split("'")[0]: out.split("_u='")[1].split("'")[0]})
		curr = curr.getnext()
	for j in range(
	  1,
	  len(
	   html.fromstring(page_content.content).xpath(
	    "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div"
	   ))):
		if (len(
		  html.fromstring(page_content.content).xpath(
		   "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div["
		   + str(j) + "]/div")) <= 0):
			break
		result_dict = {}
		result_dict.update({
		 'Name':
		 str(
		  etree.tostring(
		   html.fromstring(page_content.content).xpath(
		    "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div["
		    + str(j) + "]/div/div[2]/span/a/div/h3")[0])).split('>')[1].split('<')[0]
		})
		result_dict.update({
		 'Price':
		 str(
		  etree.tostring(
		   html.fromstring(page_content.content).xpath(
		    "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div["
		    + str(j) + "]/div/div[2]/div[2]/span/div/a/div[2]/span/span/span/span")
		   [0])).split('>')[1].split('<')[0]
		})
		result_dict.update({
		 'Link':
		 str(
		  etree.tostring(
		   html.fromstring(page_content.content).xpath(
		    "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div["
		    + str(j) + "]/div/div[2]/div[2]/span/div/a")[0])).split(
		     'href="/url?url=')[1].split('"')[0]
		})
		result_dict.update({
		 'Image':
		 img_dict[str(
		  etree.tostring(
		   html.fromstring(page_content.content).xpath(
		    "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div["
		    + str(j) + "]")[0])).split('docid="')[1].split('"')[0]]
		})
		result_price = float(result_dict['Price'].strip('$').replace(',', ''))
		if len(output) < 8 or result_price > float(
		  output[0]['Price'].strip('$').replace(',', '')):
			if len(output) == 0:
				output.append(result_dict.copy())
			elif len(output) < 8:
				added = False
				for count, value in enumerate(output):
					if result_price < float(value['Price'].strip('$').replace(',', '')):
						output.insert(count, result_dict.copy())
						added = True
						break
				if not added:
					output.append(result_dict.copy())
			else:
				added = False
				for count, value in enumerate(output):
					if result_price < float(value['Price'].strip('$').replace(',', '')):
						output.insert(count, result_dict.copy())
						added = True
						break
				if not added:
					output.append(result_dict.copy())
				output.pop(0)
	return output


def get_median(prompt):
	headers = {
	 "User-Agent":
	 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
	 'VIEWPORT-WIDTH':
	 '1918',
	 'SEC-CH-UA-ARCH':
	 "x86",
	 'SEC-CH-UA-PLATFORM':
	 "Windows",
	 'SEC-CH-UA-PLATFORM-VERSION':
	 "10.0.0",
	 'SEC-CH-UA':
	 '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"'
	}
	params = {"hl": "en", 'gl': 'us'}
	site = requests.get(
	 'https://www.google.com/search?tbm=shop&tbs=p_ord:p&q=' + prompt,
	 headers=headers,
	 params=params)  # ord: p = low to high, pd = high to low, r = relevance
	next_page_link = ''.join(
	 str(etree.tostring(
	  html.fromstring(site.content).xpath('//*[@id="xjs"]')[-1])).split('<tr')
	 [1].split('>')[2:-1])
	next_page_link = next_page_link.split('href="')
	middle_page = math.floor((len(next_page_link) - 1) / 4)
	if middle_page != 1 or middle_page != 0:
		for count, value in enumerate(next_page_link):
			if count + 1 == middle_page:
				next_page_link = 'https://www.google.com' + value.split('"')[0].replace(
				 '&amp;', '&')
				break
		next = requests.get(next_page_link, headers=headers, params=params)
		with open('content.txt', mode='w', encoding='utf-8') as f:
			f.write(next.text)
		return str(
		 etree.tostring(
		  html.fromstring(next.content).xpath(
		   "//div[contains(@class, 'sh-pr__product-results-grid sh-pr__product-results')]/div[1]/div/div[2]/div[2]/span/div/a/div[2]/span/span/span/span"
		  )[0])).split('>')[1].split('<')[0]


def weights(median_arr, budget):
	tot = 0
	for i in median_arr:
		tot += i
	difference = budget / tot
	for i in range(len(median_arr)):
		median_arr[i] *= difference
		median_arr[i] = math.floor(median_arr[i] * 100) / 100
	return median_arr


def find_items(median_arr, keyword_arr):
	x = requests.session()
	result = []
	for count, value in enumerate(median_arr):
		headers = {
		 "User-Agent":
		 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
		 'VIEWPORT-WIDTH':
		 '1918',
		 'SEC-CH-UA-ARCH':
		 "x86",
		 'SEC-CH-UA-PLATFORM':
		 "Windows",
		 'SEC-CH-UA-PLATFORM-VERSION':
		 "10.0.0",
		 'SEC-CH-UA':
		 '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"'
		}
		params = {"hl": "en", 'gl': 'us'}
		site = x.get(
		 'https://www.google.com/search?tbm=shop&tbs=p_ord:pd,price:1,ppr_max:' +
		 str(value) + '&q=' + keyword_arr[count],
		 headers=headers,
		 params=params)  # ord: p = low to high, pd = high to low, r = relevance
		output = highest_price(site)
		# for out in output:
		#     print(out['Name'])
		#     print(out['Price'])
		#     print(out['Link'])
		#     print(out['Image'])
		# if count != len(median_arr) - 1:
		#     median_arr[count + 1] += value - float(out['Price'].strip('$'))
		result.append(output)
	print(result)
	return result


@app.route('/saved_gifts/<gifts_id>')
def saved_gifts(gifts_id):
	data = dict(ref.order_by_child("name").equal_to(gifts_id).get())
	res = list(data.keys())[0]

	return render_template('saved_gifts.html', datas=data[res]["list"])


@app.route('/get_selections', methods=['POST'])
def get_selections():
	#NORMAL
	content_type = request.headers.get('Content-Type')
	if (content_type == 'application/json'):
		data = request.json
		acc = "["
		print(data["data"][0]["list"][1])
		for i in range(len(data["index"])):
			print(data["index"][i])
			acc += str(data["data"][i]["list"][data["index"][i]]).replace("\'",
			                                                              "\"") + ","
		acc = acc[:-1]
		acc += "]"
		print(acc)
		randString = ''.join(
		 secrets.choice(string.ascii_uppercase + string.digits) for i in range(7))
		print('{"name" : "' + randString + '", "list": ' + acc + '}')
		ref.push().set(
		 json.loads('{"name" : "' + randString + '", "list": ' + acc + '}'))
		return "../../saved_gifts/" + randString


@app.route('/get_gifts', methods=['POST'])
def update_data():
	#NORMAL
	content_type = request.headers.get('Content-Type')
	if (content_type == 'application/json'):
		data = request.json
		median_arr = []
		keywords = []
		for i in range(len(data["names"])):
			keyword = data["gifts"][i]
			keywords.append(keyword)
			median_arr.append(float(get_median(keyword).strip('$')))
		median_arr = weights(median_arr, float(data["price"]))
		print(median_arr)
		result_dict = find_items(median_arr, keywords)

		out_dict = []
		#change later
		for i in range(len(data["names"])):
			out_dict.append({"name": data["names"][i], "list": []})
			for set in result_dict[i]:
				out_dict[i]["list"].append({
				 "title": set["Name"],
				 "image": set["Image"],
				 "price": set["Price"],
				 "link": set["Link"],
				 "stars": 5.0,
				})
		print(data["names"][i])
		return json.dumps(out_dict)
		#return array of [[name, [{title: sample, image: sample_image.png, price: sample, link: sample, stars: 1-5}, ]], ]


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=81)

# x = requests.session()
# keyword = input()
# headers = {
#     "User-Agent":
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
#     'VIEWPORT-WIDTH':
#     '1918'
# }
# params = {"hl": "en", 'gl': 'us'}
# site = x.get('https://www.google.com/search?tbm=shop&tbs=p_ord:p&q=' + keyword, headers=headers, params=params) #ord: p = low to high, pd = high to low, r = relevance
# result_dict = get_page_data(site)
# median = get_medidan(site)
