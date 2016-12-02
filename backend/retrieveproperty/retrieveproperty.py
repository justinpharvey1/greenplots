
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

	#parse payload
	payload = event['body']
	params = payload["params"]
	listingid = params['listingid']



	query = "select * from mlsdata where listingid=" + str(listingid) +  " order by ecoscore desc limit 30"
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