
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


	query = "select * from mlsdata where (zipcode = 03755 and beds > 2 and price > 100000)"


	with conn.cursor() as cur:
		cur.execute(query)
	solarScore = cur.fetchall()




	return solarScore