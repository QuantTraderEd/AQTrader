# -*- coding: utf-8 -*-

import time
import sys
import pythoncom
import pyxing as px
from os import path
from PyQt4 import QtGui, QtCore
from ui_zerodigitviewer import Ui_Form
from weakref import proxy

xinglogindlg_dir = path.dirname(path.realpath(__file__)) + '\\..'
sys.path.append(xinglogindlg_dir)

from xinglogindlg import LoginForm
# from AQTrader.OrderManager.xinglogindlg import LoginForm


class observer_cmd:
    def Update(self, subject):
        subject.flag = False
    pass


class observer_t0441:
    def Update(self, subject):
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
    def Update(self, subject):
        if len(subject.data) > 1:
            item = subject.data[1]
            subject.pnl = int((int(item['OptEvalPnlAmt'] or 0) + int(item['FutsEvalPnlAmt'] or 0)) * 0.001)
        else:
            subject.pnl = 0
        subject.flag = False
    pass


class observer_CFOEQ11100:
    def Update(self, subject):
        if len(subject.data) == 2:
            item = subject.data[1]
            subject.pnl = int((int(item['EvalDpsamtTotamt'] or 0) - 100000000) * 0.001)
        else:
            subject.pnl = 0
        print 'Tot Pnl: ' + str(subject.pnl)
        subject.flag = False
    pass


class ZeroDigitViewer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ZeroDigitViewer, self).__init__()
        self.initUI()
        # self.initXing()
        # self.initQuery()
        # self.initTIMER()

    def initUI(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def initXing(self, XASession=None):
        if XASession != None:
            self.XASession = XASession
            if self.XASession.IsConnected() and self.XASession.GetAccountListCount(): 
                self.accountlist = self.XASession.GetAccountList()
            return

        self.XASession = px.XASession()

        login_form = LoginForm(self, proxy(self.XASession))
        login_form.show()
        login_form.exec_()

        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            self.accountlist = self.XASession.GetAccountList()
            print self.accountlist

    def initQuery(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            nowtime = time.localtime()
            str_nowdt = time.strftime("%Y%m%d", nowtime)
            print str_nowdt
            self.NewQuery = px.XAQuery_CFOEQ11100()
            obs = observer_CFOEQ11100()
            self.NewQuery.observer = obs
            self.NewQuery.SetFieldData('CFOEQ11100InBlock1', 'RecCnt', 0, 1)
            self.NewQuery.SetFieldData('CFOEQ11100InBlock1', 'AcntNo', 0, self.accountlist[1])
            self.NewQuery.SetFieldData('CFOEQ11100InBlock1', 'Pwd', 0, '0000')
            self.NewQuery.SetFieldData('CFOEQ11100InBlock1', 'BnsDt', 0, str_nowdt)

    def initTIMER(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            self.ctimer = QtCore.QTimer()
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

