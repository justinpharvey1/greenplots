
from decimal import Decimal
from datetime import datetime, date, timedelta

import mysql.connector

cnx = mysql.connector.connect(user='greenplots', password='Greenplots1', host='greenplots.cqd6sxiozckk.us-west-2.rds.amazonaws.com', database='greenplotsdb')



# UPDATE and INSERT statements for the old and new salary
updateData = ("INSERT INTO solardata (zipcode,solarscore) VALUES (10,100);")


cursor = cnx.cursor()
cursor.execute(updateData)
cnx.commit()


cursor.close()
cnx.close()