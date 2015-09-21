__author__ = 'khjtony'

from PySide.QtGui import *
from PySide.QtCore import *
from bs4 import BeautifulSoup as bs
import wget
import os.path
import sys

crawler_app = QApplication(sys.argv)

class DigiCrawler(QWidget):
    def __init__(self):
        super(DigiCrawler, self).__init__()
        self.setWindowTitle("Digi-key Crawler")
        self.resize(300, 600)
        self.initUI()
        self.list_name = []
        self.list_value = []

    def init_url_ui(self):
        self.grpbox_url = QGroupBox('URL')
        layout = QGridLayout()
        self.url_text = QLineEdit()
        connect_btn = QPushButton("Craw")
        connect_btn.clicked.connect(self.action_craw)
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.action_exit)
        layout.addWidget(self.url_text,0,0,0,5)
        layout.addWidget(connect_btn,0,6,0,1)
        layout.addWidget(exit_btn,0,7,0,1)
        self.grpbox_url.setLayout(layout)


        pass

    def init_list_ui(self):
        self.grpbox_list = QGroupBox('Table')
        layout = QGridLayout()
        self.list_table = QTableWidget()
        layout.addWidget(self.list_table, 0, 0)
        self.grpbox_list.setLayout(layout)
        pass

    def initUI(self):
        self.init_url_ui()
        self.init_list_ui()
        total_layout = QVBoxLayout()
        total_layout.addWidget(self.grpbox_url)
        total_layout.addWidget(self.grpbox_list)
        self.setLayout(total_layout)
        return

    @Slot()
    def action_craw(self):
        url = self.url_text.text()
        if len(url) == 0:
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

        for item in big_table.find_all("tr"):
            self.list_name.append(item.th.string)
            if item.td.a is None:
                self.list_value.append(item.td.string)
            else:
                self.list_value.append(item.td.a.get("href"))

        print(len(self.list_name))
        print(len(self.list_value))

        # update table
        row_count = len(self.list_name)
        self.list_table.setRowCount(row_count)
        self.list_table.setColumnCount(2)

        for index in range(len(self.list_name)):
            self.list_table.setItem(index, 0, QTableWidgetItem(str(self.list_name[index])))
            self.list_table.setItem(index, 1, QTableWidgetItem(str(self.list_value[index])))
        self.list_table.resizeColumnsToContents()
        pass

    @Slot()
    def action_exit(self):
        crawler_app.quit()

    def run(self):
        self.show()
        crawler_app.exec_()

app = DigiCrawler()
app.run()