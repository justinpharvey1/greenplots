import xlrd
from xlrd.sheet import ctype_text   
from decimal import Decimal
from datetime import datetime, date, timedelta
import mysql.connector



NUMBER_OF_ROWS = 32243

cnx = mysql.connector.connect(user='greenplots', password='Greenplots1', host='greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com', database='greenplotsdb')



xl_workbook = xlrd.open_workbook('SolarSummaries.xlsx')
sheet_names = xl_workbook.sheet_names()
print('Sheet Names', sheet_names)

xl_sheet = xl_workbook.sheet_by_name('DNI Zip Code')


for row_idx in range(1, 32096):
	print ('-'*40)
	print ('Row: %s' % row_idx)
	zipCode = xl_sheet.cell(row_idx, 0)
	zipCode = str(zipCode)
	zipCodeParts = zipCode.split(".")
	zipCode = zipCodeParts[0]
	zipCodeParts = zipCode.split(":")
	zipCode = zipCodeParts[1]

	solarScore = xl_sheet.cell(row_idx, 2)
	solarScore = str(solarScore)

	solarScoreParts = solarScore.split(".")
	solarScoreParts2 = list(solarScoreParts[1])
	solarScoreParts3 = solarScoreParts2[0]
	solarScore = solarScoreParts[0] + "." + solarScoreParts3
	solarScoreParts = solarScore.split(":")
	solarScore = solarScoreParts[1]


	print "Zip Code: ", zipCode
	print "Solar Score: ", solarScore

	# UPDATE and INSERT statements for the old and new salary

	queryString = "INSERT INTO solardata (zipcode,solarscore) VALUES(" + str(zipCode) + "," + str(solarScore) + ");"
	cursor = cnx.cursor()
	cursor.execute(queryString)
	

	print "Added Entry"


	
	#print ('Column: [%s] cell_obj: [%s]' % (0, cell_obj))


cnx.commit()
print "done loading"


cursor.close()
cnx.close()