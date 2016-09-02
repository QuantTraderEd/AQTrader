# -*- coding: utf-8 -*-

import logging
import datetime as dt
import zmq
import redis
import sip
from PyQt4 import QtCore
from PyQt4 import QtGui
from ui_AutoOTMTrader import Ui_MainWindow
from AutoOTMTrader_thread import OptionViewerThread, ExecutionThread
# from ReceiverThread import ReceiverThread

import sqlalchemy_pos_init as position_db_init
from sqlalchemy_pos_declarative import PositionEntity
from sqlalchemy_pos_update import updateNewPositionEntity

logger = logging.getLogger('AutoOTMTrader')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('AutoOTMTrader.log')
#fh = logging.Handlers.RotatingFileHandler('AutoOTMTrader.log',maxBytes=104857,backupCount=3)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)

def convert(strprice):
    return '%.2f' %round(float(strprice), 2)

class MainForm(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(MainForm, self).__init__()
        self.initUI()
        self.initPositionDB()
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
        self.socket.setsockopt(zmq.RCVTIMEO, 2000)
        self.socket.connect("tcp://127.0.0.1:6004")
        pass
    
    def initThread(self):
        # self._thread = OptionViewerThread(None)
        # self._thread.receiveData[str].connect(self.onReceiveData)
        # self._thread = ReceiverThread(None)
        self._thread = OptionViewerThread()
        self._executionthread = ExecutionThread()
        self._thread.port = 5501
        self._thread.receiveData[dict].connect(self.onReceiveData)
        # self._thread.receiveData[str].connect(self.onReceiveData_Old)
        self._executionthread.receiveData[dict].connect(self.onReceiveExecution)

    def initPositionDB(self):

        self.position_dict = {}
        self.avgexecprice_dict = {}

        self.ask1_dict = {}
        self.bid1_dict = {}

        self.total_pnl = 0

        self.orderseq = list()

        self.redis_client = redis.Redis()
        self._session = position_db_init.initSession('autotrader_position.db')
        self.updatePostionTable()

        for i in xrange(len(self.shortcd_lst)):
            shortcd = self.shortcd_lst[i]
            ask1 = self.redis_client.hget('ask1_dict', shortcd)
            bid1 = self.redis_client.hget('bid1_dict', shortcd)
            if ask1 is not None:
                self.ask1_dict[shortcd] = float(ask1)
            else:
                self.ask1_dict[shortcd] = 0
                ask1 = 0
            if bid1 is not None:
                self.bid1_dict[shortcd] = float(bid1)
            else:
                self.bid1_dict[shortcd] = 0
                bid1 = 0
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
        if shortcd[:3] in ['201', '301']:
            msg_dict = {}
            msg_dict['ShortCD'] = shortcd
            msg_dict['OrderPrice'] = orderprice
            msg_dict['OrderQty'] = orderqty
            msg_dict['BuySell'] = buysell
            msg_dict['NewAmendCancel'] = 'N'
            msg_dict['OrderType'] = 2  # market = 1 limit = 2
            msg_dict['TimeInForce'] = 'GFD'
            logger.info('Send Order->'+str(msg_dict))
            self.socket.send_pyobj(msg_dict)
            msg_in = self.socket.recv()
            logger.info('Recv Msg->'+msg_in)
            
    def onClick(self):
        isThreadRun = self._thread.isRunning()
        if not isThreadRun:
            self._thread.start()
            self.ui.pushButton_Start.setText('Stop')
        elif isThreadRun:
            self._thread.stop()
            # self._thread.terminate()
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
    
    def onReceiveData(self, msg_dict):
        if msg_dict['TAQ'] == 'Q' and msg_dict['SecuritiesType'] == 'options':
            nowtime = dt.datetime.now()
            shortcd = msg_dict['ShortCD']

            int_nowtime = nowtime.hour * 100 + nowtime.minute
            if len(self.orderseq) > 0 and ((800 <= int_nowtime < 1500) or (int_nowtime >= 1750 or int_nowtime < 400)):
                if self.orderseq[0]['buysell'] == 'buy':
                    buysell = 'B'
                elif self.orderseq[0]['buysell'] == 'sell':
                    buysell = 'S'

                self.sendOrder(self.orderseq[0]['shortcd'], self.orderseq[0]['orderprice'],
                               self.orderseq[0]['orderqty'], buysell)
                pos = self.shortcd_lst.index(self.orderseq[0]['shortcd'])
                liveqty = str(self.orderseq[0]['orderqty'])
                if buysell == 'sell': liveqty = '-' + liveqty
                self.updateTableWidgetItem(pos, 6, liveqty)
                self.updateTableWidgetItem(pos, 7, str(self.orderseq[0]['orderprice']))
                del self.orderseq[0]

            if not (shortcd in self.shortcd_lst): return
            pos = self.shortcd_lst.index(shortcd)

            ask1 = float(msg_dict['Ask1'])
            bid1 = float(msg_dict['Bid1'])
            askqty1 = int(msg_dict['AskQty1'])
            bidqty1 = int(msg_dict['BidQty1'])

            print nowtime, str(shortcd), askqty1, ask1, bid1, bidqty1
            holdqty = long(self.holdqty_lst[pos])
            midprice = (bid1 + ask1) * 0.5
            midprice_old = (self.bid1_dict[shortcd] + self.ask1_dict[shortcd]) * 0.5
            buysell = self.buysell_lst[pos]
            pnl = (midprice - self.avgexecprice_dict[shortcd]) * self.position_dict[shortcd]
            pnl_diff = (midprice - midprice_old) * holdqty
            if buysell == 'sell':
                pnl *= -1.0
                pnl_diff *= -1.0
            self.total_pnl += pnl_diff

            self.updateTableWidgetItem(pos, 2, str(pnl))
            self.updateTableWidgetItem(pos, 4, str(ask1))
            self.updateTableWidgetItem(pos, 5, str(bid1))
            
            self.updateTableWidgetItem(len(self.shortcd_lst), 2, str(self.total_pnl))

            self.ask1_dict[shortcd] = ask1
            self.bid1_dict[shortcd] = bid1
            
        pass

    def onReceiveExecution(self, data_dict):
        exec_data_dict = dict()
        exec_data_dict['autotrader_id'] = 'OTM001'
        exec_data_dict['shortcd'] = data_dict['shortcd']
        exec_data_dict['execprice'] = data_dict['execprice']
        exec_data_dict['execqty'] = data_dict['execqty']
        exec_data_dict['buysell'] = data_dict['buysell']
        updateNewPositionEntity(self._session, exec_data_dict)
        pass

    def updatePostionTable(self):
        rows = self._session.query(PositionEntity.shortcd).filter(PositionEntity.holdqty > 0).all()
        self.shortcd_lst = list(zip(*rows)[0])

        rows = self._session.query(PositionEntity.holdqty).filter(PositionEntity.holdqty > 0).all()
        self.holdqty_lst = list(zip(*rows)[0])

        rows = self._session.query(PositionEntity.avgexecprice).filter(PositionEntity.holdqty > 0).all()
        self.avgexecprice_lst = list(zip(*rows)[0])

        rows = self._session.query(PositionEntity.buysell).filter(PositionEntity.holdqty > 0).all()
        self.buysell_lst = list(zip(*rows)[0])

        self.ui.tableWidget.setRowCount(len(self.shortcd_lst)+1)

        for i in xrange(len(self.shortcd_lst)):
            shortcd = self.shortcd_lst[i]
            self.position_dict[shortcd] = int(self.holdqty_lst[i])
            self.avgexecprice_dict[shortcd] = self.avgexecprice_lst[i]

            pos = self.shortcd_lst.index(shortcd)
            buysell = self.buysell_lst[pos]
            str_holdqty = str(self.holdqty_lst[i])
            if buysell == 'sell':
                str_holdqty = '-' + str_holdqty

            self.updateTableWidgetItem(i, 0, self.shortcd_lst[i])
            self.updateTableWidgetItem(i, 1, str_holdqty)
            self.updateTableWidgetItem(i, 3, str(self.avgexecprice_dict[shortcd]))

    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    app.exec_()