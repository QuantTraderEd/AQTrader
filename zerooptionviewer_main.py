# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 22:58:29 2014

@author: assa
"""

import sys
from PyQt4 import QtGui, QtCore
from zerooptionviewer_thread import OptionViewerThread
from ui_zerooptionviewer import Ui_MainWindow
from FeedCodeList import FeedCodeList

def convert(strprice):
    return (str(round(float(strprice),2)))


class MainForm(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.initUI()
        self.initFeedCode()
        self.initStrikeList()
        self.initTableWidget()
        self.initThread()
        
        
    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionStart.triggered.connect(self.onStart)
        
    def initFeedCode(self):
        self._FeedCodeList = FeedCodeList()
        self._FeedCodeList.ReadCodeListFile()
        for item in self._FeedCodeList.optionshcodelst:
            print item
        
    def initTableWidget(self):
        self.ui.tableWidget.resizeRowsToContents()
        self.ui.tableWidget.resizeColumnToContents(1)
        self.ui.tableWidget.resizeColumnToContents(4)
        self.ui.tableWidget.resizeColumnToContents(6)
        self.ui.tableWidget.resizeColumnToContents(9)
        self.ui.tableWidget.setItem(0,5,QtGui.QTableWidgetItem("262.5"))
        self.ui.tableWidget.setItem(1,5,QtGui.QTableWidgetItem("260"))
        self.ui.tableWidget.setItem(2,5,QtGui.QTableWidgetItem("257.5"))
        
    def initThread(self):
        self.mythread = OptionViewerThread(None)
        self.mythread.receiveData[str].connect(self.onReceiveData)
        
    def initStrikeList(self):
        self.strikelst = ['262','260','257']
        
        
    def onStart(self):
        if not self.mythread.isRunning():            
            self.mythread.start()
            print "start"
        pass
        
        
    def onReceiveData(self,msg):     
        lst = msg.split(',')
        if lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'futures':
            shcode = lst[4]                
            ask1 = convert(lst[6])
            bid1 = convert(lst[23])
            askqty1 = lst[11]
            bidqty1 = lst[28]
            showmsg = '%s, %s, %s, %s' %(askqty1,ask1,bid1,bidqty1)
            self.statusBar().showMessage(showmsg)
            
        elif lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'options':                        
            
            shcode = lst[4]                    
            ask1 = convert(lst[6])
            bid1 = convert(lst[23])
            askqty1 = lst[11]
            bidqty1 = lst[28]
            
            SHCode = QtGui.QTableWidgetItem(shcode)            
            Bid = QtGui.QTableWidgetItem(bid1)
            BidQty = QtGui.QTableWidgetItem(bidqty1)
            Ask = QtGui.QTableWidgetItem(ask1)
            AskQty = QtGui.QTableWidgetItem(askqty1)
            
            if shcode[:3] == '201':
                pos = self.strikelst.index(shcode[5:8])
                self.ui.tableWidget.setItem(pos,0,SHCode)
                self.ui.tableWidget.setItem(pos,1,AskQty)
                self.ui.tableWidget.setItem(pos,2,Ask)
                self.ui.tableWidget.setItem(pos,3,Bid)
                self.ui.tableWidget.setItem(pos,4,BidQty)                
            elif shcode[:3] == '301':
                pos = self.strikelst.index(shcode[5:8])
                self.ui.tableWidget.setItem(pos,10,SHCode)
                self.ui.tableWidget.setItem(pos,6,AskQty)
                self.ui.tableWidget.setItem(pos,7,Ask)
                self.ui.tableWidget.setItem(pos,8,Bid)
                self.ui.tableWidget.setItem(pos,9,BidQty)                
                
                    
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    app.exec_()   


