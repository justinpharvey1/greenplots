
import sys
import logging
import requests
import pymysql



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




def lambda_handler(event, context):

	#parse payload
	payload = event['body']
	params = payload["params"]
	zipCode = params['zipcode']
	acreage = params['acreage']
	beds = params['beds']
	baths = params['baths']
	price = params['price']
	hasSolar = params['solar']
	hasElectricHeater = params['electricheater']
	hasWellWater = params['wellwater']
	hasInsulation = params['insulation']


	#Dummy Payload
	#zipCode = "03755"
	#acreage = 1
	#beds = 1
	#baths = 1
	#price = "100000-1000000"


	if str(zipCode)[0] is "0":
		zipCode = zipCode[1:]
		print "zipCode: ", zipCode


	prices = price.split("-")
	lowPrice = prices[0]
	highPrice = prices[1]

	query = "select * from mlsdata where (validzipcodes LIKE '%" + str(zipCode) + "%'" + " and acreage > " + str(acreage) + " and beds > " + str(beds) + " and baths > " + str(baths) + " and price between " + str(lowPrice) + " and " + str(highPrice) + ")" + " order by ecoscore desc limit 30"
	print query

	with conn.cursor() as cur:
		cur.execute(query)
	queryData = cur.fetchall()


	columns = "SHOW COLUMNS FROM mlsdata"

	with conn.cursor() as cur:
		cur.execute(columns)
	columnlist = cur.fetchall()

	returnData = []

	for result in queryData:
		counter = 0
		listing = {}
		for element in result:
			listing[columnlist[counter][0]] = element
			counter = counter + 1
		returnData.append(listing)


	for element in returnData:
		print element



	print returnData
	return returnData

#lambda_handler(event="event",context="context")