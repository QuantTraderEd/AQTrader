# -*- coding: utf-8 -*-
"""
Created on Wed Jul 02 22:20:29 2014

@author: assa
"""

import time
import sys
import pythoncom
import pyxing as px
from os import path
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from zerodigitviewer_ui import Ui_Form
from weakref import proxy

xinglogindlg_dir = path.dirname(path.realpath(__file__)) + '\\..'
sys.path.append(xinglogindlg_dir)

from xinglogindlg import LoginForm


class observer_CEXAQ31200:
    def Update(self,subject):
        subject.pnl_open = 0
        subject.pnl_day = 0
        if len(subject.data) > 1:
            item = subject.data[1]
            subject.pnl_open = int((int(item['OptEvalPnlAmt'] or 0) + int(item['FutsEvalPnlAmt'] or 0)) * 0.001)
        else:
            subject.pnl_open = 0
        subject.flag = False
        pass


class observer_CFOEQ11100:
    def Update(self, subject):
        subject.pnl_day = 0
        subject.pnl_open = 0
        if len(subject.data) == 2:
            item = subject.data[1]
            # subject.pnl = int((int(item['TotAmt'] or 0)) * 0.000001)
            pnl_day = (int(item['FutsBnsplAmt'] or 0) + int(item['OptBnsplAmt'] or 0)) * 0.001
            pnl_open = (int(item['FutsEvalPnlAmt'] or 0) + int(item['OptEvalPnlAmt'] or 0)) * 0.001
            subject.pnl_day = pnl_day + pnl_open  # P/L Day
            subject.pnl_open = pnl_open
        subject.flag = False
    pass


class ZeroDigitViewer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ZeroDigitViewer, self).__init__()
        self.initUI()
        # self.initXing()
        # self.initQuery()
        # self.initTIMER()
        self.XASession = None
        self.ctimer = QtCore.QTimer()
        self.display_name = 'pnl_day'

    def closeEvent(self, event):
        self.ctimer.stop()
        if isinstance(self.XASession, px.XASession):
            self.XASession.DisconnectServer()
        event.accept()
        super(ZeroDigitViewer, self).closeEvent(event)
        
    def initUI(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("P/L Day")
        QtGui.qApp.setStyle('Cleanlooks')
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        pnl_day_action = QtGui.QAction("P/L Day", self)
        pnl_open_action = QtGui.QAction("P/L Open", self)
        self.addAction(pnl_day_action)
        self.addAction(pnl_open_action)
        pnl_day_action.triggered.connect(self.select_pnl_day)
        pnl_open_action.triggered.connect(self.select_pnl_open)
        
    def initXing(self, XASession=None):
        if isinstance(XASession, px.XASession):
            self.XASession = XASession
            if self.XASession.IsConnected() and self.XASession.GetAccountListCount(): 
                self.accountlist = self.XASession.GetAccountList()
            return

        self.XASession = px.XASession()

        myform = LoginForm(self, proxy(self.XASession))
        myform.show()
        myform.exec_()

        if self.XASession.IsConnected() and self.XASession.GetAccountListCount(): 
            self.accountlist = self.XASession.GetAccountList()
            print self.accountlist
        
    def initQuery(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            nowtime = time.localtime()
            if nowtime.tm_hour >= 7 and nowtime.tm_hour < 17:
                str_nowdt = time.strftime("%Y%m%d", nowtime)
                print str_nowdt
                self.NewQuery = px.XAQuery_CFOEQ11100()
                obs = observer_CFOEQ11100()
                self.NewQuery.observer = obs
                self.NewQuery.SetFieldData('CFOEQ11100InBlock1', 'RecCnt', 0, 1)
                self.NewQuery.SetFieldData('CFOEQ11100InBlock1', 'AcntNo', 0, self.accountlist[1])
                self.NewQuery.SetFieldData('CFOEQ11100InBlock1', 'Pwd', 0, '0000')
                self.NewQuery.SetFieldData('CFOEQ11100InBlock1', 'BnsDt', 0, str_nowdt)
            else:
                self.NewQuery = px.XAQuery_CEXAQ31200()
                obs = observer_CEXAQ31200()
                self.NewQuery.observer = obs
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1', 'RecCnt', 0, 1)
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1', 'AcntNo', 0, self.accountlist[1])
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1', 'InptPwd', 0, '0000')
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1', 'BalEvalTp', 0, '1')
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1', 'FutsPrcEvalTp', 0, '1')

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

            if self.display_name == 'pnl_day':
                self.ui.lcdNumber.display(self.NewQuery.pnl_day)
            elif self.display_name == 'pnl_open':
                self.ui.lcdNumber.display(self.NewQuery.pnl_open)

    @pyqtSlot()
    def select_pnl_day(self):
        self.display_name = 'pnl_day'
        self.setWindowTitle("P/L Day")
        pass

    @pyqtSlot()
    def select_pnl_open(self):
        self.display_name = 'pnl_open'
        self.setWindowTitle("P/L Open")
        pass


if __name__ == '__main__':    
    app = QtGui.QApplication(sys.argv)
    myform = ZeroDigitViewer()
    myform.initXing()
    myform.initQuery()
    myform.initTIMER()
    myform.show()
    app.exec_()

