# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 07:59:46 2013

@author: Administrator
"""

import os
import sys
import time
import zmq
import ctypes
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

class ConsoleObserver:
    def Update(self,subject):
        for i in xrange(len(subject.data)):
            print subject.data[i], 
        print

class MainForm(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(MainForm,self).__init__()
        self.initUI()
        self.initTIMER()
        self.initAPI()
        self.initFeedCode()
        self.initTAQFeederLst()
        self.initZMQ()
        
        self.filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\zeroetfviewer'
        self.filename = 'prevclose.txt'
        
        
    def __del__(self):
        self.XASession.DisconnectServer()
        ctypes.windll.user32.PostQuitMessage(0)
        
        
    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conn_cy = QtGui.QTableWidgetItem("conn cy")        
        self.conn_xi = QtGui.QTableWidgetItem("conn xi")
        self.status_xi = QtGui.QTableWidgetItem("ready")   
        self.status_cy = QtGui.QTableWidgetItem("ready")
        self.ui.tableWidget.setItem(0,2,self.conn_cy)
        self.ui.tableWidget.setItem(1,2,self.conn_xi)
        self.ui.tableWidget.setItem(0,1,self.status_cy)   
        self.ui.tableWidget.setItem(1,1,self.status_xi)        
        #self.ui.tableWidget.cellClicked.connect(self.cell_was_clicked)
        
    def initTIMER(self):
        self.ctimer =  QtCore.QTimer()
        self.ctimer.start(1000)
        self.ctimer.timeout.connect(self.CtimerUpdate)
        self.cybostimer = QtCore.QTimer()
        self.cybostimer.timeout.connect(self.CybosTimerUpdate)
        self.xingtimer = QtCore.QTimer()
        self.xingtimer.timeout.connect(self.XingTimerUpdate)
        self.lbltime = QtGui.QLabel(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        self.statusBar().addPermanentWidget(self.lbltime)
        
    def initAPI(self):
        self.XASession_observer = XingXASessionUpdate(proxy(self.status_xi))
        self.XASession = px.XASession()
        self.XASession.Attach(self.XASession_observer)         
        self._CpCybos = CpCybosNULL()
        
    def initFeedCode(self):
        self._FeedCodeList = FeedCodeList()
        self._FeedCodeList.ReadCodeListFile()
        
        
    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://127.0.0.1:5500")
        
    def initZMQSender(self):
        self.ZMQFuturesTradeSender = ZMQTickSender(self.socket,'xing','T','futures')
        self.ZMQFuturesQuoteSender = ZMQTickSender(self.socket,'cybos','Q','futures')
        self.ZMQFuturesExpectSender = ZMQTickSender(self.socket,'cybos','E','futures')
        self.ZMQOptionsTradeSender = ZMQTickSender(self.socket,'xing','T','options')
        self.ZMQOptionsQuoteSender = ZMQTickSender(self.socket,'cybos','Q','options')
        self.ZMQOptionsNightQuoteSender = ZMQTickSender(self.socket,'xing','Q','options')
        self.ZMQOptionsExpectSender = ZMQTickSender(self.socket,'cybos','E','options')
        self.ZMQEquityTradeSender = ZMQTickSender(self.socket,'xing','T','equity')
        self.ZMQEquityQuoteSender = ZMQTickSender(self.socket,'cybos','Q','equity')
        self.ZMQEquityExpectSender = ZMQTickSender(self.socket,'xing','E','equity')
        self.ZMQIndexExpectSender = ZMQTickSender(self.socket,'cybos','E','index')
        self.ZMQETFNAVSender = ZMQTickSender(self.socket,'xing','N','equity')
        self.obs = ConsoleObserver()
        
    def initTAQFeederLst(self):
        self.FutureTAQFeederLst = []
        self.OptionTAQFeederLst = []
        self.EquityTAQFeederLst = []
        
    def registerFeedItem_FC0(self,shcode):
        NewItemTrade = px.XAReal_FC0(shcode,'list')
        NewItemTrade.Attach(self.ZMQFuturesTradeSender)                        
        NewItemTrade.AdviseRealData()                              
        self.FutureTAQFeederLst.append(NewItemTrade)
        
    def registerFeedItem_NC0(self,shcode):
        NewItemTrade = px.XAReal_NC0(shcode,'list')
        NewItemTrade.Attach(self.ZMQFuturesTradeSender)                        
        NewItemTrade.AdviseRealData()                              
        self.FutureTAQFeederLst.append(NewItemTrade)
        
    def registerFeedItem_OC0(self,shcode):
        NewItemTrade = px.XAReal_OC0(shcode,'list')
        NewItemTrade.Attach(self.ZMQOptionsTradeSender)                        
        NewItemTrade.AdviseRealData()                              
        self.OptionTAQFeederLst.append(NewItemTrade)
        
    def registerFeedItem_EC0(self,shcode):
        NewItemTrade = px.XAReal_EC0(shcode,'list')
        NewItemTrade.Attach(self.ZMQOptionsTradeSender)                        
        NewItemTrade.AdviseRealData()                              
        self.OptionTAQFeederLst.append(NewItemTrade)
        
    def registerFeedItem_S3_(self,shcode):
        NewItemTrade = px.XAReal_S3_(shcode,'list')
        NewItemTrade.Attach(self.ZMQEquityTradeSender)                
        NewItemTrade.AdviseRealData()              
        self.EquityTAQFeederLst.append(NewItemTrade)
        
    def registerFeedItem_YS3(self,shcode):
        NewItemExpect = px.XAReal_YS3(shcode,'list')
        NewItemExpect.Attach(self.ZMQEquityExpectSender)                
        NewItemExpect.AdviseRealData()
        self.EquityTAQFeederLst.append(NewItemExpect)
        
    def registerFeedItem_I5_(self,shcode):
        NewItemNAV = px.XAReal_I5_(shcode,'list')
        NewItemNAV.Attach(self.ZMQETFNAVSender)                
        NewItemNAV.AdviseRealData()
        self.EquityTAQFeederLst.append(NewItemNAV)
        
    def registerFeedItem_FOExpect(self,shcode):        
        if shcode[:3] == '101':
            NewItemExpect = pc.FOExpectCur()
            NewItemExpect.Attach(self.ZMQFuturesExpectSender)
            NewItemExpect.SetInputValue(0,shcode[:-3])
            NewItemExpect.SetInputValue(1,'F1')
            NewItemExpect.SetInputValue(2,shcode[3:-3])
            NewItemExpect.Subscribe()  
            self.FutureTAQFeederLst.append(NewItemExpect)
        elif shcode[:3] == '201' or shcode[:3] == '301':
            NewItemOptionExpect = pc.FOExpectCur()
            NewItemOptionExpect.Attach(self.ZMQOptionsExpectSender)            
            NewItemOptionExpect.SetInputValue(0,shcode)
            NewItemOptionExpect.SetInputValue(1,'O1')
            NewItemOptionExpect.SetInputValue(2,shcode[3:-3])
            NewItemOptionExpect.Subscribe()  
            self.OptionTAQFeederLst.append(NewItemOptionExpect)
            
    def registerFeedItem_FutureJpBid(self,shcode):
        NewItemQuote = pc.FutureJpBid(shcode[:-3])
        NewItemQuote.Attach(self.ZMQFuturesQuoteSender)
        NewItemQuote.Subscribe()                    
        self.FutureTAQFeederLst.append(NewItemQuote)
        
    def registerFeedItem_CMECurr(self,shcode):
        NewItemQuote = pc.CmeCurr(shcode[:-3])
        NewItemQuote.Attach(self.ZMQFuturesQuoteSender)
        NewItemQuote.Subscribe()                    
        self.FutureTAQFeederLst.append(NewItemQuote)
        
    def registerFeedItem_OptionJpBid(self,shcode):
        NewItemQuote = pc.OptionJpBid(shcode)
        NewItemQuote.Attach(self.ZMQOptionsQuoteSender)
        NewItemQuote.Subscribe()                    
        self.OptionTAQFeederLst.append(NewItemQuote)

    def registerFeedItem_EH0(self,shcode):
        NewItemQuote = px.XAReal_EH0(shcode,'list')
        NewItemQuote.Attach(self.ZMQOptionsNightQuoteSender)
        NewItemQuote.AdviseRealData()
        self.OptionTAQFeederLst.append(NewItemQuote)
        
    def registerFeedItem_StockJpBid(self,shcode):
        NewItemQuote = pc.StockJpBid('A' + shcode)
        NewItemQuote.Attach(self.ZMQEquityQuoteSender)
        NewItemQuote.Subscribe()                
        self.EquityTAQFeederLst.append(NewItemQuote)
        
    def registerFeedItem_ExpectIndexS(self,shcode):
        NewItemExpectIndex  = pc.ExpectIndexS(shcode)
        NewItemExpectIndex.Attach(self.ZMQIndexExpectSender)
        NewItemExpectIndex.Subscribe()
        self.EquityTAQFeederLst.append(NewItemExpectIndex)
        
             
    def slot_ToggleFeed(self,boolToggle):
        pythoncom.CoInitialize()
        
        #if boolToggle: self.slot_RequestPrevClosePrice()
        self.initFeedCode()
        self.initZMQSender()
        self.initTAQFeederLst()
        
        if self.XASession.IsConnected() and boolToggle:            
            nowlocaltime = time.localtime()
            for shcode in self._FeedCodeList.futureshcodelst:                
                if nowlocaltime.tm_hour >= 6 and nowlocaltime.tm_hour < 16:                      
                    self.registerFeedItem_FC0(shcode)
                else:
                    self.registerFeedItem_NC0(shcode)
                        
            for shcode in self._FeedCodeList.optionshcodelst:
                if nowlocaltime.tm_hour >= 6 and nowlocaltime.tm_hour < 16:                      
                    self.registerFeedItem_OC0(shcode)
                else:
                    self.registerFeedItem_EC0(shcode)
                    self.registerFeedItem_EH0(shcode)
                    
            for shcode in self._FeedCodeList.equityshcodelst:
                self.registerFeedItem_S3_(shcode)
                self.registerFeedItem_YS3(shcode)   
                self.registerFeedItem_I5_(shcode)
                              
                
        if self._CpCybos.IsConnect() and boolToggle:                                    
            nowlocaltime = time.localtime()
            for shcode in self._FeedCodeList.futureshcodelst:
                if nowlocaltime.tm_hour >= 6 and nowlocaltime.tm_hour < 16:                      
                    self.registerFeedItem_FutureJpBid(shcode)                        
                else:
                    self.registerFeedItem_CMECurr(shcode)
                self.registerFeedItem_FOExpect(shcode)                  
                    
                    
            for shcode in self._FeedCodeList.optionshcodelst:
                self.registerFeedItem_OptionJpBid(shcode)
                self.registerFeedItem_FOExpect(shcode)
                                  
                
            for shcode in self._FeedCodeList.equityshcodelst:                
                self.registerFeedItem_StockJpBid(shcode)
                        
            for shcode in self._FeedCodeList.indexshcodelst:    
                self.registerFeedItem_ExpectIndexS(shcode)
                                            
        if boolToggle:
            pythoncom.PumpMessages()

        pass
    
    
    def slot_RequestPrevClosePrice(self):
        if self._CpCybos.IsConnect():
            filep = open(self.filepath + '\\' + self.filename,'w+')            
            msglist = []
            for shcode in self._FeedCodeList.futureshcodelst:
                _FutureMst = pc.FutureMst(shcode[:-3]) 
                _FutureMst.Request()
                while 1:
                    pythoncom.PumpWaitingMessages()
                    if _FutureMst.data:   
                        print shcode
                        print _FutureMst.data[22]                        
                        msglist.append(str(_FutureMst.data[22]))
                        break
                    
            for shcode in self._FeedCodeList.optionshcodelst:
                _OptionMst = pc.OptionMst(shcode)
                _OptionMst.Request()
                while 1:
                    pythoncom.PumpWaitingMessages()
                    if _OptionMst.data:
                        print shcode
                        print round(_OptionMst.data[27],2)
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
        
