# importing the required libraries

from flask import Flask, render_template, request, redirect, url_for
import pickle
from get_tweets import get_related_tweets

# load the pipeline object

pipeline = pickle.load("model.pkl")

# function to get results for a particular text query

def requestResults(link):
	