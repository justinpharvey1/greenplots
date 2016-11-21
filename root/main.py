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
@app.route('/index.html')
def homepage():
  return render_template('index.html')



@app.route('/featured-eco-homes.html')
def featuredlistings():
  lambdaURL = "https://u75irk8wpe.execute-api.us-west-2.amazonaws.com/prod"
  listings = requests.post(lambdaURL)
  listings = json.loads(listings.content)

  print listings

  #Deal with badges
  for listing in listings:
    badges = listing['badges']
    if ("," in badges):
      badges = badges.split(",")
      badgeList = []
      for badge in badges:
        badgeList.append(str(badge))
      listing['badges'] = badgeList
    else:
      listing['badges'] = "null"
    print "\n" , listing['badges'], "\n"


  #Deal with images
  for listing in listings:
    images = listing['imageurls']
    if ("," in images):
      images = images.split(",")
      imageList = []
      for image in images:
        imageList.append(image)
      listing['imageurls'] = imageList
    else:
      listing['imageurls'] = "null"


  return render_template('featured-eco-homes.html', listings=listings)



@app.route('/find-your-home.html')
def findyourhome():
	return render_template('find-your-home.html', name="its working")




@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      lambdaURL = "https://nlcvv8kgd0.execute-api.us-west-2.amazonaws.com/prod"
      headers = {'Content-Type', 'application/json'}
      jsonParams = {"params": {"zipcode": result['ZipCode'], "acreage": result['Acreage'], "beds": result['Beds'], "baths": result['Baths'], "price": result['Price'], "solar": "true", "electricheater": "true", "wellwater": "true", "insulation": "true"}}
      listings = requests.post(lambdaURL, json = jsonParams)
      listings = json.loads(listings.content)

      #print "Listing Text: ", listings
      return render_template("findyourhome.html", listings=listings)



@app.route('/blog')
def blog():
	return render_template('blog.html', name="its working")
