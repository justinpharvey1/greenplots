from flask import Flask
from flask import request
from flask import render_template
import requests
import pymysql
import sys
import logging
import json

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('index.html')



@app.route('/featuredlistings')
def featuredlistings():
    return render_template('featuredlistings.html', name="its working")



@app.route('/findyourhome')
def findyourhome():
	return render_template('findyourhome.html', name="its working")


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      lambdaURL = "https://nlcvv8kgd0.execute-api.us-west-2.amazonaws.com/prod"
      headers = {'Content-Type', 'application/json'}
      jsonParams = {"params": {"zipcode": result['zipcode'], "acreage": result['acreage'], "beds": result['beds'], "baths": result['baths'], "price": result['price'], "solar": "true", "electricheater": "true", "wellwater": "true", "insulation": "true"}}
      listings = requests.post(lambdaURL, json = jsonParams)
      listings = json.loads(listings.content)

      #print "Listing Text: ", listings
      return render_template("result.html", listings=listings)



@app.route('/blog')
def blog():
	return render_template('blog.html', name="its working")
