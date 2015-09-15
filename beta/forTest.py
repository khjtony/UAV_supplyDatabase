__author__ = 'khjto'

import sys
from PySide import QtGui

class TabWidget(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super (TabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)

    def tabInserted(self, index):
        self.tabBar().setVisible(self.count() > 1)

    def tabRemoved(self, index):
        self.tabBar().setVisible(self.count() > 1)

qApp = QtGui.QApplication(sys.argv)

tab = TabWidget()

button = QtGui.QPushButton('Hello')
@button.clicked.connect
def clicked():
    tab.addTab(QtGui.QLabel('Hello'), 'Hello')

tab.addTab(button, 'Button')

layout = QtGui.QHBoxLayout()
layout.addWidget(tab)

window = QtGui.QWidget()
window.setLayout(layout)
window.resize(600, 400)
window.show()

qApp.exec_()
