import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import *


"""
ZetCode PySide tutorial

This program creates a statusbar.

author: Jan Bodnar
website: zetcode.com
last edited: August 2011
"""

import sys
from PySide import QtGui

import sys
from PySide import QtGui



import datetime
import mysql.connector

cnx = mysql.connector.connect(user='khjtony', database='supply_database',password='112358')
cursor = cnx.cursor()

query = ("SELECT digi_id, create_time, amount FROM supply_item ")


cursor.execute(query)

for (digi_id, create_time, amount) in cursor:
  print("{}--{:%d %b %Y}--{}\n".format(
    digi_id,create_time, amount))

cursor.close()
cnx.close()