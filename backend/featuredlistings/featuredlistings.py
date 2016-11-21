
import sys
import logging
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



	#Get listing ids
	query = "select listingid from featuredlistings"
	idString = ""
	with conn.cursor() as cur:
		cur.execute(query)
		idArray = cur.fetchall()
		for listingid in idArray:
			idString = idString + str(listingid[0]) + ","
		idString = idString[:-1]









	query = "SELECT * FROM mlsdata WHERE listingid IN (" + idString + ")"
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

	#print returnData
	return returnData



#lambda_handler(event="event", context="context")
