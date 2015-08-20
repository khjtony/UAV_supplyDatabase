__author__ = 'khjtony'

from PySide.QtCore import *
from PySide.QtGui import *
import mysql.connector
import datetime
import sys


Qapp = QApplication(sys.argv)

class mainWindow(QMainWindow):
    '''
        This is GUI by python learning based on mainwindow rather than qwidge
        This program will pull content from database and show all of them in sheet
    '''
    def __init__(self):
        super(mainWindow,self).__init__()
        self.initUI()

    def initUI(self):
        return

    @Slot


    def run(self):
        self.show()
        Qapp.exec_()
        return

app = mainWindow()
app.run()

