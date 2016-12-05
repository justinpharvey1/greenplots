from math import radians, cos, sin, asin, sqrt

import xlrd
from xlrd.sheet import ctype_text   
from decimal import Decimal
from datetime import datetime, date, timedelta
import pymysql


NUMBER_OF_ROWS = 33145
AVG_EARTH_RADIUS = 6371  # in km



def haversine(point1, point2, miles=False):
    """ Calculate the great-circle distance bewteen two points on the Earth surface.

    :input: two 2-tuples, containing the latitude and longitude of each point
    in decimal degrees.

    Example: haversine((45.7597, 4.8422), (48.8567, 2.3508))

    :output: Returns the distance bewteen the two points.
    The default unit is kilometers. Miles can be returned
    if the ``miles`` parameter is set to True.

    """
    # unpack latitude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, (float(lat1), float(lng1), float(lat2), float(lng2)))

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))
    if miles:
        return h * 0.621371  # in miles
    else:
        return h  # in kilometers


def lambda_handler(event, context):

    #Open Workbook 
    xl_workbook = xlrd.open_workbook('centroids.xlsx')
    sheet_names = xl_workbook.sheet_names()
    print('Sheet Names', sheet_names)
    xl_sheet = xl_workbook.sheet_by_name('Sheet 1')


    #rds settings
    rds_host  = "greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com"
    name = "greenplots"
    password = "Greenplots1"
    db_name = "greenplotsdb"




    #Get all unique zip codes from database
    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=10)
    except:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT(zipcode) FROM mlsdata")
    results = cursor.fetchall()
    print "Zips: ", results
    print "\n\nZip1: ", results[0][0]



    #Build zipcode -> lat long dictionary 
    latlongdict = {}
    for row_idx in range(1, NUMBER_OF_ROWS):
        #print ('-'*40)
        #print ('Row: %s' % row_idx)
        latitude = xl_sheet.cell(row_idx, 0)
        latitude = str(latitude).split(":")
        latitude = latitude[1]
        longitude = xl_sheet.cell(row_idx, 1)
        longitude = str(longitude).split(":")
        longitude = longitude[1]
        zipcode = xl_sheet.cell(row_idx, 2)
        zipcode = str(zipcode).split(":")
        zipcode = zipcode[1]
        zipcode = zipcode.split(".")
        zipcode = zipcode[0]

        #print "\nvalue: ", zipcode
        for result in results: 
            if result[0] == zipcode:
                latlongdict[str(zipcode)] = [str(latitude), str(longitude)]




    for key1 in latlongdict:
        validzips = ""
        for key2 in latlongdict:
            distance = haversine(latlongdict[key1], latlongdict[key2], miles=True)
            print "Distance: ", distance
            if distance < 20:
                validzips = validzips + str(key2) + ","

        validzips = validzips[:-1]
        print "\nadjacent dicts: ", str(validzips), "\n"
        updatestatement = "update mlsdata set validzipcodes='" + validzips + "' where zipcode=" + str(key1)
        print "updatestatement: ", updatestatement
        cursor.execute(updatestatement)


    conn.commit()
    conn.close()



