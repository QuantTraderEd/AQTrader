# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 21:56:21 2014

@author: assa
"""

import sys
import pythoncom
import pyxing as px
from PyQt4 import QtGui, QtCore
from ui_zeropositionviewer import Ui_Form

class observer_cmd:
    def Update(self,subject):       
        subject.flag = False
        pass
class observer_t0441:
    def Update(self,subject):        
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
        
        if self.XASession.data[0] != u'0000':
            self.XASession.DisconnectServer()
            return
            
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount(): 
            self.accountlist = self.XASession.GetAccountList()
        
        
    def initQuery(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():            
            self.NewQuery = px.XAQuery_t0441()
            obs = observer_t0441()
            self.NewQuery.observer = obs
            self.NewQuery.SetFieldData('t0441InBlock','accno',0,self.accountlist[0])
            self.NewQuery.SetFieldData('t0441InBlock','passwd',0,'0000')
        
        
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
            self.onReceiveData(self.NewQuery.data)
            
    def onReceiveData(self,data):
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
            
            self.updateTableWidgetItem(i-1,0,shcode)
            self.updateTableWidgetItem(i-1,1,pos)
            self.updateTableWidgetItem(i-1,6,pnl)
            
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
    
