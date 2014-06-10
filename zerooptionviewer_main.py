# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 22:58:29 2014

@author: assa
"""

import sys
from PyQt4 import QtGui, QtCore
from ui_zerooptionviewer import Ui_MainWindow
from FeedCodeList import FeedCodeList


class MainForm(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.initUI()
        self.initFeedCode()
        self.initTableWidget()
        
    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionStart.triggered.connect(self.onStart)
        
    def initFeedCode(self):
        self._FeedCodeList = FeedCodeList()
        self._FeedCodeList.ReadCodeListFile()
        print self._FeedCodeList.optionshcodelst
        
    def initTableWidget(self):
        self.ui.tableWidget.resizeRowsToContents()
        item = QtGui.QTableWidgetItem('Strike')
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.ui.tableWidget.setHorizontalHeaderItem(4,item)
        self.ui.tableWidget.setItem(0,4,QtGui.QTableWidgetItem("262.5"))
        self.ui.tableWidget.setItem(1,4,QtGui.QTableWidgetItem("260"))
        self.ui.tableWidget.setItem(2,4,QtGui.QTableWidgetItem("257.5"))
        
        
    def onStart(self):
        print "start"
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    app.exec_()   
        