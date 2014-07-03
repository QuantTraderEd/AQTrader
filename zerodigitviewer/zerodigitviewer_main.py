# -*- coding: utf-8 -*-
"""
Created on Wed Jul 02 22:20:29 2014

@author: assa
"""

import sys
import pythoncom
import pyxing as px
from PyQt4 import QtGui, QtCore
from ui_zerodigitviewer import Ui_Form

class observer_cmd:
    def Update(self,subject):                
        subject.flag = False
        pass
class observer_t0441:
    def Update(self,subject):        
        item = subject.data[0]        
        subject.pnl = int(int(item['tsunik']) * 0.001)
        subject.flag = False
        pass

class ZeroDigitViewer(QtGui.QWidget):
    def __init__(self,parent=None):
        super(ZeroDigitViewer,self).__init__()
        self.initUI()
        self.initXing()
        self.initQuery()
        self.initTIMER()
        
    def initUI(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
    def initXing(self):
        self.XASession = px.XASession()
        obs = observer_cmd()        
        
        server = 'demo.etrade.co.kr'
        port = 20001
        servertype = 1      # demo server      
        showcerterror = 1
        
        user = 'eddy777'
        password = 'c9792458'
        certpw = ""        
        
        self.XASession.observer = obs
        self.XASession.ConnectServer(server,port)
        #print 'connect server'
        ret = self.XASession.Login(user,password,certpw,servertype,showcerterror)                                
        
        self.XASession.flag = True
        while self.XASession.flag:
            pythoncom.PumpWaitingMessages()
    
        self.accountlist = self.XASession.GetAccountList()
        
    def initQuery(self):
        obs = observer_t0441()
        self.NewQuery = px.XAQuery_t0441()
        self.NewQuery.observer = obs
        self.NewQuery.SetFieldData('t0441InBlock','accno',0,self.accountlist[0])
        self.NewQuery.SetFieldData('t0441InBlock','passwd',0,'0000')
        
        
    def initTIMER(self):
        self.ctimer =  QtCore.QTimer()
        self.ctimer.start(5000)
        self.ctimer.timeout.connect(self.OnTimer)
        
    def OnTimer(self):
        self.NewQuery.flag = True
        ret = self.NewQuery.Request(False)        
        while self.NewQuery.flag:
            pythoncom.PumpWaitingMessages()
        self.ui.lcdNumber.display(self.NewQuery.pnl)
        
        
        
if __name__ == '__main__':    
    app = QtGui.QApplication(sys.argv)
    myform = ZeroDigitViewer()
    myform.show()
    app.exec_()
    
