from flask import Flask
from flask import request
from flask import render_template
import requests
import pymysql
import sys
import logging
import json
from urlparse import urlparse
app = Flask(__name__)



@app.route('/')
@app.route('/index.html')
def homepage():
  return render_template('index.html')


@app.route('/featured-eco-homes.html')
def featuredlistings():
  lambdaURL = "https://u75irk8wpe.execute-api.us-west-2.amazonaws.com/prod"
  headers = {'Content-Type', 'application/json'}
  listings = requests.post(lambdaURL)
  listings = json.loads(listings.content)

  print listings

  listings = normalizeListingsData(listings)


  return render_template('featured-eco-homes.html', listings=listings)





@app.route('/find-your-home.html', methods= ['GET'])
def findyourhome():
  zipcode = request.args.get('zipcode', '')
  acreage = request.args.get('acreage', '')
  beds = request.args.get('beds', '')
  baths = request.args.get('baths', '')
  price = request.args.get('price', '')

  if len(zipcode) > 2:
    lambdaURL = "https://nlcvv8kgd0.execute-api.us-west-2.amazonaws.com/prod"
    headers = {'Content-Type', 'application/json'}
    jsonParams = {"params": {"zipcode": zipcode, "acreage": acreage, "beds": beds, "baths": baths, "price": price, "solar": "true", "electricheater": "true", "wellwater": "true", "insulation": "true"}}
    listings = requests.post(lambdaURL, json = jsonParams)
    listings = json.loads(listings.content)
    listings = normalizeListingsData(listings)
    print "Listings: ", listings
    return render_template('find-your-home.html', listings=listings)

  else:
    print "checkpoint"
    listings = []
    return render_template('find-your-home.html', name="its working")





@app.route('/property-single.html')
def propertysingle():

  #Get Referral Links
  rds_host  = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
  name = "greenplots"
  password = "Greenplots1"
  db_name = "greenplotsdb"
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
  try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
  except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()
  query = "select * from referrals"
  print query
  with conn.cursor() as cur:
    cur.execute(query)
  links = cur.fetchall()
  for link in links:
    print "\ lik: " +  str(link)
  print "\n\Retrieved Referral Links Successfully!!!\n\n"



  #User uploaded data
  userdata = []
  query = "select solar, water, heater, insulation, land from useruploads where mlsnumber=" + str(request.args.get('listingid')) + " and status='active'"
  with conn.cursor() as cur2: 
    cur2.execute(query)
    conn.close()
  userdata = cur2.fetchone()


  #Get listing Info
  listingid = request.args.get('listingid')
  lambdaURL = "https://cr2jk3hj7b.execute-api.us-west-2.amazonaws.com/prod"
  headers = {'Content-Type', 'application/json'}
  jsonParams = {"params": {"listingid": str(listingid)}}
  listing = requests.post(lambdaURL, json = jsonParams)
  listing = json.loads(listing.content)
  listing = normalizeListingsData(listing)
  print "\nLISTING:", listing[0]


  #for element in listing:
    #print "Element \n\n", element
  return render_template('property-single.html', listing=listing[0], userdata=userdata, waterlink=links[0][1], solarlink=links[1][1], insulationlink=links[2][1], heaterlink=links[3][1])








@app.route('/blog.html')
def blog():
  lambdaURL = "https://2axsa07n85.execute-api.us-west-2.amazonaws.com/prod"
  headers = {'Content-Type', 'application/json'}
  posts = requests.post(lambdaURL)
  posts = json.loads(posts.content)
  print posts
  return render_template('blog.html', posts=posts)






@app.route('/manage-your-listing.html', methods= ['GET'])
def manageYourListing(): 
  address = request.args.get('address', '')


  if len(address) > 2: 
    #rds settings
    rds_host  = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
    name = "greenplots"
    password = "Greenplots1"
    db_name = "greenplotsdb"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
      conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
    except:
      logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
      sys.exit()
    query = "SELECT address, zipcode, price, ecoscore, description, listingid FROM mlsdata WHERE address LIKE " + "'%" + address + "%'"
    print query
    results = []
    with conn.cursor() as cur:
      cur.execute(query)
      results = cur.fetchall()
    print "RESULTS: ", results
    conn.close()
    return render_template('manage-your-listing.html', results=results)


  else: 
    return render_template('manage-your-listing.html')




@app.route('/submit-your-listing.html', methods= ['GET'])
def submitYourListing():

  print "checkpointttt"

  name = request.args.get('name', '')
  email = request.args.get('email', '')
  user = request.args.get('user', '')
  solar = request.args.get('solar', '')
  water = request.args.get('water', '')
  heater = request.args.get('heater', '')
  insulation = request.args.get('insulation', '')
  land = request.args.get('land', '')
  mlsnumber = request.args.get('mlsnumber', '')

  rds_host  = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
  name = "greenplots"
  password = "Greenplots1"
  db_name = "greenplotsdb"
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
  try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
  except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

  query = "insert into useruploads (username, email, usertype, solar, water, heater, insulation, land, mlsnumber) values ('" + str(name) + "','" + str(email) + "','" + str(user) + "','" + str(solar) + "','" + str(water) + "','" + str(heater) + "','" + str(insulation) + "','" + str(land) + "','" + str(mlsnumber) + "')" 
  print query
  with conn.cursor() as cur:
    cur.execute(query)
  conn.commit()
  conn.close()
  return render_template('posting-successful.html')










@app.route('/supersecretadmin.html', methods= ['GET'])
def supersecretadmin():

  listingToDelete = request.args.get('listingToDelete', '')
  listingToAdd = request.args.get('listingToAdd', '')
  solarImprovementLink = request.args.get('solarImprovementLink', '')
  insulationImprovementLink = request.args.get('insulationImprovementLink', '')
  waterImprovementLink = request.args.get('waterImprovementLink', '')
  heaterImprovementLink = request.args.get('heaterImprovementLink', '')
  mlsNumber = request.args.get('mlsnumber', '')




  if (len(listingToDelete) > 1 ):
    #rds settings
    rds_host  = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
    name = "greenplots"
    password = "Greenplots1"
    db_name = "greenplotsdb"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
      conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
    except:
      logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
      sys.exit()
    query = "delete from featuredlistings where listingid=" + str(listingToDelete)
    print query
    with conn.cursor() as cur:
      cur.execute(query)
    conn.commit()
    conn.close()
    print "\n\nDelete!!!\n\n"



  if (len(listingToAdd) > 1):
    #rds settings
    rds_host  = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
    name = "greenplots"
    password = "Greenplots1"
    db_name = "greenplotsdb"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
      conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
    except:
      logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
      sys.exit()
    query = "insert into featuredlistings values (" + str(listingToAdd) + ")"
    print "query: " + query
    with conn.cursor() as cur:
      cur.execute(query)
    conn.commit()
    conn.close()
    print "\nAdd!!!\n\n"



  if (len(solarImprovementLink) > 1):
    #rds settings
    rds_host  = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
    name = "greenplots"
    password = "Greenplots1"
    db_name = "greenplotsdb"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
      conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
    except:
      logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
      sys.exit()
    query = "update referrals set url='"  + str(solarImprovementLink) + "' where title='solar'"
    print "query: " + query
    with conn.cursor() as cur:
      cur.execute(query)
    conn.commit()
    conn.close()
    print "\Solar Link Updated!!!\n\n"


  if (len(insulationImprovementLink) > 1):
    #rds settings
    rds_host  = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
    name = "greenplots"
    password = "Greenplots1"
    db_name = "greenplotsdb"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
      conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
    except:
      logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
      sys.exit()
    query = "update referrals set url='"  + str(insulationImprovementLink) + "' where title='insulation'"
    print "query: " + query
    with conn.cursor() as cur:
      cur.execute(query)
    conn.commit()
    conn.close()
    print "\Insulation Link Updated!!!\n\n"


  if (len(waterImprovementLink) > 1):
    #rds settings
    rds_host  = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
    name = "greenplots"
    password = "Greenplots1"
    db_name = "greenplotsdb"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
      conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
    except:
      logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
      sys.exit()
    query = "update referrals set url='"  + str(waterImprovementLink) + "' where title='water'"
    print "query: " + query
    with conn.cursor() as cur:
      cur.execute(query)
    conn.commit()
    conn.close()
    print "\Water Link Updated!!!\n\n"




  if (len(heaterImprovementLink) > 1):
    #rds settings
    rds_host  = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
    name = "greenplots"
    password = "Greenplots1"
    db_name = "greenplotsdb"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
      conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
    except:
      logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
      sys.exit()
    query = "update referrals set url='"  + str(heaterImprovementLink) + "' where title='heater'"
    print "query: " + query
    with conn.cursor() as cur:
      cur.execute(query)
    conn.commit()
    conn.close()
    print "\Heater Link Updated!!!\n\n" 



  if (len(mlsNumber) > 1):
    #rds settings
    rds_host  = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
    name = "greenplots"
    password = "Greenplots1"
    db_name = "greenplotsdb"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
      conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
    except:
      logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
      sys.exit()
    query = "update useruploads set status='active' where mlsnumber ="  + str(mlsNumber)
    print "query: " + query
    with conn.cursor() as cur:
      cur.execute(query)
    conn.commit()
    conn.close()
    print "\Heater Link Updated!!!\n\n"




  rds_host = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
  name = "greenplots"
  password = "Greenplots1"
  db_name = "greenplotsdb"
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
  try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
  except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

  query = "select username, email, usertype, solar, water, heater, insulation, land, mlsnumber from useruploads where status='pending'"
  results = []
  with conn.cursor() as cur:
    cur.execute(query)
    results = cur.fetchall()
  conn.close()


  if len(results) > 0:
    print "PENDING LISTINGS: ", results
    return render_template('admin.html', results=results)

  else: 
    return render_template('admin.html')










def normalizeListingsData(listings):
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


  return listings
