import requests

import sys
import logging
import rds_config
import pymysql


#rds settings
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




def lambda_handler(event, context):



	payload = event['body']
	properties = payload['properties']



	#Solar data 
	with conn.cursor() as cur:
		cur.execute("select solarscore from solardata where zipcode = 03755")
	solarScore = cur.fetchone()



	#Utility data
	UTILITY_SCORE_KEY = '8wfxqbwq'
	UTILITY_SCORE_URL = 'http://api.myutilityscore.com/getutilityscore'
	requestHeaders = {'Api-Key':UTILITY_SCORE_KEY}
	utilityData = requests.post(UTILITY_SCORE_URL, headers = requestHeaders, data = {"has_property_data":True})



	#Air quality data 
	AIR_SCORE_KEY = 'ADED5391-1CE4-418E-83B2-4677E364793C'
	AIR_SCORE_URL = 'http://www.airnowapi.org/aq/observation/latLong/current'
	airDataParams = {'format': 'application/json', 'latitude': '38.3651', 'longitude': '-114.4141', 'distance': '100', 'API_KEY': AIR_SCORE_KEY}
	airData = requests.get(AIR_SCORE_URL, params=airDataParams)
	airScore = airData.json()[0]["Category"]["Name"]



	#Rainfall data
	RAINFALL_URL = 'https://www.melissadata.com/lookups/ZipWeather.asp?ZipCode=03755&submit1=Submit'
	rainfallData = requests.get(RAINFALL_URL)
	rainfallHTML = rainfallData.text
	rainfallParts = rainfallHTML.split("Yearly Total")
	rainfallParts = rainfallParts[1].split(">")
	rainfallParts = rainfallParts[9].split("<")
	annualRainfall = rainfallParts[0]


	
	#Plantmaps link generator
	#Example link below
	#http://www.plantmaps.com/interactive-texas-usda-plant-zone-hardiness-map.php?ZS=75229



	return solarScore