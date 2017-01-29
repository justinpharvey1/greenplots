import sys
import traceback
import logging
import requests
from requests.auth import HTTPDigestAuth
import pymysql
import rds_config
import json


def lambda_handler(event, context):
    # TODO implement
    uploadBatch()
    return 'Hello from Lambda'



def uploadBatch():



	#Post Data to MySQL
	rds_host  = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
	name = rds_config.db_username
	password = rds_config.db_password
	db_name = rds_config.db_name

	logger = logging.getLogger()
	logger.setLevel(logging.INFO)



	try:
		conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
	except:
		logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
		sys.exit()


	with conn.cursor() as cursor:
		query = "select listingid from mlsdata where imageurls is null limit 50"
		cursor.execute(query)

		properties = cursor.fetchall()
		print "properties: ", properties




	#Authentication 
	RETS_USERNAME = "99262idx"
	RETS_PASSWORD = "DVFGD7PSYh6yCt6RGzvf"
	RETS_LOGIN_URL = "http://neren.rets.paragonrels.com/rets/fnisrets.aspx/NEREN/login?rets-version=rets/1.8"
	loginParams = {'username': RETS_USERNAME, 'password': RETS_PASSWORD}

	session = requests.session()	

	loginResponse = session.get(RETS_LOGIN_URL, auth=HTTPDigestAuth(RETS_USERNAME, RETS_PASSWORD))
	print loginResponse.text, "\n\n"


	#Add each 
	for listingid in properties:

		photoID = str(listingid[0]) + ":*"

		print "listing: ", photoID + "\n"

		imagesString = ""

		#Add photo URL's to dataset
		RETS_SEARCH_URL = "http://neren.rets.paragonrels.com/rets/fnisrets.aspx/NEREN/getObject"
		searchParams = {'Resource': 'Property', 'Location': '1', 'Type': 'Photo', 'Id': photoID , 'rets-version': 'rets/1.8'}
		photoResponse = session.get(RETS_SEARCH_URL, params=searchParams, auth=HTTPDigestAuth(RETS_USERNAME, RETS_PASSWORD))
		print "Photo Response: ", photoResponse.text, "\n\n"

		#If no images for property
		if ( "Location: " not in photoResponse.text):
			with conn.cursor() as cursor:
				updateStatement = "update mlsdata set imageurls = '" + "noImages" + "' where listingid = " + str(listingid[0])
				print "update statement: ", updateStatement
				cursor.execute(updateStatement)
			continue


		images = photoResponse.text.split("Location: ")

		print "IMAGE COUNT: ", len(images)

		flag = 0
		for image in images:
			if flag == 0:
				flag += 1
				continue
			location = image.split(".JPG")
			location = location[0]
			location = location + ".JPG"
			print "LOCATION>>>>>> ", location
			imagesString = imagesString + location + ","
		imagesString = imagesString[:-1]


		#Add URL array to database
		with conn.cursor() as cursor:
			updateStatement = "update mlsdata set imageurls = '" + imagesString + "' where listingid = " + str(listingid[0])
			print "update statement: ", updateStatement
			cursor.execute(updateStatement)


	#Logout the session 
	RETS_LOGOUT_URL = "http://neren.rets.paragonrels.com/rets/fnisrets.aspx/NEREN/Logout"
	logoutParams = {'rets-version': 'rets/1.8.2'}
	logoutResponse = session.get(RETS_LOGOUT_URL, params=logoutParams, auth=HTTPDigestAuth(RETS_USERNAME, RETS_PASSWORD))
	print logoutResponse, "\n\n"




	conn.commit()
	conn.close()