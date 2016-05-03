# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 23:30:23 2015

@author: assa
"""

import sip
import redis
import datetime as dt
import zmq
from PyQt4 import QtCore
from PyQt4 import QtGui
from ui_AutoOTMTrader import Ui_MainWindow
# from zerooptionviewer_thread import OptionViewerThread
from AutoOTMTrader_thread import OptionViewerThread, ExecutionThread
from ReceiverThread import ReceiverThread

import sqlalchemy_pos_init as position_db_init
from sqlalchemy_pos_declarative import PositionEntity

def convert(strprice):
    return '%.2f' %round(float(strprice),2)


class MainForm(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(MainForm,self).__init__()
        self.initUI()
        self.initPositionDB()
        self.test()
        self.initZMQ()
        self.initThread()
        sip.setdestroyonexit(False)

    def closeEvent(self, event):
        setting = QtCore.QSettings("AutoOTMTrader.ini", QtCore.QSettings.IniFormat)
        setting.setValue("AutoOTMTrader_Geometry", self.saveGeometry())

    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_Start.clicked.connect(self.onClick)
        # self.resize(400, 240)
        setting = QtCore.QSettings("AutoOTMTrader.ini", QtCore.QSettings.IniFormat)
        self.restoreGeometry(setting.value("AutoOTMTrader_Geometry").toByteArray())
        pass

    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO,2000)
        self.socket.connect("tcp://127.0.0.1:6000")
        pass
    
    def initThread(self):
        # self._thread = OptionViewerThread(None)
        # self._thread.receiveData[str].connect(self.onReceiveData)
        # self._thread = ReceiverThread(None)
        self._thread = OptionViewerThread()
        self._executionthread = ExecutionThread()
        # self._thread.port = 5510
        self._thread.port = 5500
        # self._thread.receiveData[dict].connect(self.onReceiveData)
        self._thread.receiveData[str].connect(self.onReceiveData_Old)

    def initPositionDB(self):
        self._session = position_db_init.initSession('autotrader_position.db')

    def test(self):
        self.redis_client = redis.Redis()

        rows = self._session.query(PositionEntity.shortcd).filter(PositionEntity.holdqty > 0).all()
        self.shortcd_lst = list(zip(*rows)[0])

        rows = self._session.query(PositionEntity.holdqty).filter(PositionEntity.holdqty > 0).all()
        self.holdqty_lst = list(zip(*rows)[0])

        rows = self._session.query(PositionEntity.avgexecprice).filter(PositionEntity.holdqty > 0).all()
        self.avgexecprice_lst = list(zip(*rows)[0])

        rows = self._session.query(PositionEntity.buysell).filter(PositionEntity.holdqty > 0).all()
        self.buysell_lst = list(zip(*rows)[0])

        self.position_dict = {}
        self.avgexecprice_dict = {}
        
        self.ask1_dict = {}
        self.bid1_dict = {}

        self.orderseq = list()
        
        self.total_pnl = 0
        self.ui.tableWidget.setRowCount(len(self.shortcd_lst)+1)        
        for i in xrange(len(self.shortcd_lst)):
            shortcd = self.shortcd_lst[i]
            self.position_dict[shortcd] = int(self.holdqty_lst[i])
            self.avgexecprice_dict[shortcd] = self.avgexecprice_lst[i]
            ask1 = self.redis_client.hget('ask1_dict', shortcd)
            bid1 = self.redis_client.hget('bid1_dict', shortcd)
            self.ask1_dict[shortcd] = float(ask1)
            self.bid1_dict[shortcd] = float(bid1)
            midprice = (float(bid1) + float(ask1)) * 0.5
            pos = self.shortcd_lst.index(shortcd)
            buysell = self.buysell_lst[pos]
            pnl = (midprice - self.avgexecprice_dict[shortcd]) * self.position_dict[shortcd]
            if buysell == 'sell':
                pnl *= -1.0
                order_dict = dict()
                order_dict['shortcd'] = shortcd
                order_dict['orderprice'] = 0.01
                order_dict['orderqty'] = self.position_dict[shortcd]
                order_dict['buysell'] = 'buy'
                self.orderseq.append(order_dict)
            self.total_pnl += pnl
            self.updateTableWidgetItem(i, 0, self.shortcd_lst[i])
            self.updateTableWidgetItem(i, 1, str(self.holdqty_lst[i]))
            self.updateTableWidgetItem(i, 2, str(pnl))
            self.updateTableWidgetItem(i, 3, str(self.avgexecprice_dict[shortcd]))
            self.updateTableWidgetItem(i, 4, ask1)
            self.updateTableWidgetItem(i, 5, bid1)
            
        self.updateTableWidgetItem(i+1, 0, 'Total')
        self.updateTableWidgetItem(i+1, 2, str(self.total_pnl))
        
        self.ui.tableWidget.resizeColumnToContents(0)
        self.ui.tableWidget.resizeColumnToContents(1)
        self.ui.tableWidget.resizeColumnToContents(2)
        self.ui.tableWidget.resizeColumnToContents(3)
        self.ui.tableWidget.resizeColumnToContents(4)
        self.ui.tableWidget.resizeColumnToContents(5)
        self.ui.tableWidget.resizeColumnToContents(6)
        self.ui.tableWidget.resizeColumnToContents(7)

        print self.avgexecprice_dict
        print self.shortcd_lst

    def sendOrder(self, shortcd, orderprice, orderqty, buysell):
        if shortcd[:3] == '201' or shortcd[:3] == '301':
            msg = str(buysell) + ',' + str(shortcd) + ',' + str(orderprice) + ',' + str(orderqty)
            print msg
            self.socket.send(msg)
            msg_in = self.socket.recv()
            print msg_in
            
    def onClick(self):
        if not self._thread.isRunning():
            self._thread.start()
            self.ui.pushButton_Start.setText('Stop')
        else:
            self._thread.terminate()
            self.ui.pushButton_Start.setText('Start')
        pass
    
    def updateTableWidgetItem(self,row,col,text):
        widgetItem = self.ui.tableWidget.item(row,col)
        if not widgetItem:
            NewItem = QtGui.QTableWidgetItem(text)
            # if col in self.alignRightColumnList: NewItem.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            self.ui.tableWidget.setItem(row,col,NewItem)
        else:
            widgetItem.setText(text)
        pass
    
    def onReceiveData(self, row_dict):
        if row_dict['TAQ'] == 'Q' and row_dict['SecuritiesType'] == 'options':
            shortcd = row_dict['ShortCD']
            ask1 = row_dict['Ask1']
            bid1 = row_dict['Bid1']
            askqty1 = row_dict['AskQty1']
            bidqty1 = row_dict['BidQty1']
            
            print row_dict['Time']
            
            if not (shortcd in self.shortcd_lst): return
            pos = self.shortcd_lst.index(shortcd)
            
            holdqty = long(self.holdqty_lst[pos])
            midprice = (float(bid1) + float(ask1)) * 0.5
            midprice_old = (self.bid1_dict[shortcd] + self.ask1_dict[shortcd]) * 0.5
            pnl = (midprice - self.avgexecprice_lst[pos]) * holdqty
            buysell = self.buysell_lst[pos]
            pnl_diff = (midprice - midprice_old) * holdqty
            if buysell == 'sell':
                pnl *= -1.0
                pnl_diff *= 1.0
            print shortcd, midprice, midprice_old, pnl, pnl_diff
            print self.total_pnl
            self.total_pnl += pnl_diff
            print self.total_pnl
            
            self.updateTableWidgetItem(pos, 1, str(holdqty))
            self.updateTableWidgetItem(pos, 2, str(pnl))
            self.updateTableWidgetItem(pos, 4, ask1)
            self.updateTableWidgetItem(pos, 5, bid1)
            
            self.updateTableWidgetItem(len(self.shortcd_lst), 3, str(self.total_pnl))
            
            self.ask1_dict[shortcd] = float(ask1)
            self.bid1_dict[shortcd] = float(bid1)
            
        pass
    
    def onReceiveData_Old(self, msg):
        nowtime = dt.datetime.now()
        lst = msg.split(',')                
        if lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'futures':
            if nowtime.hour >= 7 and nowtime.hour < 17:
                shortcd = lst[4]
                ask1 = convert(lst[6])
                bid1 = convert(lst[23])
                askqty1 = lst[11]
                bidqty1 = lst[28]
            else:
                shortcd = lst[4]
                ask1 = convert(lst[29])
                bid1 = convert(lst[18])
                askqty1 = lst[30]
                bidqty1 = lst[19]
            
        elif lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'options':
            if nowtime.hour >= 7 and nowtime.hour <= 16:
                shortcd = lst[4]
                ask1 = convert(lst[6])
                bid1 = convert(lst[23])
                askqty1 = lst[11]
                bidqty1 = lst[28]

            else:
                return

            if len(self.orderseq) > 0:
                if self.orderseq[0]['buysell'] == 'buy':
                    buysell = 'True'
                elif self.orderseq[0]['buysell'] == 'sell':
                    buysell = 'False'

                self.sendOrder(self.orderseq[0]['shortcd'], self.orderseq[0]['orderprice'],
                               self.orderseq[0]['orderqty'], buysell)
                del self.orderseq[0]

            if not (shortcd in self.shortcd_lst): return
            pos = self.shortcd_lst.index(shortcd)
            print nowtime, shortcd, askqty1, ask1, bid1, bidqty1
            holdqty = long(self.holdqty_lst[pos])
            midprice = (float(bid1) + float(ask1)) * 0.5
            buysell = self.buysell_lst[pos]
            pnl = (midprice - self.avgexecprice_dict[shortcd]) * self.position_dict[shortcd]
            if buysell == 'sell':
                pnl *= -1.0
            
            self.updateTableWidgetItem(pos, 1, str(holdqty))
            self.updateTableWidgetItem(pos, 2, str(pnl))
            self.updateTableWidgetItem(pos, 4, ask1)
            self.updateTableWidgetItem(pos, 5, bid1)

                
        elif lst[1] == 'cybos' and lst[2] == 'E' and lst[3] == 'options':
            shortcd = lst[4]
            expectprice = convert(lst[6])
            expectqty = 'E'            
                
        elif lst[1] == 'xing' and lst[2] == 'T' and lst[3] == 'options':
            if nowtime.hour >= 7 and nowtime.hour < 17:
                shortcd = lst[31]
                lastprice = convert(lst[8])
                lastqty = lst[13]
            else:
                shortcd = lst[len(lst)-1]
                lastprice = convert(lst[9])
                lastqty = lst[14]            

        elif lst[1] == 'xing' and lst[2] == 'Q' and lst[3] == 'options':
            if nowtime.hour >= 7 and nowtime.hour <= 16:
                shortcd = str(lst[len(lst)-3])

            else:
                shortcd = str(lst[len(lst)-1])
                ask1 = convert(lst[6])
                bid1 = convert(lst[7])
                askqty1 = lst[8]
                bidqty1 = lst[9]

            if len(self.orderseq) > 0:
                if self.orderseq[0]['buysell'] == 'buy':
                    buysell = 'True'
                elif self.orderseq[0]['buysell'] == 'sell':
                    buysell = 'False'

                self.sendOrder(self.orderseq[0]['shortcd'], self.orderseq[0]['orderprice'],
                               self.orderseq[0]['orderqty'], buysell)
                del self.orderseq[0]

            if not (shortcd in self.shortcd_lst): return
            pos = self.shortcd_lst.index(shortcd)
            print nowtime, shortcd, askqty1, ask1, bid1, bidqty1
            holdqty = long(self.holdqty_lst[pos])
            midprice = (float(bid1) + float(ask1)) * 0.5
            buysell = self.buysell_lst[pos]
            pnl = (midprice - self.avgexecprice_dict[shortcd]) * self.position_dict[shortcd]
            if buysell == 'sell':
                pnl *= -1.0
            self.updateTableWidgetItem(pos, 1, str(holdqty))
            self.updateTableWidgetItem(pos, 2, str(pnl))
            self.updateTableWidgetItem(pos, 4, ask1)
            self.updateTableWidgetItem(pos, 5, bid1)
                
        pass
                
                
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    app.exec_()