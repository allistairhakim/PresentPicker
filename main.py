from flask import Flask, render_template, request, jsonify, make_response
import json

app = Flask(
 __name__,
 template_folder='templates',  # Name of html file folder
 static_folder='static'  # Name of directory for static files
)


@app.route('/')
def index():
	return render_template("home.html")


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


@app.route('/get_selections', methods=['POST'])
def get_selections():
	#NORMAL
	content_type = request.headers.get('Content-Type')
	if (content_type == 'application/json'):
		data = request.json
		print(data)
		return "https://google.com"


@app.route('/get_gifts', methods=['POST'])
def update_data():
	#NORMAL
	content_type = request.headers.get('Content-Type')
	if (content_type == 'application/json'):
		data = request.json
		print(data)
		return json.dumps(dummy_data)
		#return array of [[name, [{title: sample, image: sample_image.png, price: sample, link: sample, stars: 1-5}, ]], ]


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=81)
