# -*- coding: utf-8 -*-

import sys
import pythoncom
import pyxing as px
from weakref import proxy
from PyQt4 import QtGui

from xinglogindlg_ui import *


class LoginForm(QtGui.QDialog):
    def __init__(self, parent=None, xa_session=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_dialog()
        self.ui.setupUi(self)
        self._XASession = xa_session
        self.ui.lineEditEtradeServerName.setEchoMode(QtGui.QLineEdit.Password)
        self.ui.comboBoxServerType.activated[str].connect(self.onActivated)
        self.server = 'hts.etrade.co.kr'
        self.servertype = 0

    def __del__(self):
        self._XASession.observer = None

    def Update(self, subject):
        msg = ''
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
        # server = str(self.ui.lineEditEtradeServerName.text())
        server = self.server
        port = 20001
        servertype = self.servertype
        showcerterror = 1
        user = str(self.ui.lineEditId.text())
        password = str(self.ui.lineEditPassword.text())
        certpw = str(self.ui.lineEditEtradeServerName.text())

        if self._XASession is None:
            self._XASession = px.XASession()
        self._XASession.observer = proxy(self)
        self._XASession.ConnectServer(server, port)
        # print 'connect server'
        ret = self._XASession.Login(user, password, certpw, servertype, showcerterror)

        px.XASessionEvents.session = self._XASession
        self._XASession.flag = True
        while self._XASession.flag:
            pythoncom.PumpWaitingMessages()
        # self.ui.lineEditMessage.setText("Log")

    def slot_test(self):
        if self._XASession is not None:
            accountlist = self._XASession.GetAccountList()
            msg = ''
            for item in accountlist:
                msg = msg + ' ' + item
            self.ui.lineEditMessage.setText(msg)

            # console_viewer = ConsoleViewer()
            # xquery = px.XAQuery_CFOBQ10800()
            # xquery.observer = console_viewer
            # xquery.SetFieldData('CFOBQ10800InBlock1', 'RecCnt', 0, 1)
            # xquery.SetFieldData('CFOBQ10800InBlock1', 'PrdgrpClssCode', 0, '01')  # ProductClassCode
            # xquery.SetFieldData('CFOBQ10800InBlock1', 'ClssGrpCode', 0, '501')  # UnderlyGroupCode
            # xquery.SetFieldData('CFOBQ10800InBlock1', 'FstmmTpCode', 0, 'B')  # ExpireMonthCode
            # xquery.flag = True
            # res = xquery.Request(False)
            # while xquery.flag:
            #     pythoncom.PumpWaitingMessages()
            #     # print xquery.data[1]


# ==================== Observers ====================
class ConsoleViewer:
    def Update(self, subject):
        subject.flag = False
        print '--------' * 5
        if type(subject.data) == dict:
            for item in subject.data:
                print item, subject.data[item]
        elif type(subject.data) == list:
            for item in subject.data:
                print item
        else:
            print item
        pass


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myform = LoginForm()
    myform.show()
    sys.exit(app.exec_())
