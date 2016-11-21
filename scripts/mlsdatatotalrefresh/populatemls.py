import sys
import traceback
import logging
import requests
from requests.auth import HTTPDigestAuth
import pymysql
import rds_config


def lambda_handler(event, context):
    # TODO implement
    uploadBatch()
    return 'Hello from Lambda'



def uploadBatch():


	OFFSET_COUNT = 0


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


	with conn.cursor() as cur:
		cur.execute("SELECT placeholdervalue from placeholder")
	queryData = cur.fetchall()


	OFFSET_COUNT = str(queryData[0][0])


	#Authentication 
	RETS_USERNAME = "99262idx"
	RETS_PASSWORD = "DVFGD7PSYh6yCt6RGzvf"
	RETS_LOGIN_URL = "http://neren.rets.paragonrels.com/rets/fnisrets.aspx/NEREN/login?rets-version=rets/1.8"
	loginParams = {'username': RETS_USERNAME, 'password': RETS_PASSWORD}

	session = requests.session()	

	loginResponse = session.get(RETS_LOGIN_URL, auth=HTTPDigestAuth(RETS_USERNAME, RETS_PASSWORD))
	print loginResponse.text, "\n\n"


	#Search for Properties
	RETS_SEARCH_URL = "http://neren.rets.paragonrels.com/rets/fnisrets.aspx/NEREN/search"
	searchParams = {'SearchType': 'Property', 'Class': 'RE_1', 'QueryType': 'DMQL2', 'Format': 'COMPACT-DECODED', 
	'StandardNames': '0', 'Select': 'L_ListingID, L_AskingPrice, L_Address, LM_Int1_6, LM_int4_36, L_NumAcres, LM_Char10_30, LFD_WaterHeater_36, L_Zip, LM_Int4_16, LFD_Water_35, LFD_Electric_9, LR_remarks22', 
	'Query': '(ListPrice=50000+)', 'Count': '1', 'Limit': '2500', 'Offset': OFFSET_COUNT, 'rets-version': 'rets/1.8'}
	searchResponse = session.get(RETS_SEARCH_URL, params=searchParams, auth=HTTPDigestAuth(RETS_USERNAME, RETS_PASSWORD))
	print searchResponse.text, "\n\n"


	#Parse Columns
	columns = searchResponse.text.split("<COLUMNS>")
	columns = columns[1].split("</COLUMNS>")
	columns = columns[0]
	columns = columns.split("\t")
	columns.remove("")
	columns.remove("")
	print columns
	columnDict = {}
	columnCounter = 1
	for column in columns:
		columnDict[columnCounter] = column
		columnCounter += 1
	print "column dict: ", columnDict



	#Parse Data
	dataSet = []
	data = searchResponse.text.split("<DATA>")
	data.remove(data[0])
	rowCounter = 0
	for row in data:
		row = row.split("\t")
		row.remove("")
		if "</DATA>\r\n" in row:
			row.remove("</DATA>\r\n")
		if "</DATA>\r\n<MAXROWS/>\r\n</RETS>\r\n" in row: 
			row.remove("</DATA>\r\n<MAXROWS/>\r\n</RETS>\r\n")
		if "</DATA>\r\n</RETS>\r\n" in row:
			row.remove("</DATA>\r\n</RETS>\r\n")
		print row
		columnCounter = 1
		entry = {}
		for element in row:
			if len(element) > 0:
				entry[columnDict[columnCounter]] = element
			else:
				entry[columnDict[columnCounter]] = "noData"
			columnCounter += 1
		dataSet.append(entry)

	print "data set: ", dataSet



	photoID = dataSet[0]['L_ListingID'] + ":0"

	#Add photo URL's to dataset
	#Search for Properties
	#RETS_SEARCH_URL = "http://neren.rets.paragonrels.com/rets/fnisrets.aspx/NEREN/getObject"
	#searchParams = {'Resource': 'Property', 'Location': '1', 'Type': 'Photo', 'Id': photoID , 'rets-version': 'rets/1.8'}
	#photoResponse = session.get(RETS_SEARCH_URL, params=searchParams, auth=HTTPDigestAuth(RETS_USERNAME, RETS_PASSWORD))
	#print "Photo Response: ", photoResponse.content, "\n\n"
	#http://<Paragon.rets.server.url>/rets/fnisrets.aspx/mlsid/getObject?Resource=Property&Type=Photo&Id=910131:0



	#Logout the session 
	RETS_LOGOUT_URL = "http://neren.rets.paragonrels.com/rets/fnisrets.aspx/NEREN/Logout"
	logoutParams = {'rets-version': 'rets/1.8.2'}
	logoutResponse = session.get(RETS_LOGOUT_URL, params=logoutParams, auth=HTTPDigestAuth(RETS_USERNAME, RETS_PASSWORD))
	print logoutResponse, "\n\n"





	
	#Commit listings
	cur = conn.cursor()
	for listing in dataSet:
		try:
			insertStatement = "INSERT IGNORE INTO mlsdata (listingid, price, acreage, beds, baths, address, zipcode, currentheater, greenreport, sqft, water, currentsolar, description) VALUES (" + str(listing['L_ListingID']) + "," + str(listing['L_AskingPrice']) + "," + str(listing['L_NumAcres']) + "," + str(listing['LM_Int1_6'])  + "," + str(listing['LM_int4_36']) + ",'" + str(listing['L_Address']) + "'," + str(listing['L_Zip']) + ",'" + str(listing['LFD_WaterHeater_36']) + "','" + str(listing['LM_Char10_30']) + "','" + str(listing['LM_Int4_16']) + "','" + str(listing['LFD_Water_35']) +  "','" + str(listing['LFD_Electric_9']) + "','" + str(listing['LR_remarks22']) + "')"
			print insertStatement
			cur.execute(insertStatement)
		except Exception as e:
			print "error. do nothing"


	conn.commit()


	#update offset count in db
	OFFSET_COUNT = str(int(OFFSET_COUNT) + 2500)
	updateStatement = "update placeholder set placeholdervalue = " + OFFSET_COUNT
	cur.execute(updateStatement)	
	conn.commit()


	conn.close()





