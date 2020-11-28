# importing the required libraries

from flask import Flask, render_template, request, redirect, url_for
import pickle
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import os.path
import joblib

# load the pipeline object

model = open("model.pkl", "rb")
model = pickle.load(model)

# function to get results for a particular text query

def requestResults(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'lxml')
	pretified_page = soup.prettify()
	td = soup.select('h1')
	title = td[0].text
	title = title.lower()
	title = title.split()
	ps = PorterStemmer()
	title = [ps.stem(word) for word in title if not word in set(stopwords.words('english'))]
	title = ' '.join(title)
	# Load vectorizer
	vectorizer = joblib.load("vectorizer.joblib")
	x = vectorizer.transform([title])

	nb = pickle.load("model.pkl")
	predicted_flare = nb.predict(x)
	print(predicted_flare)

	flares = []

requestResults("https://www.reddit.com/r/india/comments/jj8aog/coronavirus_covid19_megathread_news_and_updates_7/")