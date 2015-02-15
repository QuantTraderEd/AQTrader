# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 21:56:21 2014

@author: assa
"""

#import imp
#imp.load_source('xinglogindlg','..\\xinglogindlg.py')

import os
import time
import sys
import pythoncom
import pyxing as px
from PyQt4 import QtGui, QtCore
from ui_zeropositionviewer import Ui_Form
from weakref import proxy

xinglogindlg_dir = os.path.dirname(os.path.realpath(__file__)) + '\\..'
sys.path.append(xinglogindlg_dir)

from xinglogindlg import LoginForm

class observer_cmd:
    def Update(self,subject):       
        subject.flag = False
        pass
class observer_t0441:
    def Update(self,subject):        
        subject.flag = False
        pass

class observer_CEXAQ31200:
    def Update(self,subject):
        item = subject.data[1]
        subject.pnl = int((int(item['OptEvalPnlAmt']) + int(item['FutsEvalPnlAmt'])) * 0.001)
        subject.flag = False
        pass

class ZeroPositionViewer(QtGui.QWidget):
    def __init__(self,parent=None):
        super(ZeroPositionViewer,self).__init__()
        self.initUI()
        #self.initXing()
        #self.initQuery()
        #self.initTIMER()
        
    def initUI(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
    def initXing(self,XASession=None):
        if XASession != None:
            self.XASession = XASession
            if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
                self.accountlist = self.XASession.GetAccountList()
            return

        self.XASession = px.XASession()

        myform = LoginForm(self,proxy(self.XASession))
        myform.show()
        myform.exec_()

        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            self.accountlist = self.XASession.GetAccountList()
            print self.accountlist
        
        
    def initQuery(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():            
            nowtime = time.localtime()
            if nowtime.tm_hour >= 6 and nowtime.tm_hour < 16:
                self.exchange = 'KRX'
                self.NewQuery = px.XAQuery_t0441()
                obs = observer_t0441()
                self.NewQuery.observer = obs
                self.NewQuery.SetFieldData('t0441InBlock','accno',0,self.accountlist[0])
                self.NewQuery.SetFieldData('t0441InBlock','passwd',0,'0302')
            else:
                self.exchange = 'EUREX'
                self.NewQuery = px.XAQuery_CEXAQ31200()
                obs = observer_CEXAQ31200()
                self.NewQuery.observer = obs
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1','RecCnt',0,1)
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1','AcntNo',0,self.accountlist[0])
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1','InptPwd',0,'0302')
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1','BalEvalTp',0,'1')
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1','FutsPrcEvalTp',0,'1')
        
        
    def initTIMER(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():            
            self.ctimer =  QtCore.QTimer()
            self.ctimer.timeout.connect(self.onTimer)
            self.ctimer.start(5000)
            
        
    def onTimer(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            self.NewQuery.flag = True
            ret = self.NewQuery.Request(False)        
            while self.NewQuery.flag:
                pythoncom.PumpWaitingMessages()
            self.onReceiveData(self.exchange,self.NewQuery.data)
            
    def onReceiveData(self,exchange,data):
        if exchange == 'KRX':
            self.ui.tableWidget.setRowCount(len(data)-1)
            for i in xrange(1,len(data)):
                shcode = data[i]['expcode']
                if data[i]['medocd'] == '1':
                    pos = u'-' + data[i]['jqty']
                elif data[i]['medocd'] == '2':
                    pos = data[i]['jqty']
                else:
                    pos = ''
                pnl = data[i]['dtsunik1']
                avgprc = '%.5s'%data[i]['pamt']

                self.updateTableWidgetItem(i-1,0,shcode)
                self.updateTableWidgetItem(i-1,1,pos)
                self.updateTableWidgetItem(i-1,6,pnl)
                self.updateTableWidgetItem(i-1,7,avgprc)
        elif exchange == 'EUREX':
            self.ui.tableWidget.setRowCount(len(data)-2)
            for i in xrange(2,len(data)):
                shcode = data[i]['FnoIsuNo']
                if data[i]['BnsTpCode'] == '1':
                    pos = u'-' + data[i]['UnsttQty']
                elif data[i]['BnsTpCode'] == '2':
                    pos = data[i]['UnsttQty']
                pnl = data[i]['EvalPnl']
                avgprc = '%.5s'%data[i]['FnoAvrPrc']

                self.updateTableWidgetItem(i-2,0,shcode)
                self.updateTableWidgetItem(i-2,1,pos)
                self.updateTableWidgetItem(i-2,6,pnl)
                self.updateTableWidgetItem(i-2,7,avgprc)


            
    def updateTableWidgetItem(self,row,col,text):
        widgetItem = self.ui.tableWidget.item(row,col)
        if not widgetItem:
            NewItem = QtGui.QTableWidgetItem(text)
            #if col in self.alignRightColumnList: NewItem.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            self.ui.tableWidget.setItem(row,col,NewItem)
        else:
            widgetItem.setText(text)
        pass
                
                
        
        
if __name__ == '__main__':    
    app = QtGui.QApplication(sys.argv)
    myform = ZeroPositionViewer()
    myform.initXing()
    myform.initQuery()
    myform.initTIMER()
    myform.show()
    app.exec_()
    
