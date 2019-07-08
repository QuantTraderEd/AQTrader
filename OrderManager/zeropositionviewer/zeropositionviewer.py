# -*- coding: utf-8 -*-


import os
import time
import sys
import logging
import pythoncom
import pyxing as px
from PyQt4 import QtGui, QtCore
from ui_zeropositionviewer import Ui_Form
from weakref import proxy

xinglogindlg_dir = os.path.dirname(os.path.realpath(__file__)) + '\\..'
sys.path.append(xinglogindlg_dir)

from xinglogindlg import LoginForm


class observer_cmd:
    def Update(self, subject):
        subject.flag = False
        pass


class observer_t0441:
    def Update(self, subject):
        subject.flag = False
        pass


class observer_CEXAQ31200:
    def Update(self, subject):
        item = subject.data[1]
        subject.pnl = int((int(item['OptEvalPnlAmt'] or 0) + int(item['FutsEvalPnlAmt'] or 0)) * 0.001)
        subject.flag = False
        pass


class ZeroPositionViewer(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ZeroPositionViewer, self).__init__()
        self.initUI()
        # self.initXing()
        # self.initQuery()
        # self.initTIMER()
        self.logger = logging.getLogger('ZeroOMS.PositionViewer')
        self.logger.info('Init PositionViewer')
        
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
        self.ui.tableWidget.setColumnWidth(8, 120)   # P/L Open

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

    def initQuery(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():            
            nowtime = time.localtime()
            if nowtime.tm_hour >= 6 and nowtime.tm_hour < 16:
                self.exchange = 'KRX'
                self.NewQuery = px.XAQuery_t0441()
                obs = observer_t0441()
                self.NewQuery.observer = obs
                self.NewQuery.SetFieldData('t0441InBlock', 'accno', 0, self.accountlist[1])
                self.NewQuery.SetFieldData('t0441InBlock', 'passwd', 0, '0000')
            else:
                self.exchange = 'EUREX'
                self.NewQuery = px.XAQuery_CEXAQ31200()
                obs = observer_CEXAQ31200()
                self.NewQuery.observer = obs
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1', 'RecCnt', 0, 1)
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1', 'AcntNo', 0, self.accountlist[1])
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1', 'InptPwd', 0, '0000')
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1', 'BalEvalTp', 0, '1')
                self.NewQuery.SetFieldData('CEXAQ31200InBlock1', 'FutsPrcEvalTp', 0, '1')

            self.option_greeks_query = px.XAQuery_t2301()
            obs = observer_cmd()
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
            self.NewQuery.flag = True
            ret = self.NewQuery.Request(False)        
            while self.NewQuery.flag:
                pythoncom.PumpWaitingMessages()

            if self.servername[0] == 'X':
                self.option_greeks_query.flag = True
                self.option_greeks_query.set_data('201706', 'G')
                self.option_greeks_query.SetFieldData('T2301InBlock', 'yyyymm', 0, '201705')
                self.option_greeks_query.SetFieldData('T2301InBlock', 'gubun', 0, 'G')
                ret = self.option_greeks_query.Request(False)
                while self.option_greeks_query.flag:
                    pythoncom.PumpWaitingMessages()

                self.option_greeks_query.flag = True
                self.option_greeks_query.set_data('201706', 'G')
                self.option_greeks_query.SetFieldData('T2301InBlock', 'yyyymm', 0, '201706')
                self.option_greeks_query.SetFieldData('T2301InBlock', 'gubun', 0, 'G')
                ret = self.option_greeks_query.Request(False)
                while self.option_greeks_query.flag:
                    pythoncom.PumpWaitingMessages()

            self.onReceiveData(self.exchange, self.NewQuery.data, self.option_greeks_query.block_data)
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
            total_pnl = 0

            print 'P/L Day: ', data[0]['tdtsunik'] + data[0]['tsunik']

            for i in xrange(1, len(data)):
                shortcd = data[i]['expcode']
                if data[i]['medocd'] == '1':
                    pos = u'-' + data[i]['jqty']
                elif data[i]['medocd'] == '2':
                    pos = data[i]['jqty']
                else:
                    pos = ''

                if data[i]['dtsunik1'] == '-':
                    pnl = 0
                else:
                    pnl = "{:,}".format(long(data[i]['dtsunik1']))
                avgprc = '%.5f' % float(data[i]['pamt'])
                lastprc = '%.2f' % float(data[i]['price'])

                # FIXME: switch futures greeks
                if shortcd[0] in ['2', '3']:
                    delta = float(block_data.get(shortcd, greek_default_dict)['delt']) * int(pos)
                    gamma = float(block_data.get(shortcd, greek_default_dict)['gama']) * int(pos)
                    theta = float(block_data.get(shortcd, greek_default_dict)['ceta']) * int(pos)
                    vega = float(block_data.get(shortcd, greek_default_dict)['vega']) * int(pos)
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
                    total_pnl += long(data[i]['dtsunik1'])

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
                self.updateTableWidgetItem(i-1, 8, pnl)

            total_delta = '%.4f' % total_delta
            total_gamma = '%.4f' % total_gamma
            total_theta = '%.4f' % total_theta
            total_vega = '%.4f' % total_vega
            total_pnl = "{:,}".format(total_pnl)

            self.updateTableWidgetItem(len(data) - 1, 0, 'Total')
            self.updateTableWidgetItem(len(data) - 1, 1, '')
            self.updateTableWidgetItem(len(data) - 1, 2, '')
            self.updateTableWidgetItem(len(data) - 1, 3, '')
            self.updateTableWidgetItem(len(data) - 1, 4, total_delta)
            self.updateTableWidgetItem(len(data) - 1, 5, total_gamma)
            self.updateTableWidgetItem(len(data) - 1, 6, total_theta)
            self.updateTableWidgetItem(len(data) - 1, 7, total_vega)
            self.updateTableWidgetItem(len(data) - 1, 8, total_pnl)

        elif exchange_code == 'EUREX':
            self.ui.tableWidget.setRowCount(len(data)-2 + 1)
            self.ui.tableWidget.resizeRowsToContents()

            total_delta = 0
            total_gamma = 0
            total_theta = 0
            total_vega = 0
            total_pnl = 0

            for i in xrange(2, len(data)):
                shortcd = data[i]['FnoIsuNo']
                if data[i]['BnsTpCode'] == '1':
                    pos = u'-' + data[i]['UnsttQty']
                elif data[i]['BnsTpCode'] == '2':
                    pos = data[i]['UnsttQty']
                pnl = "{:,}".format(long(data[i]['EvalPnl']))
                avgprc = '%.5f' % float(data[i]['FnoAvrPrc'])
                lastprc = '%.2f' % float(data[i]['NowPrc'])

                # FIXME: switch futures greeks
                if shortcd[0] in ['2', '3']:
                    delta = float(block_data.get(shortcd, greek_default_dict)['delt']) * int(pos)
                    gamma = float(block_data.get(shortcd, greek_default_dict)['gama']) * int(pos)
                    theta = float(block_data.get(shortcd, greek_default_dict)['ceta']) * int(pos)
                    vega = float(block_data.get(shortcd, greek_default_dict)['vega']) * int(pos)
                else:
                    delta = 0
                    gamma = 0
                    theta = 0
                    vega = 0

                total_delta += delta
                total_gamma += gamma
                total_theta += theta
                total_vega += vega
                total_pnl += long(data[i]['EvalPnl'])

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
                self.updateTableWidgetItem(i-2, 8, pnl)

            total_delta = '%.4f' % total_delta
            total_gamma = '%.4f' % total_gamma
            total_theta = '%.4f' % total_theta
            total_vega = '%.4f' % total_vega
            total_pnl = "{:,}".format(total_pnl)

            # print total_pnl

            self.updateTableWidgetItem(len(data)-2, 0, 'Total')
            self.updateTableWidgetItem(len(data)-2, 1, '')
            self.updateTableWidgetItem(len(data)-2, 2, '')
            self.updateTableWidgetItem(len(data)-2, 3, '')
            self.updateTableWidgetItem(len(data)-2, 4, total_delta)
            self.updateTableWidgetItem(len(data)-2, 5, total_gamma)
            self.updateTableWidgetItem(len(data)-2, 6, total_theta)
            self.updateTableWidgetItem(len(data)-2, 7, total_vega)
            self.updateTableWidgetItem(len(data)-2, 8, total_pnl)
            
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
    
