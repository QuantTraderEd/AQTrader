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
        self.ui.lineEditEtradeServerName.setEchoMode(QtGui.QLineEdit.Password)
        self.ui.comboBoxServerType.activated[str].connect(self.onActivated)
        self.server = 'hts.etrade.co.kr'
        self.servertype = 0
        
    def __del__(self):        
        self._XASession.observer = None
    
    def Update(self,subject):
        msg =''
        for item in subject.data:
            msg = msg + ' ' + item                
        self.ui.lineEditMessage.setText(msg)
        pass

    def onActivated(self, text):
        if text == 'real server':
            self.server = 'hts.etrade.co.kr'
            self.servertype = 0
        elif text == 'demo server':
            self.server = 'demo.etrade.co.kr'
            self.servertype = 1
        pass

        
    def slot_login(self):
        server = self.server
        port = 20001
        servertype = self.servertype
        showcerterror = 1
        user = str(self.ui.lineEditId.text())
        password = str(self.ui.lineEditPassword.text())
        certpw = str(self.ui.lineEditEtradeServerName.text())
        
        if user == '':
            user = 'eddy7777'
            password = 'c9792458'
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
