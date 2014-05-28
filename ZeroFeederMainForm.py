# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 07:59:46 2013

@author: Administrator
"""

import os
import sys
import time
import zmq
import pythoncom
#import cybos_feeder

import pyxing as px
import pycybos as pc
from FeedCodeList import FeedCodeList

from PyQt4 import QtCore
from PyQt4 import QtGui
from ui_zerofeeder import Ui_MainWindow
from xinglogindlg import LoginForm
from ZMQTickSender import ZMQTickSender

from weakref import proxy

import psutil
from subprocess import Popen



class MainForm(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ctimer =  QtCore.QTimer()
        self.ctimer.start(1000)
        self.ctimer.timeout.connect(self.CtimerUpdate)
        self.cybostimer = QtCore.QTimer()
        self.cybostimer.timeout.connect(self.CybosTimerUpdate)
        self.xingtimer = QtCore.QTimer()
        self.xingtimer.timeout.connect(self.XingTimerUpdate)
        self.lbltime = QtGui.QLabel(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        self.statusBar().addPermanentWidget(self.lbltime)
        self.conn_cy = QtGui.QTableWidgetItem("conn cy")        
        self.conn_xi = QtGui.QTableWidgetItem("conn xi")
        self.status_xi = QtGui.QTableWidgetItem("ready")   
        self.status_cy = QtGui.QTableWidgetItem("ready")
        self.ui.tableWidget.setItem(0,2,self.conn_cy)
        self.ui.tableWidget.setItem(1,2,self.conn_xi)
        self.ui.tableWidget.setItem(0,1,self.status_cy)   
        self.ui.tableWidget.setItem(1,1,self.status_xi)        
        #self.ui.tableWidget.cellClicked.connect(self.cell_was_clicked)
        
        
        self._FeedCodeList = FeedCodeList()
        self._FeedCodeList.ReadCodeListFile()
        
        self.FuturesOptionTAQFeederLst = []
        self.EquityTAQFeederLst = []
        
        self.filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\zeroetfviewer'
        self.filename = 'prevclose.txt'
        
        self.XASession_observer = XingXASessionUpdate(proxy(self.status_xi))
        self.XASession = px.XASession()
        self.XASession.Attach(self.XASession_observer)
                
        self._CpCybos = CpCybosNULL()
        
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://127.0.0.1:5500")
        
    def __del__(self):
        self.XASession.DisconnectServer()
    
             
    def slot_ToggleFeed(self,boolToggle):
        pythoncom.CoInitialize()
        
        if boolToggle:
            self.slot_RequestPrevClosePrice()
        
        ZMQFuturesTradeSender = ZMQTickSender(self.socket,'xing','T','futures')
        ZMQFuturesQuoteSender = ZMQTickSender(self.socket,'cybos','Q','futures')
        ZMQFutureExpectSender = ZMQTickSender(self.socket,'cybos','E','futures')
        ZMQEquityTradeSender = ZMQTickSender(self.socket,'xing','T','equity')
        ZMQEquityQuoteSender = ZMQTickSender(self.socket,'cybos','Q','equity')
        ZMQEquityExpectSender = ZMQTickSender(self.socket,'xing','E','equity')
        ZMQIndexExpectSender = ZMQTickSender(self.socket,'cybos','E','index')
        
        
        self.FuturesOptionTAQFeederLst = []
        self.EquityTAQFeederLst = []
        
        if self.XASession.IsConnected() and boolToggle:            
            for shcode in self._FeedCodeList.futuresoptionshcodelst:
                if shcode[-3:] == '000':
                    nowlocaltime = time.localtime()
                    if nowlocaltime.tm_hour >= 6 and nowlocaltime.tm_hour < 16:                      
                        NewItemTrade = px.XAReal_FC0(shcode,'list')
                        NewItemTrade.Attach(ZMQFuturesTradeSender)                        
                        NewItemTrade.AdviseRealData()                              
                        self.FuturesOptionTAQFeederLst.append(NewItemTrade)
                    else:
                        NewItemTrade = px.XAReal_NC0(shcode,'list')
                        NewItemTrade.Attach(ZMQFuturesTradeSender)                        
                        NewItemTrade.AdviseRealData()                              
                        self.FuturesOptionTAQFeederLst.append(NewItemTrade)
                    
            for shcode in self._FeedCodeList.equityshcodelst:
                NewItemTrade = px.XAReal_S3_(shcode,'list')
                NewItemTrade.Attach(ZMQEquityTradeSender)                
                NewItemTrade.AdviseRealData()                  
                
                NewItemExprect = px.XAReal_YS3(shcode,'list')
                NewItemExprect.Attach(ZMQEquityExpectSender)                
                NewItemExprect.AdviseRealData()
                
                self.EquityTAQFeederLst.append(NewItemTrade)
                self.EquityTAQFeederLst.append(NewItemExprect)
                
                
        if self._CpCybos.IsConnect() and boolToggle:                                    
            for shcode in self._FeedCodeList.futuresoptionshcodelst:
                if shcode[-3:] == '000':
                    nowlocaltime = time.localtime()
                    if nowlocaltime.tm_hour >= 6 and nowlocaltime.tm_hour < 16:                      
                        NewItemQuote = pc.FutureJpBid(shcode[:-3])                        
                    else:
                        NewItemQuote = pc.CmeCurr(shcode[:-3])
                    NewItemQuote.Attach(ZMQFuturesQuoteSender)
                    NewItemQuote.Subscribe()                    
                    self.FuturesOptionTAQFeederLst.append(NewItemQuote)
                                        
                    NewItemExpectFutures = pc.FOExpectCur()
                    NewItemExpectFutures.Attach(ZMQFutureExpectSender)
                    NewItemExpectFutures.SetInputValue(0,shcode[:-3])
                    NewItemExpectFutures.SetInputValue(1,'F1')
                    NewItemExpectFutures.SetInputValue(2,shcode[3:-3])
                    NewItemExpectFutures.Subscribe()  
                    self.FuturesOptionTAQFeederLst.append(NewItemExpectFutures)
                
            for shcode in self._FeedCodeList.equityshcodelst:                
                NewItemQuote = pc.StockJpBid('A' + shcode)
                NewItemQuote.Attach(ZMQEquityQuoteSender)
                NewItemQuote.Subscribe()                
                self.EquityTAQFeederLst.append(NewItemQuote)
                        
            for shcode in self._FeedCodeList.indexshcodelst:    
                NewItemExpectIndex  = pc.ExpectIndexS(shcode)
                NewItemExpectIndex.Attach(ZMQIndexExpectSender)
                NewItemExpectIndex.Subscribe()
                self.EquityTAQFeederLst.append(NewItemExpectIndex)
            
            
                                    
        while self.ui.actionFeed.isChecked():
            pythoncom.PumpWaitingMessages()
        pass
    
    def slot_RequestPrevClosePrice(self):
        if self._CpCybos.IsConnect():
            filep = open(self.filepath + '\\' + self.filename,'w+')            
            msglist = []
            for shcode in self._FeedCodeList.futuresoptionshcodelst:
                _FutureMst = pc.FutureMst(shcode[:-3]) 
                _FutureMst.Request()
                while 1:
                    pythoncom.PumpWaitingMessages()
                    if _FutureMst.data:   
                        print shcode
                        print _FutureMst.data[22]                        
                        msglist.append(str(_FutureMst.data[22]))
                        break
            strshcodelist = 'A' + ',A'.join(self._FeedCodeList.equityshcodelst)                    
            _StockMst2 = pc.StockMst2(strshcodelist)            
            _StockMst2.Request()
            while 1:
                pythoncom.PumpWaitingMessages()
                if _StockMst2.data:
                    for i in xrange(_StockMst2.count):
                        print _StockMst2.data[19+30*i]                        
                        msglist.append(str(_StockMst2.data[19+30*i]))
                    break
            filep.write(','.join(msglist) + '\n')
            filep.close()        
        pass
    
    
    def slot_StartXingDlg(self,row,column):
        if row == 1 and column == 2:
            #print("Row %d and Column %d was doblueclicked" % (row,column))
            myform = LoginForm(XASession=proxy(self.XASession))
            myform.show()
            myform.exec_()
            self.xingtimer.start(1000)
            
    def slot_CheckCybosStarter(self,row,column):
        if row == 0 and column == 2:
#            if not ("DibServer.exe" in [psutil.Process(i).name for i in psutil.get_pid_list()]):
#                Popen('C:\\DAISHIN\\starter\\ncStarter.exe /prj:cp')
#            else:                
            self._CpCybos = pc.CpCybos()
            self.status_cy.setText('connect')
            self.cybostimer.start(1000)
                
            

#    def cell_was_clicked(self, row, column):
#        print("Row %d and Column %d was clicked" % (row,column))
#        #item = self.ui.tableWidget.itemAt(row,column)
        
    
    def NotifyMsg(self,msg):
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
        msg = timestamp + msg        
        #self.ui.plainTextEditMsg.appendPlainText(msg)
    

    def CtimerUpdate(self):
        self.lbltime.setText(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        
    def CybosTimerUpdate(self):
        if self._CpCybos.IsConnect():            
            if self.status_cy.text() == 'connect':
                self.status_cy.setText('connect.')
            elif self.status_cy.text() == 'connect.':
                self.status_cy.setText('connect..')
            elif self.status_cy.text() == 'connect..':
                self.status_cy.setText('connect...')
            elif self.status_cy.text() == 'connect...':
                self.status_cy.setText('connect')
        else:
            self.status_cy.setText('disconnect')
            
    def XingTimerUpdate(self):
        if self.XASession.IsConnected():
            if self.status_xi.text() == 'connect' or self.status_xi.text() == 'connect: 0000':
                self.status_xi.setText('connect.')
            elif self.status_xi.text() == 'connect.':
                self.status_xi.setText('connect..')
            elif self.status_xi.text() == 'connect..':
                self.status_xi.setText('connect...')
            elif self.status_xi.text() == 'connect...':  
                self.status_xi.setText('connect')
        else:
            self.status_xi.setText('disconnect')
            
        
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
    
class CpCybosNULL():
    def IsConnect(self):
        return False
    
if __name__ == '__main__':    
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    app.exec_()
        