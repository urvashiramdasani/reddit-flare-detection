# importing the required libraries

from flask import Flask, render_template, request, redirect, url_for, jsonify
import pickle
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import os.path
import numpy as np
import joblib

# function to get results for a particular text query

def requestResults(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
	response = requests.get(url, headers = headers)
	soup = BeautifulSoup(response.text, 'lxml')
	pretified_page = soup.prettify()
	try:
		td = soup.select('h1')
		title = td[0].text
		title = title.lower()
		title = title.split()
		ps = PorterStemmer()
		title = [ps.stem(word) for word in title if not word in set(stopwords.words('english'))]
		title = ' '.join(title)
		# Load vectorizer
		vectorizer = joblib.load("vectorizer2.joblib")
		x = vectorizer.transform([title])

		model = joblib.load("vec.joblib")
		prob = model.predict_proba(x).reshape((31,))
		idx = np.argmax(prob)

		flares = ["/r/all", "Art/Photo (OC)", "AskIndia", "Business/Finance", "CAA-NRC", "CAA-NRC-NPR", "Casual AMA",
		"Coronavirus", "Demonetization", "Food", "History", "Misleading Headline", "Moderated", "Non-Political", "Official Sadness Thread",
		"Original Comics", "Photography", "Policy & Economy", "Policy/Economy -2017 Article", "Politics", "Scheduled",
		"Science/Technology", "Sports", "TW for South Indian People", "They knew", "Totally Real", "Unverified", 
		"Zoke tyme", "[R]eddiqeutte", "r/indiameme", "why tho?"]

		return flares[idx]
	except IndexError:
		return "URL not found!"

def automated_requests(file):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
	url = str(file.readline())[2:-5]
	# print(urls[2:-5], type(urls))
	ps = PorterStemmer()
	vectorizer = joblib.load("vectorizer2.joblib")
	model = joblib.load("vec.joblib")

	predicted_flares = dict()

	while url:
		response = requests.get(url, headers = headers)
		soup = BeautifulSoup(response.text, 'lxml')
		pretified_page = soup.prettify()
		try:
			td = soup.select('h1')
			title = td[0].text
			title = title.lower()
			title = title.split()
			title = [ps.stem(word) for word in title if not word in set(stopwords.words('english'))]
			title = ' '.join(title)
			# Load vectorizer
			x = vectorizer.transform([title])
			prob = model.predict_proba(x).reshape((31,))
			idx = np.argmax(prob)

			flares = ["/r/all", "Art/Photo (OC)", "AskIndia", "Business/Finance", "CAA-NRC", "CAA-NRC-NPR", "Casual AMA",
			"Coronavirus", "Demonetization", "Food", "History", "Misleading Headline", "Moderated", "Non-Political", "Official Sadness Thread",
			"Original Comics", "Photography", "Policy & Economy", "Policy/Economy -2017 Article", "Politics", "Scheduled",
			"Science/Technology", "Sports", "TW for South Indian People", "They knew", "Totally Real", "Unverified", 
			"Zoke tyme", "[R]eddiqeutte", "r/indiameme", "why tho?"]

			predicted_flares[url] = flares[idx]

		except IndexError:
			predicted_flares[url] = "URL not found!";

		url = str(file.readline())[2:-5]

	return jsonify(predicted_flares)


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        url = request.form['link']
        return requestResults(str(url))

@app.route('/automated_testing')
def automated_testing_form():
	return render_template('home_file.html')

@app.route('/automated_testing', methods = ['POST', 'GET'])
def automated_testing():
	if request.method == 'POST':
		file = request.files['file']
		return automated_requests(file)

if __name__ == '__main__' :
    app.run(debug=True)