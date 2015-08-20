__author__ = 'khjtony'
from datetime import date, datetime, timedelta
import mysql.connector as mysql

conn = mysql.connect(host='localhost', user='khjtony',password='112358',database='supply_database')
cursor = conn.cursor()

nowtime = datetime.now()

add_item = ("INSERT INTO supply_item "
               "(catagory, create_time, MountingType) "
               "VALUES (%s, %s, %s)")

data_item = ('Regulator',nowtime,'N/A')

cursor.execute(add_item, data_item)

conn.commit()
cursor.close()
conn.close()
