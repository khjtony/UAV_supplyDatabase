__author__ = 'khjtony'
'''
 This is alpha version of supply management software suite. It only can insert new item
 and query data to local and check by their category.
 version 0.1
 '''

import datetime
import mysql.connector as mysql
import sys
from PySide.QtCore import *
from PySide.QtGui import *

supply_app = QApplication(sys.argv)


class SupplyAppAlpha(QWidget):
    def __init__(self):
        super(SupplyAppAlpha, self).__init__()
        print("In __init__")
        self.initUI()

    def init_main_window_ui(self):
        # self.statusBar().showMessage('Welcome. Please enter username and password first.')
        self.setWindowTitle('Supply Management Suite -- Alpha v0.1')

        # exitaction on menu bar
        # exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        # exitAction.setShortcut('Ctrl+Q')
        # exitAction.setStatusTip('Exit application')
        # exitAction.triggered.connect(self.close)
        # menubar = self.menuBar()
        # filemenu = menubar.addMenu('&File')
        # filemenu.addAction(exitAction)

        self.setGeometry(100, 100, 500, 600)

    def init_login_ui(self):
        self.grpbox_login = QGroupBox('Login')
        layout = QGridLayout()
        # Add url row
        url_label = QLabel('URL: ')
        self.url_text = QLineEdit(self)
        url_label.setBuddy(self.url_text)
        # Add username row
        username_label = QLabel('Username: ')
        self.username_text = QLineEdit(self)
        username_label.setBuddy(self.username_text)
        # Add password row
        passwd_label = QLabel('Password: ')
        self.passwd_text = QLineEdit(self)
        self.passwd_text.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        passwd_label.setBuddy(self.passwd_text)
        # Add buttons
        self.connect_btn = QPushButton('Connect')
        self.exit_btn = QPushButton('Exit')
        self.exit_btn.clicked.connect(self.action_exit)
        # Add layout
        layout.addWidget(url_label, 0, 0)
        layout.addWidget(self.url_text, 0, 1)
        layout.addWidget(self.connect_btn, 0, 2)
        layout.addWidget(self.exit_btn, 0, 3)
        layout.addWidget(username_label, 1, 0)
        layout.addWidget(self.username_text, 1, 1)
        layout.addWidget(passwd_label, 1, 2)
        layout.addWidget(self.passwd_text, 1, 3)

        self.grpbox_login.setLayout(layout)
        return

    def init_insert_ui(self):
        self.grpbox_insert = QGroupBox('Insert')
        layout = QGridLayout()
        # Add digi_id
        digi_id_label = QLabel('digi_ID: ')
        self.digi_id_text = QLineEdit(self)
        self.digi_id_text.setPlaceholderText('e.g. 754-1851-1-ND')
        digi_id_label.setBuddy(self.digi_id_text)
        # Add category
        category_label = QLabel('Category: ')
        self.category_text = QLineEdit(self)
        self.category_text.setPlaceholderText('e.g. Regulator')
        category_label.setBuddy(self.category_text)
        # Add amount
        amount_label = QLabel('Amount: ')
        self.amount_text = QLineEdit(self)
        self.amount_text.setPlaceholderText('e.g. 100')
        amount_label.setBuddy(self.amount_text)
        # Add mountingType
        moutingtype_label = QLabel('MountingType')
        self.mountingtype = QComboBox()
        moutingtypes = ['SurfaceMount', 'ThroughHole', 'N/A']
        self.mountingtype.addItems(moutingtypes)
        # Add buttons
        self.commit_btn = QPushButton('Commit')
        # Add layout
        layout.addWidget(digi_id_label, 0, 0)
        layout.addWidget(self.digi_id_text, 0, 1)
        layout.addWidget(category_label, 0, 2)
        layout.addWidget(self.category_text, 0, 3)
        layout.addWidget(amount_label, 1, 0)
        layout.addWidget(self.amount_text, 1, 1)
        layout.addWidget(moutingtype_label, 1, 2)
        layout.addWidget(self.mountingtype, 1, 3)
        layout.addWidget(self.commit_btn, 0, 4)
        self.grpbox_insert.setLayout(layout)
        return

    def init_query_ui(self):
        self.grpbox_query = QGroupBox('Query')
        return

    def initUI(self):
        print("In initUI")
        self.init_main_window_ui()
        self.init_login_ui()
        self.init_insert_ui()
        self.init_query_ui()
        total_layout = QVBoxLayout()
        total_layout.addWidget(self.grpbox_login)
        total_layout.addWidget(self.grpbox_insert)
        total_layout.addWidget(self.grpbox_query)
        total_layout.addStretch(1)
        self.setLayout(total_layout)
        return

    @Slot()
    def action_exit(self):
        supply_app.quit()

    def run(self):
        self.show()
        supply_app.exec_()

app = SupplyAppAlpha()
app.run()

