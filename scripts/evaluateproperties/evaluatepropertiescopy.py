import sys
import logging
import pymysql



def lambda_handler(event, context):
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


	query = "select * from mlsdata where listingid=4510036"
	with conn.cursor() as cur:
		cur.execute(query)
	queryData = cur.fetchall()
	counter = 0
	columns = "SHOW COLUMNS FROM mlsdata"
	with conn.cursor() as cur:
		cur.execute(columns)
	columnlist = cur.fetchall()
	data = []
	for result in queryData:
		counter = 0
		listing = {}
		for element in result:
			listing[columnlist[counter][0]] = element
			counter = counter + 1
		data.append(listing)


	for row in data:
		ecoscore = 0
		badges = []


		#Based on Certification
		if str(row['greenreport']) == "Platinum":
			ecoscore = 99
			badges.append("certified")
		if str(row['greenreport']) == "Gold":
			ecoscore = 91
			badges.append("certified")
		if str(row['greenreport']) == "Silver":
			ecoscore = 85
			badges.append("certified")
		if str(row['greenreport']) == "Certified":
			ecoscore = 79
			badges.append("certified")

		#Based on sqft
		if ecoscore == 0:
			if (int(row['sqft']) < 1000):
				ecoscore = 75
			if (1000 <= int(row['sqft']) < 2000):
				ecoscore = 65
			if (2000 <= int(row['sqft']) < 3000):
				ecoscore = 60
			if (3000 <= int(row['sqft']) < 4000):
				ecoscore = 55
			if (4000 <= int(row['sqft'])):
				ecoscore = 50


		#Add points for well water
		if ("Private" in str(row['water'])):
			badges.append("wellwater")
			ecoscore += 5
		elif ("Well" in str(row['water'])):
			badges.append("wellwater")
			ecoscore += 5


		#Add points for solar
		if ("Solar" in str(row['currentsolar'])):
			badges.append("solar")
			ecoscore += 11



		#Add points for heater
		if ("Electric" in str(row['currentheater'])):
			badges.append("electric")
			ecoscore += 11


		if (ecoscore > 99):
			ecoscore = 99


		print row
		print "\n\n"

		badgeString = ""
		for badge in badges:
			badgeString = badgeString + badge + ","
		badgeString = badgeString[:-1]


		updateStatement = "update mlsdata set ecoscore = " + str(ecoscore) + ", badges = '" + badgeString + "' where listingid = '" + str(row['listingid']) + "'"
		print updateStatement
		cursor = conn.cursor()
		cursor.execute(updateStatement)
		conn.commit()


lambda_handler(event="event", context="context")
