# -*- coding: utf-8 -*-

import time
import sys
import logging
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


class observer_CEXAQ31100(object):
    @classmethod
    def Update(cls, subject):
        subject.pnl_open = 0
        subject.pnl_day = 0
        item = subject.data[1]
        if item['TotEvalAmt'] != '':
            subject.pnl_open = int(item['TotEvalAmt'])
        if item['BnsplAmt'] != '':
            subject.pnl_day = subject.pnl_open + int(item['BnsplAmt'])
        else:
            subject.pnl_day = subject.pnl_open
        subject.flag = False
        pass


class observer_CFOEQ11100(object):
    @classmethod
    def Update(cls, subject):
        subject.pnl_day = 0
        subject.pnl_open = 0
        if len(subject.data) == 2:
            item = subject.data[1]
            pnl_day_test = (int(item['NtdayTotAmt'] or 0) - int(item['OpnmkDpsamtTotamt'] or 0)) * 0.001
            futures_adj_dt_amnt = (int(item['FutsAdjstDfamt'] or 0)) * 0.001
            # print "P/L Day Test: %d FutsAdjstDfamt: %d" % (pnl_day_test, futures_adj_dt_amnt)
            pnl_day = pnl_day_test
            pnl_open = (int(item['FutsEvalPnlAmt'] or 0) + int(item['OptEvalPnlAmt'] or 0)) * 0.001
            subject.pnl_day = pnl_day + pnl_open  # P/L Day
            subject.pnl_open = pnl_open
        subject.flag = False
    pass


class ZeroDigitViewer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ZeroDigitViewer, self).__init__(parent)
        self.initUI()
        # self.initXing()
        # self.initQuery()
        # self.initTIMER()
        self.XASession = None
        self.ctimer = QtCore.QTimer()
        self.display_name = 'pnl_day'
        QtGui.qApp.setStyle('Cleanlooks')
        self.logger = logging.getLogger('ZeroOMS.DigitViewer')
        self.logger.info('Init DigitViewer')

    def closeEvent(self, event):
        self.ctimer.stop()
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
        if not isinstance(XASession, px.XASession):
            self.XASession = px.XASession()
            myform = LoginForm(self, proxy(self.XASession))
            myform.show()
            myform.exec_()
        else:
            self.XASession = XASession

        if self.XASession.IsConnected() and self.XASession.GetAccountListCount(): 
            self.accountlist = self.XASession.GetAccountList()
            self.logger.info('XASession Connected')
        else:
            self.logger.info('XASession NoConnected')
        
    def initQuery(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            nowtime = time.localtime()
            if nowtime.tm_hour >= 7 and nowtime.tm_hour < 17:
                str_nowdt = time.strftime("%Y%m%d", nowtime)
                print str_nowdt
                self.xquery = px.XAQuery_CFOEQ11100()
                obs = observer_CFOEQ11100()
                self.xquery.observer = obs
                self.xquery.SetFieldData('CFOEQ11100InBlock1', 'RecCnt', 0, 1)
                self.xquery.SetFieldData('CFOEQ11100InBlock1', 'AcntNo', 0, self.accountlist[1])
                self.xquery.SetFieldData('CFOEQ11100InBlock1', 'Pwd', 0, '0000')
                self.xquery.SetFieldData('CFOEQ11100InBlock1', 'BnsDt', 0, str_nowdt)
            else:
                self.xquery = px.XAQuery_CEXAQ31100()
                obs = observer_CEXAQ31100()
                self.xquery.observer = obs
                self.xquery.SetFieldData('CEXAQ31100InBlock1', 'RecCnt', 0, 1)
                self.xquery.SetFieldData('CEXAQ31100InBlock1', 'AcntNo', 0, self.accountlist[1])
                self.xquery.SetFieldData('CEXAQ31100InBlock1', 'InptPwd', 0, '0000')
                self.xquery.SetFieldData('CEXAQ31100InBlock1', 'BalEvalTp', 0, '1')
                self.xquery.SetFieldData('CEXAQ31100InBlock1', 'FutsPrcEvalTp', 0, '1')

    def initTIMER(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():            
            self.ctimer = QtCore.QTimer()
            self.ctimer.timeout.connect(self.onTimer)
            self.ctimer.start(5000)
        
    def onTimer(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            self.xquery.flag = True
            ret = self.xquery.Request(False)
            while self.xquery.flag:
                pythoncom.PumpWaitingMessages()

            if self.display_name == 'pnl_day':
                self.ui.lcdNumber.display(self.xquery.pnl_day)
            elif self.display_name == 'pnl_open':
                self.ui.lcdNumber.display(self.xquery.pnl_open)

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

