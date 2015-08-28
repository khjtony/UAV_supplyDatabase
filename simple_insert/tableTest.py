__author__ = 'khjtony'
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide.QtCore import *
from PySide.QtGui import *


def myprint(obj, end='\n'):
    sys.stdout.write(str(obj) + end)


class cuwindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.initgui()

        self.btn_get.clicked.connect(self.test)

    def initgui(self):
        (x, y, w, h) = (500, 200, 600, 400)
        self.setGeometry(x, y, w, h)
        self.setWindowTitle('cu')

        self.btn_get = QPushButton('get', self)
        self.ltxt_reply = QLineEdit(self)
        self.btn_del = QPushButton('delete', self)

        #self.view_result = QTableWidget(5, 2, self)
        self.view_result = QTableWidget()
        self.view_result.setRowCount(5)
        self.view_result.setColumnCount(2)

        self.view_result.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view_result.setAlternatingRowColors(True)
        self.view_result.setSelectionMode(QAbstractItemView.SingleSelection)
        self.view_result.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view_result.setSortingEnabled(True)

        layout = QGridLayout()
        layout.addWidget(self.btn_get, 0, 0, 1, 1)
        layout.addWidget(self.ltxt_reply, 0, 1, 1, 1)
        layout.addWidget(self.btn_del, 0, 2, 1, 1)
        layout.addWidget(self.view_result, 1, 0, 10, 10)

        self.setLayout(layout)

    def test(self):
        ts = zip(range(5), range(5))
        rowcount = 0
        for (a, b) in ts:
            #rowcount += 1
            myprint('setitem: row=%d content=%s' % (rowcount, str((a,
                    b))))
            self.view_result.setItem(rowcount, 0,
                    QTableWidgetItem(str(a)))
            self.view_result.setItem(rowcount, 1,
                    QTableWidgetItem(str(b)))
            rowcount += 1


def main():
    app = QApplication(sys.argv)
    window = cuwindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

    # myprint('done')