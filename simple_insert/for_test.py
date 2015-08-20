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

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PySide tutorial

This program creates a toolbar.

author: Jan Bodnar
website: zetcode.com
last edited: August 2011
"""

import sys
from PySide import QtGui


#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import sys
from PySide.QtCore import *
from PySide.QtGui import *


class Form(QDialog):

def ''init''(self, parent=None):
 super(Form, self).''init''(parent)
 # Create widgets
 self.edit = QLineEdit("Write my name here")
 self.button = QPushButton("Show Greetings")
 # Create layout and add widgets
 layout = QVBoxLayout()
 layout.addWidget(self.edit)
 layout.addWidget(self.button)
 # Set dialog layout
 self.setLayout(layout)
 # Add button signal to greetings slot
 self.button.clicked.connect(self.greetings)

# Greets the user
 def greetings(self):
 print ("Hello s" self.edit.text())

if ''name'' == '''main''':
 # Create the Qt Application
 app = QApplication(sys.argv)
 # Create and show the form
 form = Form()
 form.show()
 # Run the main Qt loop
 sys.exit(app.exec_())
