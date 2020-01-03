# -*- coding: utf-8 -*-

import time
import sys
import logging
import pprint
import redis
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
    # ToDo: Dulicated Query with position_viewer > reduce query_point
    @classmethod
    def Update(cls, subject):
        subject.pnl_open = 0
        subject_pnl_trade = 0
        subject.pnl_day = 0
        item = subject.data[1]
        if item['TotPnlAmt'] != '':
            subject.pnl_day = 0
        if item['BnsplAmt'] != '':
            subject.pnl_trade = long(item['BnsplAmt']) * 0.001
        if item['TotPnlAmt'] != '':
            subject.pnl_open = 0
        subject.flag = False
        pass


class observer_CCEAQ50600(object):
    # ToDo: Dulicated Query with position_viewer > reduce query_point
    @classmethod
    def Update(cls, subject):
        msg = pprint.pformat(subject.data[1])
        print msg
        subject.flag = False


class observer_CFOEQ11100(object):
    @classmethod
    def Update(cls, subject):
        subject.pnl_day = 0
        subject.pnl_open = 0
        if len(subject.data) == 2:
            item = subject.data[1]
            # 익일예탁총액 - 개장시예탁금총액
            pnl_day_test = (long(item['NtdayTotAmt'] or 0) - long(item['OpnmkDpsamtTotamt'] or 0)) * 0.001
            futures_adj_dt_amnt = (int(item['FutsAdjstDfamt'] or 0)) * 0.001
            # print "P/L Day Test: %d FutsAdjstDfamt: %d" % (pnl_day_test, futures_adj_dt_amnt)
            pnl_day = pnl_day_test
            # 선물매매손익금액 + 옵션매매손익금액 - 수수료
            pnl_trade = (long(item['FutsBnsplAmt'] or 0) + long(item['OptBnsplAmt'] or 0) - long(item['CmsnAmt'] or 0)) * 0.001
            # 선물평가손익금액 + 옵션평가손익금액
            pnl_open = (long(item['FutsEvalPnlAmt'] or 0) + long(item['OptEvalPnlAmt'] or 0)) * 0.001
            subject.pnl_day = pnl_day  # P/L Day
            subject.pnl_open = pnl_open
            subject.pnl_trade = pnl_trade
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
        self.redis_client = None

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
        pnl_trade_action = QtGui.QAction("P/L Trade", self)
        pnl_open_action = QtGui.QAction("P/L Open", self)
        self.addAction(pnl_day_action)
        self.addAction(pnl_trade_action)
        self.addAction(pnl_open_action)
        pnl_day_action.triggered.connect(self.select_pnl_day)
        pnl_trade_action.triggered.connect(self.select_pnl_trade)
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
        
    def init_query(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            nowtime = time.localtime()
            if nowtime.tm_hour >= 7 and nowtime.tm_hour < 17:
                str_nowdt = time.strftime("%Y%m%d", nowtime)
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

                self.xquery_cash = px.XAQuery_CCEAQ50600()
                obs = observer_CCEAQ50600()
                self.xquery_cash.observer = obs
                self.xquery_cash.SetFieldData('CCEAQ50600InBlock1', 'RecCnt', 0, 1)
                self.xquery_cash.SetFieldData('CCEAQ50600InBlock1', 'AcntNo', 0, self.accountlist[1])
                self.xquery_cash.SetFieldData('CCEAQ50600InBlock1', 'InptPwd', 0, '0000')
                self.xquery_cash.SetFieldData('CCEAQ50600InBlock1', 'BalEvalTp', 0, '1')
                self.xquery_cash.SetFieldData('CCEAQ50600InBlock1', 'FutsPrcEvalTp', 0, '1')

    def init_timer(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():            
            self.ctimer = QtCore.QTimer()
            self.ctimer.timeout.connect(self.on_timer)
            self.ctimer.start(5000)

    def update_cash_data(self, data):
        if not isinstance(data, list) and len(data) == 3:
            return
        data_cash = data[1]
        data_pnl_open = data[2]        
        self.xquery.pnl_open = long(data_pnl_open.replace(',', '')) * 0.001
        self.xquery.pnl_day = (long(data_cash['EvalDpsamtTotamt']) - long(data_cash['DpsamtTotamt'])) * 0.001 + self.xquery.pnl_open
        if self.display_name == 'pnl_day':
            self.ui.lcdNumber.display(self.xquery.pnl_day)
            self.logger.debug('P/L Day-> %d' % self.xquery.pnl_day)
        elif self.display_name == 'pnl_open':
            self.ui.lcdNumber.display(self.xquery.pnl_open)
            self.logger.debug('P/L Open-> %d' % self.xquery.pnl_open)

        if isinstance(self.redis_client, redis.Redis):
            self.redis_client.hset('pnl_dict', 'pnl_day', self.xquery.pnl_day)
            self.redis_client.hset('pnl_dict', 'pnl_open', self.xquery.pnl_open)

    def on_timer(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            self.xquery.flag = True
            ret = self.xquery.Request(False)
            self.logger.debug('on_timer')
            while self.xquery.flag:
                pythoncom.PumpWaitingMessages()

            nowtime = time.localtime()
            if self.display_name == 'pnl_day' and nowtime.tm_hour >= 7 and nowtime.tm_hour < 17:
                self.ui.lcdNumber.display(self.xquery.pnl_day)
                self.logger.debug('P/L Day-> %d' % self.xquery.pnl_day)
            elif self.display_name == 'pnl_trade':
                self.ui.lcdNumber.display(self.xquery.pnl_trade)
                self.logger.debug('P/L Trade-> %d' % self.xquery.pnl_trade)
            elif self.display_name == 'pnl_open':
                self.ui.lcdNumber.display(self.xquery.pnl_open)
                self.logger.debug('P/L Open-> %d' % self.xquery.pnl_open)

            if isinstance(self.redis_client, redis.Redis):
                if nowtime.tm_hour >= 7 and nowtime.tm_hour < 17:
                    self.redis_client.hset('pnl_dict', 'pnl_day', self.xquery.pnl_day)
                    self.redis_client.hset('pnl_dict', 'pnl_trade', self.xquery.pnl_trade)
                    self.redis_client.hset('pnl_dict', 'pnl_open', self.xquery.pnl_open)

    @pyqtSlot()
    def select_pnl_day(self):
        self.display_name = 'pnl_day'
        self.setWindowTitle("P/L Day")
        pass

    @pyqtSlot()
    def select_pnl_trade(self):
        self.display_name = 'pnl_trade'
        self.setWindowTitle("P/L Trade")
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
    myform.init_query()
    myform.init_timer()
    myform.show()
    app.exec_()

