# -*- coding: utf-8 -*-
"""
Created on Wed Jul 02 22:20:29 2014

@author: assa
"""

import os
import time
import sys
import pythoncom
import pyxing as px
from PyQt4 import QtGui, QtCore
from ui_zerodigitviewer import Ui_Form
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
        if len(subject.data) > 0:
            item = subject.data[0]
            if item['tsunik'] != '-':
                subject.pnl = int(int(item['tsunik'] or 0) * 0.001)
            else:
                subject.pnl = 0
        else:
            subject.pnl = 0
        subject.flag = False
        pass

class observer_CEXAQ31200:
    def Update(self,subject):
        if len(subject.data) > 1:
            item = subject.data[1]
            subject.pnl = int((int(item['OptEvalPnlAmt'] or 0) + int(item['FutsEvalPnlAmt'] or 0)) * 0.001)
        else:
            subject.pnl = 0
        subject.flag = False
        pass


class ZeroDigitViewer(QtGui.QWidget):
    def __init__(self,parent=None):
        super(ZeroDigitViewer,self).__init__()
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
                self.NewQuery = px.XAQuery_t0441()
                obs = observer_t0441()
                self.NewQuery.observer = obs
                self.NewQuery.SetFieldData('t0441InBlock','accno',0,self.accountlist[0])
                self.NewQuery.SetFieldData('t0441InBlock','passwd',0,'0302')
            else:
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
            self.ui.lcdNumber.display(self.NewQuery.pnl)
        
        
if __name__ == '__main__':    
    app = QtGui.QApplication(sys.argv)
    myform = ZeroDigitViewer()
    myform.initXing()
    myform.initQuery()
    myform.initTIMER()
    myform.show()
    app.exec_()

