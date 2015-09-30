__author__ = 'khjtony'

'''
 This is beta version of supply management software suite. It has relatively complete features that can
 login, read, insert, check logs, and etc.
 It is the last version before release version
 '''

from PySide.QtCore import *
from PySide.QtGui import *
from bs4 import BeautifulSoup as bs
import mysql.connector as mysql
import os
import sys
import operator
import wget
import re


# some global
SOFTWARE_VERSION = 0.4
MYSQL_DATABASE = 'supply_database'

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

#
# class MysqlTools(mysql):
#     """
#     This is Mysqltool box. This class can help supply client to maintain completely of database
#     when user want to insert a new item, this class receives the item information and check if
#     remote database has all the columns. If yes, just generate sql command and send it to the database.
#     If not, this class will insert a new column first and insert this item.
#     """
#     # TODO: need exception handler
#     def __init__(self):
#         raw_url = 'localhost'
#         raw_user = 'default'
#         raw_password = 'default'
#         self.url = raw_url
#         self.username = raw_user
#         self.password = raw_password
#
#         self.columns = []
#         self.values = []
#         self.conn = mysql.connect(host=self.url,
#                                   user=self.username,
#                                   password=self.password)
#         self.cur = self.conn.cursor()
#
#     def setup(self, raw_url, raw_user, raw_password):
#         self.url = raw_url
#         self.username = raw_user
#         self.password = raw_password
#
#     def test_connection(self):
#         '''
#         check connectivity
#         :return:
#         '''
#         connectivity = False
#
#
#
#         return connectivity
#
#
#     def update_columns(self):
#         '''
#         update local self.columns list to the newest version
#         need to check frequently because there may be multiple users at the same time
#         :return:
#         '''
#         pass
#
#     def get_item(self):
#         '''
#         get all the information of one item, and filter out any None columns, only show important
#         :return:
#         '''
#
#         pass
#
#     def insert_item(self, item):
#         # update columns
#         self.update_columns()
#         # check if database has all the necessary columns
#         # YES: insert item
#         # NO: insert column first, then insert item
#         pass

class MainTab(QTabWidget):
    def __init__(self):
        super(MainTab, self).__init__()
        self.setWindowTitle('Supply Management Suite --ver {}'.format(SOFTWARE_VERSION))
        self.resize(800, 600)
        self.setTabsClosable(False)
        self.init_tab_login()
        self.init_tab_insert()
        self.init_tab_query()
        self.init_tab_log()
        self.init_tab_about()
        self.isConnected = False

    def init_tab_login(self):
        self.tab_login = QWidget()
        Mainlayout = QGridLayout()

        # Definition of login group box
        grp_login = QGroupBox('Login')

        label_url = QLabel('URL: ')
        self.text_url = QLineEdit('localhost')
        label_url.setBuddy(self.text_url)

        label_user = QLabel('Username: ')
        self.text_user = QLineEdit('khjtony')
        label_user.setBuddy(self.text_user)

        label_password = QLabel('Password: ')
        self.text_password = QLineEdit('112358')
        self.text_password.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        label_password.setBuddy(self.text_password)

        self.btn_connect = QPushButton('Connect')
        self.btn_connect.clicked.connect(self.action_login_connect)
        self.btn_save = QPushButton('Save Login')
        self.btn_exit = QPushButton('Exit')
        self.btn_exit.clicked.connect(self.action_exit)

        login_layout = QGridLayout()
        login_layout.addWidget(label_url,0,0)
        login_layout.addWidget(self.text_url,0,1)
        login_layout.addWidget(self.btn_connect,0,2)
        login_layout.addWidget(label_user, 1, 0)
        login_layout.addWidget(self.text_user, 1, 1)
        login_layout.addWidget(self.btn_save, 1, 2)
        login_layout.addWidget(label_password, 2,0)
        login_layout.addWidget(self.text_password,2,1)
        login_layout.addWidget(self.btn_exit, 2, 2)


        # Definition of login status message window
        grp_terminal = QGroupBox('Login Terminal')
        self.log_terminal = QPlainTextEdit()
        self.log_terminal.setReadOnly(True)
        log_layout = QHBoxLayout()
        log_layout.addWidget(self.log_terminal)
        grp_terminal.setLayout(log_layout)

        # Definition of Login tab initialization
        grp_login.setLayout(login_layout)
        Mainlayout.addWidget(grp_login)
        Mainlayout.addWidget(grp_terminal)
        self.tab_login.setLayout(Mainlayout)
        self.addTab(self.tab_login, 'Login')

        pass

    def init_tab_insert(self):
        """
        init_tab_insert return None
        this function will be execeuted during initialization and create content for tab_insert
        tab_insert has two groups of widgets. One is quick insert, for using item by inputing Digikey \
        url. Another one is manual input group and content display window.
        :return:
        """
        self.tab_insert = QWidget()
        mainlayout = QGridLayout()
        grp_quick_insert = QGroupBox('Quick insert')
        grp_manual_insert = QGroupBox('Manual insert')

        # quick insert section
        grid_quick_insert = QHBoxLayout()
        self.text_insert_url = QLineEdit()
        btn_quick_clear = QPushButton('Clear')
        btn_quick_clear.clicked.connect(self.text_insert_url.clear)
        btn_quick_load = QPushButton('Load')
        btn_quick_load.clicked.connect(self.action_craw)
        grid_quick_insert.addWidget(self.text_insert_url)
        grid_quick_insert.addWidget(btn_quick_load)
        grid_quick_insert.addWidget(btn_quick_clear)
        grp_quick_insert.setLayout(grid_quick_insert)

        # manual insert section (quick insert helper section)
        self.table_insert = QTableWidget()
        manual_layout = QHBoxLayout()
        manual_layout.addWidget(self.table_insert)
        grp_manual_insert.setLayout(manual_layout)

        # insert, clear all
        btn_insert = QPushButton('Insert')
        btn_insert.clicked.connect(self.action_insert)
        btn_insert_clearall = QPushButton('Clear All')
        btn_insert_clearall.clicked.connect(self.action_insert_clearAll)


        mainlayout.addWidget(grp_quick_insert, 0, 0, 1, 5)
        mainlayout.addWidget(grp_manual_insert, 1, 0, 5, 5)
        mainlayout.addWidget(btn_insert, 6, 3, 1, 1)
        mainlayout.addWidget(btn_insert_clearall, 6, 4, 1, 1)
        self.tab_insert.setLayout(mainlayout)
        self.addTab(self.tab_insert, 'Insert')
        pass

    def init_tab_query(self):
        self.addTab(QWidget(), 'Query')
        pass

    def init_tab_log(self):
        self.tab_log = QWidget()
        log_layout = QVBoxLayout()
        self.text_log = QPlainTextEdit()
        self.text_log.setReadOnly(True)
        log_layout.addWidget(self.text_log)
        self.tab_log.setLayout(log_layout)
        self.addTab(self.tab_log, 'Log')

        pass

    def init_tab_about(self):
        self.tab_about = QWidget()
        tab_layout = QVBoxLayout()

        software = QLabel('Supply Management Suite -- ver {}'.format(SOFTWARE_VERSION))
        design_for = QLabel('Designed for DART in UC Davis')
        name = QLabel('Written by Hengjiu Kang\n'
                      'Electrical Engineering Student At UC Davis')
        contact = QLabel('hjkang@ucdavis.edu')

        tab_layout.addStretch(5)
        tab_layout.addWidget(software)
        tab_layout.addWidget(design_for)
        tab_layout.addStretch(1)
        tab_layout.addWidget(name)
        tab_layout.addWidget(contact)
        tab_layout.addStretch(5)
        tab_layout.setAlignment(Qt.AlignVCenter)

        self.tab_about.setLayout(tab_layout)
        QLayout.setAlignment(tab_layout, Qt.AlignCenter)
        self.addTab(self.tab_about, 'About')
        pass

    def run(self):
        self.show()
        supply_app.exec_()

    def helper_column_preprocessor(self, name):
        # print('The input string is: ', name, end='')
        name = name.replace(' ', '_')
        for letter in name:
            if not re.match('[0-9a-zA-Z_]', letter):
                name = name.replace(letter, '')
        name = name.lower()
        # print(' After process the string is: ', name)
        return name


    @Slot()
    def action_login_connect(self):
        try:
            self.conn = mysql.connect(host=self.text_url.text(), user=self.text_user.text(), password=self.text_password.text())
            self.cur = self.conn.cursor()
            self.isConnected = True
        except:
            self.isConnected = False
            print("Connecting failed")
            print("Login info is: {}, {}, {}".format(self.text_url.text(), self.text_user.text(), self.text_password.text()))

    @Slot()
    def action_exit(self):
        supply_app.quit()

    @Slot()
    def action_craw(self):
        url = self.text_insert_url.text()
        if len(url) == 0:
            print("URL is NULL!")
            return

        if (len(url)<10):
        # url is file name already
            fname = url
        else:
        # url is url
            fname = url.split('/')[-1]

        if os.path.isfile(fname):
            # file exits
            ptr = open(fname,mode='r', encoding='utf-8')
            source = ''.join(str(line) for line in ptr if "valign=top>Packaging" not in str(line))
        else:
            # file not exist
            temp = wget.download(url)
            ptr = open(temp, mode='r', encoding='utf-8')
            source = ''.join(str(line) for line in ptr if "valign=top>Packaging" not in str(line))
        ptr.close()
        soup = bs(source, 'html.parser')


        big_table = soup.find("td", class_="attributes-table-main")
        self.insert_item_name = []
        self.insert_item_value = []

        for item in big_table.find_all("tr"):
            self.insert_item_name.append(self.helper_column_preprocessor(str(item.th.string)))
            if item.td.a is None:
                self.insert_item_value.append(self.helper_column_preprocessor(str(item.td.string)))
            else:
                self.insert_item_value.append(item.td.a.get("href"))
        # update table
        row_count = len(self.insert_item_name)
        self.table_insert.setRowCount(row_count)
        self.table_insert.setColumnCount(2)

        for index in range(row_count):
            self.table_insert.setItem(index, 0, QTableWidgetItem(str(self.insert_item_name[index])))
            self.table_insert.setItem(index, 1, QTableWidgetItem(str(self.insert_item_value[index])))
        self.table_insert.resizeColumnsToContents()
        pass

    @Slot()
    def action_insert_clearAll(self):
        self.text_insert_url.clear()
        self.table_insert.clear()

    @Slot()
    def action_insert(self):
        # check connection to mysql
        if self.isConnected is False:
            self.action_login_connect()
        # check if input data is valid
        if self.table_insert.rowCount() <= 0:
            print("Insert error: Cannot insert blank item")
            return

        # check if columns are complete
        insert_columns = self.insert_item_name
        delta_columns = []
        current_columns=[]
        self.cur.execute("USE supply_database")
        self.cur.execute("SHOW COLUMNS FROM supply_database.supply_item")
        current_columns = [names[0].lower() for (names) in self.cur]
        for title in insert_columns:
            if title.lower() not in current_columns:
                delta_columns.append(title.lower())
        print(delta_columns)

        # if not: add new columns
        for title in delta_columns:
            self.cur.execute("ALTER TABLE supply_database.supply_item ADD {} VARCHAR(200)".format(title.lower()))
            print("{} has been added".format(title))

        # Now the columns are:
        self.cur.execute("SHOW COLUMNS FROM supply_database.supply_item")
        print("now the columns are: {}".format([names[0] for (names) in self.cur]))
        # if yes: goto insert
        query = self.helper_insert_formater('supply_database.supply_item', self.insert_item_name)
        # insert
        print("self.insert_imte_value is : {}".format(tuple(self.insert_item_value)))
        self.cur.execute(query, tuple(self.insert_item_value))

        self.conn.commit()
        pass

    def helper_insert_formater(self, table, names):
        query = "INSERT INTO {} ({}) VALUES ({})".format(table, ','.join(names), ','.join(["%s"]*len(names)))
        print("The query: {} will be sent to mysql server".format(query))
        return query



class SupplyAppBeta(QWidget):
    def __init__(self, parent=None):
        super(SupplyAppBeta, self).__init__(parent)

        print("In __Init__")
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Supply Management Suite -- Beta v{}'.format(SOFTWARE_VERSION))
        self.setWindowIcon(QIcon('panIAC.png'))
        self.resize(800, 600)
        self.init_tab()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        pass

    def init_tab(self):
        print('In init_tab')
        self.tabs = MainTab()

        pass



    def run(self):
        self.show()
        supply_app.exec_()

# TODO: need a mysql helper, which can guarantee that we store all the useful information in the database
# includes category test
supply_app = QApplication(sys.argv)
app = MainTab()
app.run()
