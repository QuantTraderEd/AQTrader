# -*- coding: utf-8 -*-
"""
Created on Sat Jun 08 22:43:30 2013

@author: assa
"""

import sys
import win32com
import win32com.client
import pythoncom
import pyxing as px
from weakref import proxy
from PyQt4 import QtCore
from PyQt4 import QtGui

from ui_xinglogindlg import *




class LoginForm(QtGui.QDialog):
    def __init__(self, parent=None,XASession=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_dialog()
        self.ui.setupUi(self)
        self._XASession = XASession
        
    def __del__(self):        
        self._XASession.observer = None
    
    def Update(self,subject):
        msg =''
        for item in subject.data:
            msg = msg + ' ' + item                
        self.ui.lineEditMessage.setText(msg)
        pass
    
        
    def slot_login(self):
        #server = str(self.ui.lineEditEtradeServerName.text())
        server = 'demo.etrade.co.kr'
        port = 20001
        servertype = 1      # demo server      
        showcerterror = 1
        user = str(self.ui.lineEditId.text())
        password = str(self.ui.lineEditPassword.text())
        certpw = ""
        
        if user == '':
            user = 'eddy777'
            password = ''
        if self._XASession == None:
            self._XASession = px.XASession()
        self._XASession.observer = proxy(self)
        self._XASession.ConnectServer(server,port)
        #print 'connect server'
        ret = self._XASession.Login(user,password,certpw,servertype,showcerterror)
                
                
        px.XASessionEvents.session = self._XASession
        self._XASession.flag = True
        while self._XASession.flag:
            pythoncom.PumpWaitingMessages()
        #self.ui.lineEditMessage.setText("Log")
                        
        

    def slot_test(self):
        if self._XASession != None:
            accountlist = self._XASession.GetAccountList()
            msg = ''
            for item in accountlist:                
                msg = msg + ' ' +  item
            self.ui.lineEditMessage.setText(msg)
            print msg
            

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)        
    myform = LoginForm()
    myform.show()
    sys.exit(app.exec_())