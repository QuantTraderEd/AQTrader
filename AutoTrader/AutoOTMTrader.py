# -*- coding: utf-8 -*-

import os
import logging
import datetime as dt
import collections
import redis
import sip
from PyQt4 import QtCore
from PyQt4 import QtGui
from ui_AutoOTMTrader import Ui_MainWindow
from AutoOTMTrader_thread import TickDataReceiverThread, ExecutionReportThread, OrderThread
from FeedCodeList import FeedCodeList
import CommUtil.ExpireDateUtil as ExpireDateUtil

import sqlalchemy_pos_init as position_db_init
from sqlalchemy_pos_declarative import PositionEntity
from sqlalchemy_pos_update import updateNewPositionEntity

logger = logging.getLogger('AutoOTMTrader')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('AutoOTMTrader.log')
# fh = logging.Handlers.RotatingFileHandler('AutoOTMTrader.log',maxBytes=104857,backupCount=3)
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


class MainForm(QtGui.QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.initUI()
        self.redis_client = redis.Redis()
        self.position_entity_dict = {}
        self.position_dict = {}
        self.avgexecprice_dict = {}
        self.liveqty_dict = {}
        self.ask1_dict = {}
        self.bid1_dict = {}
        self.total_pnl = 0
        self.orderseq = list()
        self.order_qu = collections.deque()
        self.order_cnt = 0

        self.autotrader_id = 'OTM001'
        self.order_port = 6001  # real 6000
        self.exec_report_port = 7001  # real 7000

        self.qtimer = QtCore.QTimer()
        self.qtimer.timeout.connect(self.on_timer)

        self.initStrikeList()
        self.initThread()
        self._session = position_db_init.initSession('autotrader_position.db')
        self.init_quote_dict()
        self.updatePostionTable()
        # self.init_orderseq()

        self.atm_strike = self.find_atm_strike()

        call_shortcd = self.find_target_shortcd('call')
        put_shortcd = self.find_target_shortcd('put')

        logger.info('======= target option shortcd ======')
        logger.info('atm_strike-> %s' % self.atm_strike)
        logger.info('target call option-> %s' % call_shortcd)
        logger.info('target put option-> %s' % put_shortcd)
        logger.info('====================================')

        sip.setdestroyonexit(False)

    def closeEvent(self, event):
        setting = QtCore.QSettings("AutoOTMTrader.ini", QtCore.QSettings.IniFormat)
        setting.setValue("AutoOTMTrader_Geometry", self.saveGeometry())
        event.accept()
        super(MainForm, self).closeEvent(event)

    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_Start.clicked.connect(self.onClick)

        setting = QtCore.QSettings("AutoOTMTrader.ini", QtCore.QSettings.IniFormat)
        if setting.value("AutoOTMTrader_Geometry") is not None:
            self.restoreGeometry(setting.value("AutoOTMTrader_Geometry").toByteArray())

        self.alignRightColumnList = [1, 2, 3, 4, 6, 7]
        self.alignCenterColumnList = [0]
        self.bidaskcolindex = [4, 5]

        self.ui.tableWidget.resizeRowsToContents()
        # self.ui.tableWidget.resizeColumnToContents(0)       # shortcd
        # self.ui.tableWidget.resizeColumnToContents(1)       # qty
        self.ui.tableWidget.resizeColumnToContents(2)       # P/L Open
        self.ui.tableWidget.resizeColumnToContents(3)  # avgprice
        # self.ui.tableWidget.resizeColumnToContents(4)       # ask1
        # self.ui.tableWidget.resizeColumnToContents(5)       # bid1
        self.ui.tableWidget.resizeColumnToContents(6)  # liveqty
        self.ui.tableWidget.resizeColumnToContents(7)  # orderprice

        self.ui.tableWidget.setColumnWidth(0, 70)
        self.ui.tableWidget.setColumnWidth(1, 35)
        self.ui.tableWidget.setColumnWidth(2, 70)
        self.ui.tableWidget.setColumnWidth(4, 40)
        self.ui.tableWidget.setColumnWidth(5, 40)

        pass

    def initThread(self):
        # self._thread = OptionViewerThread(None)
        # self._thread.receiveData[str].connect(self.onReceiveData)
        # self._thread = ReceiverThread(None)
        self._tickreceiverthread = TickDataReceiverThread()
        self._executionreportthread = ExecutionReportThread()
        self._orderthread = OrderThread()
        self._tickreceiverthread.port = 5501
        self._executionreportthread.port = self.exec_report_port
        self._orderthread.port = self.order_port
        self._orderthread.initZMQ()
        self._tickreceiverthread.receiveData[dict].connect(self.onReceiveData)
        # self._thread.receiveData[str].connect(self.onReceiveData_Old)
        self._orderthread.receiveData[dict].connect(self.onReceiveOrderAck)
        self._executionreportthread.receiveData[dict].connect(self.onReceiveExecution)

    def init_quote_dict(self):
        self.bid1_dict = self.redis_client.hgetall('bid1_dict')
        self.ask1_dict = self.redis_client.hgetall('ask1_dict')
        for shortcd in self.bid1_dict.keys():
            if self.bid1_dict[shortcd] is not None:
                self.bid1_dict[shortcd] = float(self.bid1_dict[shortcd])
            else:
                self.bid1_dict[shortcd] = 0.0

        for shortcd in self.ask1_dict.keys():
            if self.ask1_dict[shortcd] is not None:
                self.ask1_dict[shortcd] = float(self.ask1_dict[shortcd])
            else:
                self.ask1_dict[shortcd] = 0.0

    def init_orderseq(self):
        if len(self.position_shortcd_lst) > 0:
            logger.info('======= exit option shortcd ======')
            for i in xrange(len(self.position_shortcd_lst)):
                shortcd = self.position_shortcd_lst[i]
                ask1 = self.bid1_dict.get(shortcd, 0.0)
                bid1 = self.bid1_dict.get(shortcd, 0.0)

                pos = self.position_shortcd_lst.index(shortcd)
                buysell = self.buysell_lst[pos]

                if buysell in ['sell', 'S']:
                    logger.info('exit option shortcd-> %s' % shortcd)
                    order_dict = dict()
                    order_dict['shortcd'] = shortcd
                    order_dict['orderprice'] = 0.01
                    # if ask1 - bid1 <= 0.03:
                    #     order_dict['orderprice'] = ask1
                    order_dict['orderqty'] = self.position_dict[shortcd]
                    # order_dict['orderprice'] = float(ask1)
                    # order_dict['orderqty'] = 1
                    order_dict['buysell'] = 'B'
                    self.orderseq.append(order_dict)

            logger.info('====================================')

        else:
            now_dt = dt.datetime.now()
            # if now_dt.hour >= 9 and now_dt.hour <= 15:
            if now_dt.hour >= 9:
                call_shortcd = self.find_target_shortcd('call')
                put_shortcd = self.find_target_shortcd('put')

                logger.info('======= target option shortcd ======')
                logger.info('target call option-> %s' % call_shortcd)
                logger.info('target put option-> %s' % put_shortcd)
                logger.info('====================================')

                if call_shortcd is None or put_shortcd is None:
                    logger.info('target option is not found')
                    self.orderseq = list()

                # for shortcd in [call_shortcd, put_shortcd]:
                for shortcd in [put_shortcd]:
                    if shortcd is None: continue
                    ask1 = self.bid1_dict.get(shortcd, 0.0)
                    bid1 = self.bid1_dict.get(shortcd, 0.0)
                    buysell = 'S'

                    for i in xrange(4):

                        order_dict = dict()
                        order_dict['shortcd'] = shortcd
                        order_dict['orderprice'] = ask1
                        if ask1 - bid1 <= 0.03:
                            order_dict['orderprice'] = bid1 + 0.01 * i
                        order_dict['orderqty'] = 1
                        # order_dict['orderprice'] = float(ask1)
                        # order_dict['orderqty'] = 1
                        order_dict['buysell'] = buysell
                        self.orderseq.append(order_dict)
            else:
                logger.info('')

    def initExpireDateUtil(self):
        self.expiredate_util = ExpireDateUtil.ExpireDateUtil()
        now_dt = dt.datetime.now()
        today = now_dt.strftime('%Y%m%d')

        self.expiredate_util.read_expire_date(os.path.dirname(ExpireDateUtil.__file__))
        expire_shortcd_lst = self.expiredate_util.make_expire_shortcd(today)
        logger.info('%s' % ','.join(expire_shortcd_lst))

    def initStrikeList(self):
        self._FeedCodeList = FeedCodeList()
        self._FeedCodeList.ReadCodeListFile()
        option_shortcd_lst = self._FeedCodeList.optionshcodelst
        self.expire_code_lst = list(set([shortcd[3:5] for shortcd in option_shortcd_lst]))
        self.expire_code_lst.sort()
        self.expireMonthCode = self.expire_code_lst[1]
        self.strikelst = list(set([shortcd[-3:] for shortcd in option_shortcd_lst
                                   if shortcd[3:5] == self.expireMonthCode]))
        self.strikelst.sort(reverse=True)

    def find_atm_strike(self):
        put_call_parity_min = 99999
        atm_strike = ''
        for strike in self.strikelst:
            call_shortcd = '201' + self.expire_code_lst[0] + strike
            put_shortcd = '301' + self.expire_code_lst[0] + strike

            bid1 = self.bid1_dict.get(call_shortcd, 0.0)
            ask1 = self.ask1_dict.get(call_shortcd, 0.0)
            if int(bid1 * 100) == 0 or int(ask1 * 100) == 0: continue
            call_mid = (ask1 + bid1) * 0.5

            bid1 = self.bid1_dict.get(put_shortcd, 0.0)
            ask1 = self.ask1_dict.get(put_shortcd, 0.0)
            if int(bid1 * 100) == 0 or int(ask1 * 100) == 0: continue
            put_mid = (ask1 + bid1) * 0.5

            put_call_parity = abs(call_mid - put_mid)
            if put_call_parity_min > put_call_parity:
                put_call_parity_min = put_call_parity
                atm_strike = strike

        return atm_strike
        pass

    def find_target_shortcd(self, callput):
        target_shortcd = None
        min_bid1 = 9999
        if callput == 'call':
            self.strikelst.sort(reverse=True)
            shortcd = '201' + self.expireMonthCode + self.strikelst[0]
            bid1 = self.bid1_dict.get(shortcd, 0.0)
            ask1 = self.ask1_dict.get(shortcd, 0.0)
            mid = (ask1 + bid1) * 0.5
            if 0.15 < mid < 0.60: return shortcd
            for strike in self.strikelst:
                if int(strike) < int(self.atm_strike) * 1.10: continue
                shortcd = '201' + self.expireMonthCode + strike
                bid1 = self.bid1_dict.get(shortcd, 0.0)
                ask1 = self.ask1_dict.get(shortcd, 0.0)
                bid_ask_spread = ask1 - bid1
                if 0 < bid_ask_spread <= 0.03 and 0.03 <= bid1 <= 0.15 and min_bid1 > bid1:
                    min_bid1 = bid1
                    target_shortcd = shortcd

            return target_shortcd
        elif callput == 'put':
            self.strikelst.sort()
            shortcd = '301' + self.expireMonthCode + self.strikelst[0]
            bid1 = self.bid1_dict.get(shortcd, 0.0)
            ask1 = self.ask1_dict.get(shortcd, 0.0)
            mid = (ask1 + bid1) * 0.5
            if 0.15 < mid < 0.60: return shortcd

            for strike in self.strikelst:
                if int(strike) > int(self.atm_strike) * 0.90: continue
                shortcd = '301' + self.expireMonthCode + strike
                bid1 = self.bid1_dict.get(shortcd, 0.0)
                ask1 = self.ask1_dict.get(shortcd, 0.0)
                bid_ask_spread = ask1 - bid1
                if 0 < bid_ask_spread <= 0.03 and 0.10 <= bid1 <= 0.15 and min_bid1 > bid1:
                    min_bid1 = bid1
                    target_shortcd = shortcd

            return target_shortcd
        else:
            return target_shortcd

    def sendOrder(self, shortcd, orderprice, orderqty, buysell):
        if shortcd[:3] in ['201', '301']:
            msg_dict = {}
            msg_dict['AutoTraderID'] = 'OTM001'
            msg_dict['ShortCD'] = shortcd
            msg_dict['OrderPrice'] = orderprice
            msg_dict['OrderQty'] = orderqty
            msg_dict['BuySell'] = buysell
            msg_dict['NewAmendCancel'] = 'N'
            msg_dict['OrderType'] = 2  # market = 1 limit = 2
            msg_dict['TimeInForce'] = 'GFD'
            logger.info('Send Order->' + str(msg_dict))
            try:
                self.socket.send_pyobj(msg_dict)
                msg_in = self.socket.recv()
            except:
                e = sys.exc_info()[0]
                logger.info("zmq send_pyobj error: %s" % e)
                raise
            logger.info('Recv Msg->' + msg_in)

    def onClick(self):
        isThreadRun = self._tickreceiverthread.isRunning()
        if not isThreadRun:
            self._tickreceiverthread.start()
            self._executionreportthread.start()
            self.ui.pushButton_Start.setText('Stop')
            self.qtimer.start(10000)
        elif isThreadRun:
            self._tickreceiverthread.stop()
            self._executionreportthread.stop()
            self._tickreceiverthread.terminate()
            self._executionreportthread.terminate()
            self._tickreceiverthread.wait()
            self._executionreportthread.wait()
            self.ui.pushButton_Start.setText('Start')
            self.qtimer.stop()
        pass

    def on_timer(self):
        now_dt = dt.datetime.now()
        # print 'on_timer->' + str(now_dt)
        if (len(self.orderseq) >= 1) or (self.order_cnt > 0): return
        self.init_orderseq()
        pass

    def updateTableWidgetItem(self, row, col, text):
        widget_item = self.ui.tableWidget.item(row, col)
        if not widget_item:
            new_item = QtGui.QTableWidgetItem(text)
            if col in self.alignRightColumnList:
                new_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            elif col in self.alignCenterColumnList:
                new_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.tableWidget.setItem(row, col, new_item)
        else:
            widget_item.setText(text)
        pass

    def onReceiveData(self, msg_dict):
        if msg_dict['TAQ'] == 'Q' and msg_dict['SecuritiesType'] == 'options':
            nowtime = dt.datetime.now()
            int_nowtime = nowtime.hour * 100 + nowtime.minute

            if len(self.orderseq) > 0 and ((800 <= int_nowtime < 1535) or (int_nowtime >= 1750 or int_nowtime < 400)):
                if self._orderthread.isRunning(): return
                order_dict = self.orderseq.pop(0)

                # self.sendOrder(order_dict['shortcd'], order_dict['orderprice'],
                #                order_dict['orderqty'], buysell)
                self._orderthread.setNewOrder(self.autotrader_id,
                                              order_dict['shortcd'],
                                              order_dict['orderprice'],
                                              order_dict['orderqty'],
                                              order_dict['buysell']
                                              )
                self.order_qu.append(order_dict)
                self.order_cnt += 1
                self._orderthread.sendNewOrder()
                #####################
                ## this part is needed to refactory to onReceiveAck @function
                # pos = self.position_shortcd_lst.index(order_dict['shortcd'])
                # liveqty = str(order_dict['orderqty'])

                # if buysell == 'sell': liveqty = '-' + liveqty
                # self.updateTableWidgetItem(pos, 6, liveqty)
                # self.updateTableWidgetItem(pos, 7, str(order_dict['orderprice']))
                # self.liveqty_dict[order_dict['shortcd']] = int(liveqty) + self.liveqty_dict.get(order_dict['shortcd'],0)
                # logger.info('%s liveqty-> %d' % (order_dict['shortcd'], self.liveqty_dict[order_dict['shortcd']]))
                #######################

            shortcd = msg_dict['ShortCD']
            if not (shortcd in self.position_shortcd_lst): return
            pos = self.position_shortcd_lst.index(shortcd)

            ask1 = float(msg_dict['Ask1'])
            bid1 = float(msg_dict['Bid1'])
            askqty1 = int(msg_dict['AskQty1'])
            bidqty1 = int(msg_dict['BidQty1'])

            # print nowtime, str(shortcd), askqty1, ask1, bid1, bidqty1
            holdqty = long(self.holdqty_lst[pos])
            midprice = (bid1 + ask1) * 0.5
            midprice_old = (float(self.bid1_dict[shortcd]) + float(self.ask1_dict[shortcd])) * 0.5
            buysell = self.buysell_lst[pos]
            pnl = (midprice - self.avgexecprice_dict[shortcd]) * self.position_dict[shortcd]
            pnl_diff = (midprice - midprice_old) * holdqty
            if buysell == 'S':
                pnl *= -1.0
                pnl_diff *= -1.0
            self.total_pnl += pnl_diff

            self.updateTableWidgetItem(pos, 2, '%.3f' % pnl)
            self.updateTableWidgetItem(pos, 4, '%.2f' % ask1)
            self.updateTableWidgetItem(pos, 5, '%.2f' % bid1)

            self.updateTableWidgetItem(len(self.position_shortcd_lst), 2,  "%.3f" % self.total_pnl)

            self.ask1_dict[shortcd] = ask1
            self.bid1_dict[shortcd] = bid1

        pass

    def onReceiveOrderAck(self, msg_dict):
        # msg_in indicate only recv_ack_code
        # ack_code
        # 00040: buy limit order
        # 00039: sell limit order
        # OK: normal @EUREX
        # But how can here know that shortcd, orderqty, orderprice ??
        # So, msg_in replace to msg_dict
        # At first, We decide to use only both msg_code and order_qu, although that can't make safe code.
        order_dict = self.order_qu.popleft()
        if msg_dict['MsgCode'] in ['00040', '00039', 'OK', '00000']:
            liveqty = int(msg_dict['OrderQty'])
            # assume new order only same buysell code
            if msg_dict['BuySell'] == 'S': liveqty *= -1
            self.liveqty_dict[msg_dict['ShortCD']] = liveqty + self.liveqty_dict.get(msg_dict['ShortCD'], 0)
            liveqty = str(liveqty)
            logger.info('%s liveqty-> %d' % (msg_dict['ShortCD'], self.liveqty_dict[msg_dict['ShortCD']]))
            pos = 0
            if msg_dict['ShortCD'] in self.position_shortcd_lst:
                pos = self.position_shortcd_lst.index(msg_dict['ShortCD'])
                self.updateTableWidgetItem(pos, 6, liveqty)
                self.updateTableWidgetItem(pos, 7, str(msg_dict['OrderPrice']))
            else:
                return
        else:
            logger.warn('msg_code: %s -> not normal msg_code' % msg_dict['MsgCode'])
        pass

    def onReceiveExecution(self, data_dict):
        if data_dict['AutoTraderID'] == 'OTM001':
            exec_data_dict = dict()
            exec_data_dict['autotrader_id'] = 'OTM001'
            exec_data_dict['datetime'] = data_dict['TimeStamp']
            exec_data_dict['shortcd'] = data_dict['ShortCD']
            exec_data_dict['execprice'] = float(data_dict['ExecPrice'])
            exec_data_dict['execqty'] = int(data_dict['ExecQty'])
            exec_data_dict['buysell'] = data_dict['BuySell']

            shortcd = exec_data_dict['shortcd']
            execqty = exec_data_dict['execqty']
            buysell = exec_data_dict['buysell']
            liveqty = self.liveqty_dict.get(shortcd, 0)
            if liveqty != 0:
                if buysell == 'S':
                    self.liveqty_dict[shortcd] = liveqty + execqty
                else:
                    self.liveqty_dict[shortcd] = liveqty - execqty
            print self.liveqty_dict

            updateNewPositionEntity(self._session, exec_data_dict)
            self.updatePostionTable()
        else:
            ordno_dict = self.redis_client.hgetall('ordno_dict')
            if data_dict['OrderNo'] in ordno_dict:
                logger.info('already ordno <-> autotrader_id')
            else:
                logger.info('not match ordno <-> autotrader_id')
        pass

    def updatePostionTable(self):
        rows = self._session.query(PositionEntity).filter(PositionEntity.holdqty > 0).all()
        if len(rows) == 0:
            self.ui.tableWidget.setRowCount(1)
            self.position_shortcd_lst = []
            self.holdqty_lst = []
            self.avgexecprice_lst = []
            self.buysell_lst = []
        else:
            self.position_entity_dict.clear()
            for row in rows:
                self.position_entity_dict[row.shortcd] = row

            rows = self._session.query(PositionEntity.shortcd).filter(PositionEntity.holdqty > 0).all()
            self.position_shortcd_lst = list(zip(*rows)[0])

            rows = self._session.query(PositionEntity.holdqty).filter(PositionEntity.holdqty > 0).all()
            self.holdqty_lst = list(zip(*rows)[0])

            rows = self._session.query(PositionEntity.avgexecprice).filter(PositionEntity.holdqty > 0).all()
            self.avgexecprice_lst = list(zip(*rows)[0])

            rows = self._session.query(PositionEntity.buysell).filter(PositionEntity.holdqty > 0).all()
            self.buysell_lst = list(zip(*rows)[0])

        self.ui.tableWidget.setRowCount(len(self.position_shortcd_lst) + 1)
        self.ui.tableWidget.resizeRowsToContents()

        self.total_pnl = 0

        for i in xrange(len(self.position_shortcd_lst)):
            shortcd = self.position_shortcd_lst[i]
            self.position_dict[shortcd] = int(self.holdqty_lst[i])
            self.avgexecprice_dict[shortcd] = self.avgexecprice_lst[i]
            ask1 = self.ask1_dict.get(shortcd, 0.0)
            bid1 = self.bid1_dict.get(shortcd, 0.0)
            midprice = (float(bid1) + float(ask1)) * 0.5

            pos = self.position_shortcd_lst.index(shortcd)
            buysell = self.buysell_lst[pos]
            pnl = (midprice - self.avgexecprice_dict[shortcd]) * self.position_dict[shortcd]
            if buysell in ['sell', 'S']: pnl *= -1.0
            str_holdqty = str(self.holdqty_lst[i])
            if buysell in ['sell', 'S']:
                str_holdqty = '-' + str_holdqty

            self.updateTableWidgetItem(i, 0, self.position_shortcd_lst[i])
            self.updateTableWidgetItem(i, 1, str_holdqty)
            self.updateTableWidgetItem(i, 2, "%.3f" % pnl)
            self.updateTableWidgetItem(i, 3, "%.3f" % self.avgexecprice_dict[shortcd])
            self.updateTableWidgetItem(i, 4, "%.2f" % float(ask1))
            self.updateTableWidgetItem(i, 5, "%.2f" % float(bid1))
            self.updateTableWidgetItem(i, 6, "%d" % self.liveqty_dict.get(self.position_shortcd_lst[i], 0))
            self.updateTableWidgetItem(i, 7, '')

            self.total_pnl += pnl

        if len(self.position_shortcd_lst) == 0:
            i = -1

        self.updateTableWidgetItem(i + 1, 0, 'Total')
        self.updateTableWidgetItem(i + 1, 1, '')
        self.updateTableWidgetItem(i + 1, 2, "%.3f" % self.total_pnl)
        self.updateTableWidgetItem(i + 1, 3, '')
        self.updateTableWidgetItem(i + 1, 4, '')
        self.updateTableWidgetItem(i + 1, 5, '')
        self.updateTableWidgetItem(i + 1, 6, '')
        self.updateTableWidgetItem(i + 1, 7, '')


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    app.exec_()