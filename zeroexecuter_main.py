# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 13:37:02 2013

@author: Administrator
"""
import sys
import time
import os

import pyxing as px
import sqlite3 as lite

from PyQt4 import QtCore, QtGui
from ui_zeroexecuter import Ui_MainWindow
from xinglogindlg import LoginForm
from zeroexecuter_thread import ExecuterThread
from orderlistdlg_main import OrderListDialog
from zerodigitviewer.zerodigitviewer_main import ZeroDigitViewer


from weakref import proxy

class MainForm(QtGui.QMainWindow):
    def __init__(self,parent=None):
        #QtGui.QWidget.__init__(self,parent)
        super(MainForm,self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ctimer = QtCore.QTimer()
        self.ctimer.start(1000)
        self.ctimer.timeout.connect(self.ctimerUpdate)
        self.labelTimer = QtGui.QLabel(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        self.xingTimer = QtCore.QTimer()
        self.xingTimer.timeout.connect(self.xingTimerUpdate)
        self.ui.statusbar.addPermanentWidget(self.labelTimer)
        
        
        self.conn_xi = QtGui.QTableWidgetItem("conn xi")
        self.status_xi = QtGui.QTableWidgetItem("ready")                   
        self.ui.tableWidget.setItem(0,2,self.conn_xi)        
        self.ui.tableWidget.setItem(0,1,self.status_xi)
        
        
        self.FuturesOptionTAQFeederLst = []
        self.EquityTAQFeederLst = []
        
        self.XASession_observer = XingXASessionUpdate(proxy(self.status_xi))
        self.XASession = px.XASession()
        self.XASession.Attach(self.XASession_observer)
        self.accountlist = []
        
        strtime = time.strftime('%Y%m%d',time.localtime())
        strdbname = "orderlist_%s.db" %(strtime)
        if not os.path.isfile(strdbname):        
            self.conn_db = lite.connect(strdbname)
            self.cursor_db = self.conn_db.cursor()
            self.cursor_db.execute("DROP TABLE IF EXISTS OrderList")
            self.cursor_db.execute("""CREATE TABLE OrderList(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                                           OrdNo TEXT,
                                           OrgOrdNo TEXT,
                                           ExecNo TEXT,
                                           Time TEXT,                  
                                           BuySell TEXT,                                       
                                           ShortCD TEXT,
                                           Price TEXT,
                                           Qty TEXT,
                                           Type1 TEXT,
                                           Type2 TEXT,
                                           ExecPrice TEXT,
                                           ExecQty TEXT,
                                           UnExecQty TEXT,
                                           ChkReq TEXT
                                           )""")
            self.conn_db.close()
        
        
        self.executerThread = ExecuterThread()
        self.executerThread._XASession = proxy(self.XASession)    
        #self.connect(self.executerThread,QtCore.SIGNAL("OnUpdateDB (QString)"),self.NotifyOrderListViewer)
        self.executerThread.threadUpdateDB.connect(self.NotifyOrderListViewer)
        
        self.myOrdListDlg = OrderListDialog()
        
        self.myDigitViewer = ZeroDigitViewer()
        
        self.ui.actionDigitView.triggered.connect(self.triggeredDigitViewer)
        
        
        
    def __del__(self):
        self.XASession.DisconnectServer()
        
    def ctimerUpdate(self):
        self.labelTimer.setText(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
                
        
    def slot_StartXingDlg(self,row,column):
        if row == 0 and column == 2:
            #print("Row %d and Column %d was doblueclicked" % (row,column))
            myform = LoginForm(self,proxy(self.XASession))
            myform.show()
            #myform.exec_()
            self.xingTimer.start(1000)
            
            if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
                self.accountlist = self.XASession.GetAccountList()
                self.executerThread._accountlist = self.accountlist
                
            
    def xingTimerUpdate(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            if self.status_xi.text() == 'connect' or self.status_xi.text() == 'connect: 0000':
                self.status_xi.setText('connect.')
            elif self.status_xi.text() == 'disconnect':
                self.status_xi.setText('connect.')
            elif self.status_xi.text() == 'connect.':
                self.status_xi.setText('connect..')
            elif self.status_xi.text() == 'connect..':
                self.status_xi.setText('connect...')
            elif self.status_xi.text() == 'connect...':
                self.status_xi.setText('connect')
        else:
            self.status_xi.setText('disconnect')
            
    def slot_ToggleExecute(self,boolToggle):
        if (not self.executerThread.isRunning()) and boolToggle: #and self.XASession.IsConnected():
            if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
                self.accountlist = self.XASession.GetAccountList()
                self.executerThread._accountlist = self.accountlist
                print  self.accountlist
                self.executerThread.start()
            else:
                self.ui.actionExecute.setChecked(False)
        elif self.executerThread.isRunning() and (not boolToggle):
            self.executerThread.terminate()
            print 'thread pause'
        pass
    
    def slot_TriggerOrderList(self):
        if not self.myOrdListDlg.isVisible():
            self.myOrdListDlg.show()
            self.myOrdListDlg.exec_()        
        pass
    
    def NotifyOrderListViewer(self):
        #update ordlistDB
        print "will update ordlistDB"
        self.myOrdListDlg.OnUpdateList()
        pass
    
    def triggeredDigitViewer(self):
        if not self.myDigitViewer.isVisible():
            self.myDigitViewer.initXing(proxy(self.XASession))
            self.myDigitViewer.initQuery()
            self.myDigitViewer.initTIMER()
            self.myDigitViewer.show()
        pass
        
        
class XingXASessionUpdate():
    def __init__(self,status_xi=None):
        self.status_xi = status_xi
    def Update(self,subject):
        msg =''
        for item in subject.data:
            msg = msg + ' ' + item                        
        if msg[:5] == ' 0000':
            self.status_xi.setText('connect:' + msg[:5])    
        pass
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myForm = MainForm()
    myForm.show()        
    app.exec_()
        
