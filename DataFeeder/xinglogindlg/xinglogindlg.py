# -*- coding: utf-8 -*-

import pythoncom
import pyxing as px
from weakref import proxy
from PyQt4 import QtCore
from PyQt4 import QtGui

from xinglogindlg_ui import *


class LoginForm(QtGui.QDialog):
    def __init__(self, parent=None, XASession=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_dialog()
        self.ui.setupUi(self)
        QtGui.qApp.setStyle('Cleanlooks')
        self._XASession = XASession
        self.ui.lineEditEtradeServerName.setEchoMode(QtGui.QLineEdit.Password)
        self.ui.comboBoxServerType.activated[str].connect(self.onActivated)
        self.server = 'hts.etrade.co.kr'
        self.servertype = 0
        
    def __del__(self):        
        self._XASession.observer = None
    
    def update(self, subject):
        msg = ''
        for item in subject.data:
            msg = msg + ' ' + item                
        self.ui.lineEditMessage.setText(msg)
        pass

    def onActivated(self, text):
        if text == 'real server':
            self.server = 'hts.ebestsec.co.kr'
            self.servertype = 0
        elif text == 'demo server':
            self.server = 'demo.ebestsec.co.kr'
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
            return
        if not isinstance(self._XASession, px.XASession):
            self._XASession = px.XASession()
        self._XASession.observer = proxy(self)
        self._XASession.ConnectServer(server,port)
        # print 'connect server'
        ret = self._XASession.Login(user,password,certpw,servertype,showcerterror)

        px.XASessionEvents.session = self._XASession
        self._XASession.flag = True
        while self._XASession.flag:
            pythoncom.PumpWaitingMessages()
        # self.ui.lineEditMessage.setText("Log")

    def slot_test(self):
        if isinstance(self._XASession, px.XASession):
            accountlist = self._XASession.GetAccountList()
            msg = ''
            for item in accountlist:                
                msg = msg + ' ' + item
            self.ui.lineEditMessage.setText(msg)
            print msg
            

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)        
    myform = LoginForm()
    myform.show()
    sys.exit(app.exec_())
