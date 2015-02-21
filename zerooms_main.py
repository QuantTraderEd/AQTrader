# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 13:37:02 2013

@author: Administrator
"""

import sys
import time
import os
import pythoncom

import logging
import pyxing as px
import sqlite3 as lite

from PyQt4 import QtCore, QtGui
from ui_zerooms import Ui_MainWindow
from xinglogindlg import LoginForm
from zerooms_thread import ExecuterThread
from orderlistdlg_main import OrderListDialog
from zerodigitviewer.zerodigitviewer_main import ZeroDigitViewer, observer_t0441, observer_CEXAQ31200
from zeropositionviewer.zeropositionviewer import ZeroPositionViewer

from weakref import proxy

logger = logging.getLogger('ZeroOMS')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('ZeroOMS.log')
#fh = logging.Handlers.RotatingFileHandler('ZeroOMS.log',maxBytes=104857,backupCount=3)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)

class MainForm(QtGui.QMainWindow):
    def __init__(self,parent=None):
        #QtGui.QWidget.__init__(self,parent)
        super(MainForm,self).__init__(parent)

        self.initUI()

        self.ctimer = QtCore.QTimer()
        self.ctimer.start(1000)
        self.ctimer.timeout.connect(self.ctimerUpdate)

        self.xingTimer = QtCore.QTimer()
        self.xingTimer.timeout.connect(self.xingTimerUpdate)
        self.queryTimer = QtCore.QTimer()
        self.queryTimer.timeout.connect(self.queryTimerUpdate)
        
        self.FuturesOptionTAQFeederLst = []
        self.EquityTAQFeederLst = []
        
        self.XASession_observer = XingXASessionUpdate(proxy(self.status_xi))
        self.XASession = px.XASession()
        self.XASession.Attach(self.XASession_observer)
        self.accountlist = []
        self.servername = ''
        
        self.initDB()        
        
        self.executerThread = ExecuterThread()
        self.executerThread._XASession = proxy(self.XASession)    
        #self.connect(self.executerThread,QtCore.SIGNAL("OnUpdateDB (QString)"),self.NotifyOrderListViewer)
        self.executerThread.threadUpdateDB.connect(self.NotifyOrderListViewer)
        self.executerThread.finished.connect(self.NotifyThreadEnd)


        logger.info('Start ZeroOMS')

    def closeEvent(self, event):
        self.XASession.DisconnectServer()
        setting = QtCore.QSettings("ZeroOMS.ini",QtCore.QSettings.IniFormat)
        setting.setValue("OMS_Geometry",self.saveGeometry())
        setting.setValue("OrdListDlg_Geometry",self.myOrdListDlg.saveGeometry())
        setting.setValue("PositionViewer_Geometry",self.myPositionViewer.saveGeometry())
        setting.setValue("DigitViewer_Geometry",self.myDigitViewer.saveGeometry())
        self.myOrdListDlg.close()
        self.myPositionViewer.close()
        self.myDigitViewer.close()
        logger.info("Close ZeroOMS")

    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.labelTimer = QtGui.QLabel(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        self.ui.statusbar.addPermanentWidget(self.labelTimer)

        self.conn_xi = QtGui.QTableWidgetItem("conn xi")
        self.status_xi = QtGui.QTableWidgetItem("ready")
        self.ui.tableWidget.setItem(0,2,self.conn_xi)
        self.ui.tableWidget.setItem(0,1,self.status_xi)

        self.myOrdListDlg = OrderListDialog()
        self.myPositionViewer = ZeroPositionViewer()
        self.myDigitViewer = ZeroDigitViewer()

        self.ui.actionDigitView.triggered.connect(self.triggeredDigitViewer)
        self.ui.actionPositionView.triggered.connect(self.trigeredPositionViewer)

        setting = QtCore.QSettings("ZeroOMS.ini",QtCore.QSettings.IniFormat)
        self.restoreGeometry(setting.value("OMS_Geometry").toByteArray())
        self.myOrdListDlg.restoreGeometry(setting.value("OrdListDlg_Geometry").toByteArray())
        self.myPositionViewer.restoreGeometry(setting.value("PositionViewer_Geometry").toByteArray())
        self.myDigitViewer.restoreGeometry(setting.value("DigitViewer_Geometry").toByteArray())

    def initDB(self):
        nowtime = time.localtime()
        strtime = time.strftime('%Y%m%d',nowtime)
        if nowtime.tm_hour >= 6 and nowtime.tm_hour < 16:
            strdbname = "orderlist_%s.db" %(strtime)
        elif nowtime.tm_hour >= 16:
            strdbname = "orderlist_night_%s.db" %(strtime)
        elif nowtime.tm_hour < 6:
            strtime = "%d%.2d%.2d" %(nowtime.tm_year,nowtime.tm_mon,nowtime.tm_mday-1)
            strdbname = "orderlist_night_%s.db" %(strtime)
            
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
            logger.info('Init New OrdList DB File')

        


    def initQuery(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            nowtime = time.localtime()
            if nowtime.tm_hour >= 6 and nowtime.tm_hour < 16:
                self.exchange = 'KRX'
                logger.info(self.exchange)
                self.NewQuery = px.XAQuery_t0441()
                obs = observer_t0441()
                self.NewQuery.observer = obs
                self.NewQuery.SetFieldData('t0441InBlock','accno',0,self.accountlist[0])
                if self.servername[:3] == 'MIS':
                    self.NewQuery.SetFieldData('t0441InBlock','passwd',0,'0000')
                elif self.servername[0] == 'X':
                    # it need the real account pw
                    self.NewQuery.SetFieldData('t0441InBlock','passwd',0,'0302')
            else:
                self.exchange = 'EUREX'
                logger.info(self.exchange)
                self.NewQuery = px.XAQuery_CEXAQ31200()
                obs = observer_CEXAQ31200()
                self.NewQuery.observer = obs
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1','RecCnt',0,1)
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1','AcntNo',0,self.accountlist[0])
                if self.servername[:3] == 'MIS':
                    self.NewQuery.SetFieldData('CEXAQ31200InBlock1','InptPwd',0,'0000')
                elif self.servername[0] == 'X':
                    # it need the real account pw
                    self.NewQuery.SetFieldData('CEXAQ31200InBlock1','InptPwd',0,'0302')
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1','BalEvalTp',0,'1')
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1','FutsPrcEvalTp',0,'1')
        
    def ctimerUpdate(self):
        self.labelTimer.setText(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        
            
    def queryTimerUpdate(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount() and self.NewQuery != None:
            self.NewQuery.flag = True
            ret = self.NewQuery.Request(False)        
            while self.NewQuery.flag:
                pythoncom.PumpWaitingMessages()
            self.myDigitViewer.ui.lcdNumber.display(self.NewQuery.pnl)
            self.myPositionViewer.onReceiveData(self.exchange,self.NewQuery.data)
                
        
    def slot_StartXingDlg(self,row,column):
        if row == 0 and column == 2:
            #print("Row %d and Column %d was doblueclicked" % (row,column))
            myform = LoginForm(self,proxy(self.XASession))
            myform.show()
            #myform.exec_()
            self.xingTimer.start(1000)
            
            
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
                self.servername = self.XASession.GetServerName()
                self.accountlist = self.XASession.GetAccountList()
                self.executerThread._accountlist = self.accountlist
                self.executerThread._servername = self.servername
                #print  self.servername, self.accountlist
                logmsg = '%s   %s'%(self.servername,self.accountlist[0])
                logger.info(logmsg)
                self.initQuery()
                self.queryTimer.start(10000)
                self.executerThread.start()
                logger.info('Thread start')
            else:
                self.ui.actionExecute.setChecked(False)
        elif self.executerThread.isRunning() and (not boolToggle):
            self.executerThread.terminate()
            logger.info('Thread stop')
        pass

    def NotifyThreadEnd(self):
        self.ui.actionExecute.setChecked(False)
        logger.info('Thread finished')
        pass
    
    def slot_TriggerOrderList(self):
        if not self.myOrdListDlg.isVisible():
            self.myOrdListDlg.show()
            self.myOrdListDlg.exec_()        
        pass


    def NotifyOrderListViewer(self):
        #update ordlistDB
        logger.info('will update ordlistDB')
        self.myOrdListDlg.OnUpdateList()
        pass
    
    def triggeredDigitViewer(self):
        if not self.myDigitViewer.isVisible():
            self.myDigitViewer.show()
        pass
    
    def trigeredPositionViewer(self):
        if not self.myPositionViewer.isVisible():
            self.myPositionViewer.show()
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
        
