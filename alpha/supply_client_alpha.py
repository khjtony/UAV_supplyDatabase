__author__ = 'khjtony'
'''
 This is alpha version of supply management software suite. It only can insert new item
 and query data to local and check by their category.
 version 0.4
 '''

import datetime
import operator
import mysql.connector as mysql
import sys
from PySide.QtCore import *
from PySide.QtGui import *

supply_app = QApplication(sys.argv)


class SupplyItemModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        self.mylist = mylist
        self.header = header
        QAbstractTableModel.__init__(self, parent, *args)


    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))


class SupplyAppAlpha(QWidget):
    def __init__(self):
        super(SupplyAppAlpha, self).__init__()
        print("In __init__")
        self.initUI()
        self.header_list = []
        self.item_list = []

    def init_main_window_ui(self):
        # self.statusBar().showMessage('Welcome. Please enter username and password first.')
        self.setWindowTitle('Supply Management Suite -- Alpha v0.4')

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
        self.url_text = QLineEdit('localhost')
        url_label.setBuddy(self.url_text)
        # Add username row
        username_label = QLabel('Username: ')
        self.username_text = QLineEdit('khjtony')
        username_label.setBuddy(self.username_text)
        # Add password row
        passwd_label = QLabel('Password: ')
        self.passwd_text = QLineEdit('112358')
        self.passwd_text.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        passwd_label.setBuddy(self.passwd_text)
        # Add buttons
        self.connect_btn = QPushButton('Connect')
        self.exit_btn = QPushButton('Exit')
        self.connect_btn.clicked.connect(self.action_connect)
        self.exit_btn.clicked.connect(self.action_exit)
        # Add layout
        layout.addWidget(url_label, 0, 0)
        layout.addWidget(self.url_text, 0, 1, 1, 4)
        layout.addWidget(self.connect_btn, 0, 5)
        layout.addWidget(self.exit_btn, 0, 6)
        layout.addWidget(username_label, 1, 0)
        layout.addWidget(self.username_text, 1, 1, 1, 2)
        layout.addWidget(passwd_label, 1, 3)
        layout.addWidget(self.passwd_text, 1, 4, 1 ,6)

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
        layout = QGridLayout()
        self.category_table = QTableWidget(0, 0, self)
        layout.addWidget(self.category_table, 0, 0, 0, 2)
        self.category_table.itemClicked.connect(self.action_category_clicked)
        self.item_table = QTableView(self)
        layout.addWidget(self.item_table, 0, 3, 0, 5)
        self.grpbox_query.setLayout(layout)
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
        # total_layout.addStretch(1)
        self.setLayout(total_layout)
        return


    def method_update_category(self):
        try:
            self.sqlconn = mysql.connect(host=self.url_text.text(),
                                             user=self.username_text.text(),
                                             password=self.passwd_text.text())
            sqlcur = self.sqlconn.cursor()
            sqlcur.execute("USE supply_database")
            sqlcur.execute("SELECT category_name FROM category_list")
            self.category_name = [category_name[0] for (category_name) in sqlcur]
            # TODO: update table
            # SetRowCount
            self.category_table.setColumnCount(1)
            # SetColumnCount
            self.category_table.setRowCount(len(self.header_list)+1)
            # print("Prepare to update tablewidget")
            # Add 'ALL' category
            self.category_table.setItem(0, 0, QTableWidgetItem(str('ALL')))

            if (len(self.category_name) == 0):
                return

            for index in range(1,len(self.category_name)+1):
                # print("{} has been added at position {}".format(self.header_list[index],index), end='\n')
                self.category_table.setItem(index, 0, QTableWidgetItem(str(self.category_name[index-1])))
            # print(self.header_list)
        except:
            # TODO: connection failed exception
            print("Exception in method_update_header!")
            pass
        finally:
            # TODO: connection failed handler
            self.sqlconn.close()
            pass


    def method_update_header(self):
        try:
            self.sqlconn = mysql.connect(host=self.url_text.text(),
                                             user=self.username_text.text(),
                                             password=self.passwd_text.text())
            sqlcur = self.sqlconn.cursor()
            sqlcur.execute("USE supply_database")
            sqlcur.execute("SHOW COLUMNS FROM supply_item")
            self.header_list = [header_name[0] for (header_name) in sqlcur]
            # TODO: update table
        except:
            # TODO: connection failed exception
            print("Exception in method_update_header!")
            pass
        finally:
            # TODO: connection failed handler
            self.sqlconn.close()
            pass

    def method_update_list(self, item_category='ALL'):
        # try:
        self.method_update_header()
        self.sqlconn = mysql.connect(host=self.url_text.text(),
                                     user=self.username_text.text(),
                                     password=self.passwd_text.text())
        sqlcur = self.sqlconn.cursor()
        sqlcur.execute("USE supply_database")

        if (item_category == 'ALL'):
            sqlcur.execute("SELECT * FROM supply_item")
            items = sqlcur.fetchall()
            print(items)
            pass
        #     get all item
        else:
            query = "SELECT * FROM supply_item WHERE category={}".format(item_category)
            sqlcur.execute(query)
            items = sqlcur.fetchall()
            pass
        # get specified item
        self.item_list = items
        item_table_model = SupplyItemModel(self, self.item_list, self.header_list)
        self.item_table.setModel(item_table_model)
        self.item_table.resizeColumnsToContents()
        # TODO:update Qtablewidget
        self.sqlconn.close()
        # except:
        #     pass
        # finally:
        #     self.sqlconn.close()


    @Slot()
    def action_exit(self):
        supply_app.quit()

    @Slot()
    def action_connect(self):
        try:
            self.sqlconn = mysql.connect(host=self.url_text.text(),
                                         user=self.username_text.text(),
                                         password=self.passwd_text.text())
            self.sqlcur = self.sqlconn.cursor()
            self.connection_set_flag = True
            # print("Connection setup!")
            self.method_update_category()
        #     filling in header_list
            self.method_update_header()

        except:
            self.connection_set_flag = False

        finally:
            self.sqlconn.close()
            return


    # TODO: The problem is,  if every click needs an update, there should be a class to record selection status.
    @Slot()
    def action_view_update(self):
        # TODO: update table
        self.method_update_category()
        # TODO: update item list
        self.method_update_list()
        # TODO: update view
        return

    @Slot()
    def action_category_clicked(self):
        # TODO: finish one selection first, then do multiple selection
        items = self.category_table.selectedItems()
        item_name = items[0].text()
        self.method_update_list(item_name)

    def run(self):
        self.show()
        supply_app.exec_()

app = SupplyAppAlpha()
app.run()

