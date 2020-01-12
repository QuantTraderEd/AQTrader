# -*- coding: utf-8 -*-

import time
import sys
import logging
import pythoncom
import datetime as dt
import pyxing as px
from os import path
from weakref import proxy
from PyQt4 import QtGui, QtCore

from zeropositionviewer_ui import Ui_Form

import commutil.ExpireDateUtil as ExpireDateUtil

xinglogindlg_dir = path.dirname(path.realpath(__file__)) + '\\..'
sys.path.append(xinglogindlg_dir)

from commutil.xinglogindlg.xinglogindlg_main import LoginForm


class Observer_cmd(object):
    @classmethod
    def Update(cls, subject):
        subject.flag = False
        pass


class Observer_t0441(object):
    @classmethod
    def Update(cls, subject):
        subject.flag = False
        pass


class Observer_CEXAQ31200(object):
    @classmethod
    def Update(cls, subject):
        item = subject.data[1]
        if item['OptEvalPnlAmt'] != '' and item['FutsEvalPnlAmt'] != '':
            subject.pnl = int((int(item['OptEvalPnlAmt'] or 0) + int(item['FutsEvalPnlAmt'] or 0)) * 0.001)
        else:
            subject.pnl = 0
        # print subject.pnl
        subject.flag = False
        pass


class ZeroPositionViewer(QtGui.QWidget):
    update_CEXAQ31200 = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ZeroPositionViewer, self).__init__(parent)
        self.initUI()
        # self.initXing()
        # self.initQuery()
        # self.initTIMER()
        self.initExpireDateUtil()
        self.XASession = None
        self.ctimer = QtCore.QTimer()
        QtGui.qApp.setStyle('Cleanlooks')
        self.logger = logging.getLogger('ZeroOMS.PositionViewer')
        self.logger.info('Init PositionViewer')

    def closeEvent(self, event):
        self.ctimer.stop()
        event.accept()
        super(ZeroPositionViewer, self).closeEvent(event)
        
    def initUI(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # self.ui.tableWidget.resizeColumnToContents(1)
        self.ui.tableWidget.resizeRowsToContents()
        self.ui.tableWidget.setColumnWidth(0, 80)   # ShortCD
        self.ui.tableWidget.setColumnWidth(1, 50)   # Qty
        self.ui.tableWidget.setColumnWidth(2, 60)   # Mark
        self.ui.tableWidget.setColumnWidth(3, 70)   # TradePrice
        self.ui.tableWidget.setColumnWidth(4, 70)   # Delta
        self.ui.tableWidget.setColumnWidth(5, 70)   # Gamma
        self.ui.tableWidget.setColumnWidth(6, 70)   # Theta
        self.ui.tableWidget.setColumnWidth(7, 70)   # Vega
        self.ui.tableWidget.setColumnWidth(8, 120)  # P/L Day
        self.ui.tableWidget.setColumnWidth(9, 120)  # P/L Open

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
            self.servername = self.XASession.GetServerName()
            print self.accountlist
        else:
            print 'Not IsConnected or No Account'

    def initExpireDateUtil(self):
        self.expiredate_util = ExpireDateUtil.ExpireDateUtil()
        now_dt = dt.datetime.now()
        today = now_dt.strftime('%Y%m%d')

        self.expiredate_util.read_expire_date(path.dirname(ExpireDateUtil.__file__) + "\\expire_date.txt")
        expire_date_lst = self.expiredate_util.make_expire_date(today)
        # logger.info('%s' % ','.join(expire_date_lst))

    def initQuery(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():            
            nowtime = time.localtime()
            if nowtime.tm_hour >= 7 and nowtime.tm_hour < 17:
                self.exchange = 'KRX'
                self.xquery = px.XAQuery_t0441()
                obs_t0441 = Observer_t0441()
                self.xquery.observer = obs_t0441
                self.xquery.SetFieldData('t0441InBlock', 'accno', 0, self.accountlist[1])
                self.xquery.SetFieldData('t0441InBlock', 'passwd', 0, '0000')
            else:
                self.exchange = 'EUREX'
                self.xquery = px.XAQuery_CEXAQ31200()
                obs_cexaq31200 = Observer_CEXAQ31200()
                self.xquery.observer = obs_cexaq31200
                self.xquery.SetFieldData('CEXAQ31200InBlock1', 'RecCnt', 0, 1)
                self.xquery.SetFieldData('CEXAQ31200InBlock1', 'AcntNo', 0, self.accountlist[1])
                self.xquery.SetFieldData('CEXAQ31200InBlock1', 'InptPwd', 0, '0000')
                self.xquery.SetFieldData('CEXAQ31200InBlock1', 'BalEvalTp', 0, '1')
                self.xquery.SetFieldData('CEXAQ31200InBlock1', 'FutsPrcEvalTp', 0, '1')

            self.option_greeks_query = px.XAQuery_t2301()
            obs = Observer_cmd()
            self.option_greeks_query.observer = obs
        pass
        
    def initTIMER(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            self.ctimer = QtCore.QTimer()
            self.ctimer.timeout.connect(self.onTimer)
            self.ctimer.start(5000)
        pass
        
    def onTimer(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            self.xquery.flag = True
            ret = self.xquery.Request(False)
            while self.xquery.flag:
                # print 'test'
                pythoncom.PumpWaitingMessages()
                # self.xquery.flag = False

            if self.servername[0] == 'X':
                self.option_greeks_query.flag = True
                self.option_greeks_query.set_data(self.expiredate_util.front_expire_date[:6], 'G')
                ret = self.option_greeks_query.Request(False)
                while self.option_greeks_query.flag:
                    pythoncom.PumpWaitingMessages()

                self.option_greeks_query.flag = True
                self.option_greeks_query.set_data(self.expiredate_util.back_expire_date[:6], 'G')
                ret = self.option_greeks_query.Request(False)
                while self.option_greeks_query.flag:
                    pythoncom.PumpWaitingMessages()

            self.update_CEXAQ31200.emit()
            self.onReceiveData(self.exchange, self.xquery.data, self.option_greeks_query.block_data)
        pass

    def onReceiveData(self, exchange_code, data, block_data):

        greek_default_dict = dict()
        greek_default_dict['delt'] = 0.0
        greek_default_dict['gama'] = 0.0
        greek_default_dict['ceta'] = 0.0
        greek_default_dict['vega'] = 0.0

        if exchange_code == 'KRX':
            self.ui.tableWidget.setRowCount(len(data)-1+1)
            self.ui.tableWidget.resizeRowsToContents()

            total_delta = 0
            total_gamma = 0
            total_theta = 0
            total_vega = 0
            total_pnl_day = 0
            total_pnl_open = 0

            pnl_day = 0
            pnl_open = 0
            if data[0]['tdtsunik'] != '-':
                pnl_day = "{:,}".format(long(data[0]['tdtsunik']))
            if data[0]['tsunik'] != '-':
                pnl_open = "{:,}".format(long(data[0]['tsunik']))
            # print 'P/L Day: %s P/L Open: %s' % (data[0]['tdtsunik'], data[0]['tsunik'])

            for i in xrange(1, len(data)):
                shortcd = data[i]['expcode']
                if data[i]['medocd'] == '1':
                    pos = u'-' + data[i]['jqty']
                elif data[i]['medocd'] == '2':
                    pos = data[i]['jqty']
                else:
                    pos = ''

                pnl_day = 0
                pnl_open = 0

                if data[i]['dtsunik1'] != '-':
                    pnl_open = "{:,}".format(long(data[i]['dtsunik1']))
                if data[i]['dtsunik'] != '-':
                    pnl_day = "{:,}".format(long(data[i]['dtsunik']))

                avgprc = '%.5f' % float(data[i]['pamt'])
                lastprc = '%.2f' % float(data[i]['price'])

                if shortcd[0] in ['2', '3']:
                    delta = float(block_data.get(shortcd, greek_default_dict)['delt']) * int(pos)
                    gamma = float(block_data.get(shortcd, greek_default_dict)['gama']) * int(pos)
                    theta = float(block_data.get(shortcd, greek_default_dict)['ceta']) * int(pos)
                    vega = float(block_data.get(shortcd, greek_default_dict)['vega']) * int(pos)
                elif shortcd[:3] in ['101', '105']:
                    if shortcd[:3] == '101':
                        delta = 1.0 * int(pos)
                    elif shortcd[:3] == '105':
                        delta = 1.0 * int(pos) * 0.2
                    gamma = 0
                    theta = 0
                    vega = 0
                else:
                    delta = 0
                    gamma = 0
                    theta = 0
                    vega = 0

                total_delta += delta
                total_gamma += gamma
                total_theta += theta
                total_vega += vega

                if data[i]['dtsunik1'] != '-':
                    total_pnl_open += long(data[i]['dtsunik1'])
                if data[i]['dtsunik'] != '-':
                    total_pnl_day += long(data[i]['dtsunik'])

                delta = '%.4f' % delta
                gamma = '%.4f' % gamma
                theta = '%.4f' % theta
                vega = '%.4f' % vega

                self.updateTableWidgetItem(i-1, 0, shortcd)
                self.updateTableWidgetItem(i-1, 1, pos)
                self.updateTableWidgetItem(i-1, 2, lastprc)
                self.updateTableWidgetItem(i-1, 3, avgprc)
                self.updateTableWidgetItem(i-1, 4, delta)
                self.updateTableWidgetItem(i-1, 5, gamma)
                self.updateTableWidgetItem(i-1, 6, theta)
                self.updateTableWidgetItem(i-1, 7, vega)
                self.updateTableWidgetItem(i-1, 8, pnl_day)
                self.updateTableWidgetItem(i-1, 9, pnl_open)

            total_delta = '%.4f' % total_delta
            total_gamma = '%.4f' % total_gamma
            total_theta = '%.4f' % total_theta
            total_vega = '%.4f' % total_vega
            total_pnl_day = "{:,}".format(total_pnl_day)
            total_pnl_open = "{:,}".format(total_pnl_open)

            self.updateTableWidgetItem(len(data) - 1, 0, 'Total')
            self.updateTableWidgetItem(len(data) - 1, 1, '')
            self.updateTableWidgetItem(len(data) - 1, 2, '')
            self.updateTableWidgetItem(len(data) - 1, 3, '')
            self.updateTableWidgetItem(len(data) - 1, 4, total_delta)
            self.updateTableWidgetItem(len(data) - 1, 5, total_gamma)
            self.updateTableWidgetItem(len(data) - 1, 6, total_theta)
            self.updateTableWidgetItem(len(data) - 1, 7, total_vega)
            self.updateTableWidgetItem(len(data) - 1, 8, total_pnl_day)
            self.updateTableWidgetItem(len(data) - 1, 9, total_pnl_open)

        elif exchange_code == 'EUREX':
            self.ui.tableWidget.setRowCount(len(data)-2 + 1)
            self.ui.tableWidget.resizeRowsToContents()

            # print 'Tot P/L: %s Net P/L: %s' % (data[1]['TotPnlAmt'], data[1]['NetPnlAmt'])

            total_delta = 0
            total_gamma = 0
            total_theta = 0
            total_vega = 0
            total_pnl_day = 0
            total_pnl_open = 0

            for i in xrange(2, len(data)):
                shortcd = data[i]['FnoIsuNo']
                if data[i]['BnsTpCode'] == '1':
                    pos = u'-' + data[i]['UnsttQty']
                elif data[i]['BnsTpCode'] == '2':
                    pos = data[i]['UnsttQty']
                pnl_day = 0
                pnl_open = "{:,}".format(long(data[i]['EvalPnl']))
                avgprc = '%.5f' % float(data[i]['FnoAvrPrc'])
                lastprc = '%.2f' % float(data[i]['NowPrc'])

                # FIXME: switch futures greeks
                if shortcd[0] in ['2', '3']:
                    delta = float(block_data.get(shortcd, greek_default_dict)['delt']) * int(pos)
                    gamma = float(block_data.get(shortcd, greek_default_dict)['gama']) * int(pos)
                    theta = float(block_data.get(shortcd, greek_default_dict)['ceta']) * int(pos)
                    vega = float(block_data.get(shortcd, greek_default_dict)['vega']) * int(pos)
                elif shortcd[:3] in ['101', '105']:
                    if shortcd[:3] == '101':
                        delta = 1.0 * int(pos)
                    elif shortcd[:3] == '105':
                        delta = 1.0 * int(pos) * 0.2
                    gamma = 0
                    theta = 0
                    vega = 0
                else:
                    delta = 0
                    gamma = 0
                    theta = 0
                    vega = 0

                total_delta += delta
                total_gamma += gamma
                total_theta += theta
                total_vega += vega
                total_pnl_open += long(data[i]['EvalPnl'])

                delta = '%.4f' % delta
                gamma = '%.4f' % gamma
                theta = '%.4f' % theta
                vega = '%.4f' % vega

                self.updateTableWidgetItem(i-2, 0, shortcd)
                self.updateTableWidgetItem(i-2, 1, pos)
                self.updateTableWidgetItem(i-2, 2, lastprc)
                self.updateTableWidgetItem(i-2, 3, avgprc)
                self.updateTableWidgetItem(i-2, 4, delta)
                self.updateTableWidgetItem(i-2, 5, gamma)
                self.updateTableWidgetItem(i-2, 6, theta)
                self.updateTableWidgetItem(i-2, 7, vega)
                self.updateTableWidgetItem(i-2, 8, pnl_day)
                self.updateTableWidgetItem(i-2, 9, pnl_open)

            total_delta = '%.4f' % total_delta
            total_gamma = '%.4f' % total_gamma
            total_theta = '%.4f' % total_theta
            total_vega = '%.4f' % total_vega
            total_pnl_open = "{:,}".format(total_pnl_open)

            # print total_pnl

            self.updateTableWidgetItem(len(data)-2, 0, 'Total')
            self.updateTableWidgetItem(len(data)-2, 1, '')
            self.updateTableWidgetItem(len(data)-2, 2, '')
            self.updateTableWidgetItem(len(data)-2, 3, '')
            self.updateTableWidgetItem(len(data)-2, 4, total_delta)
            self.updateTableWidgetItem(len(data)-2, 5, total_gamma)
            self.updateTableWidgetItem(len(data)-2, 6, total_theta)
            self.updateTableWidgetItem(len(data)-2, 7, total_vega)
            self.updateTableWidgetItem(len(data)-2, 8, total_pnl_day)
            self.updateTableWidgetItem(len(data)-2, 9, total_pnl_open)
            
    def updateTableWidgetItem(self, row, col, text):
        widget_item = self.ui.tableWidget.item(row, col)
        if not widget_item:
            newitem = QtGui.QTableWidgetItem(text)
            newitem.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            if col == 0:
                newitem.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            # if col in self.alignRightColumnList: NewItem.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            self.ui.tableWidget.setItem(row, col, newitem)
        else:
            widget_item.setText(str(text))
        pass


if __name__ == '__main__':    
    app = QtGui.QApplication(sys.argv)
    myform = ZeroPositionViewer()
    myform.initXing()
    myform.initQuery()
    myform.initTIMER()
    myform.show()
    app.exec_()

