# -*- coding: utf-8 -*-

import time
import datetime as dt
import logging
import pprint
import zmq
import sqlite3 as lite
import pandas as pd
from PyQt4 import QtCore


class ReplyThread(QtCore.QThread):
    def __init__(self, order_port=6001, exec_report_port=7001, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.order_port = order_port
        self.exec_report_port = exec_report_port
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pause_condition = QtCore.QWaitCondition()
        self.logger = logging.getLogger('DataReplayer.RepThread')
        self.logger.info('Init Thread')

    def init_zmq(self):
        self.context = zmq.Context()
        self.socket_order = self.context.socket(zmq.REP)
        self.socket_order.bind("tcp://127.0.0.1:%d" % self.order_port)
        # self.socket = context.socket(zmq.DEALER)
        # self.socket.connect("tcp://127.0.0.1:6001")

        self.socket_execution_report = self.context.socket(zmq.PUB)
        self.socket_execution_report.bind("tcp://127.0.0.1:%d" % self.exec_report_port)

    def run(self):
        self.init_zmq()

        while True:
            msg_dict = self.socket_order.recv_pyobj()
            send_dict = dict()

            if type(msg_dict) != dict:
                send_dict['MsgCode'] = 'NotMsgDict'
                self.logger.info(str(msg_dict) + 'is not dict')
                self.socket_order.send_pyobj(send_dict)
                continue

            nowtime = dt.datetime.now()
            # strnowtime = datetime.strftime(nowtime, "%Y-%m-%d %H:%M:%S.%f")
            # strnowtime = strnowtime[:-3]
            self.logger.info('===================' * 4)
            self.logger.info('receive_order')

            newamendcancel = msg_dict.get('NewAmendCancel', ' ')  # 'N' = New, 'A' = Amend, 'C' = Cancel
            buysell = msg_dict.get('BuySell', '')  # 'B' = Buy, 'S' = 'Sell'
            shortcd = msg_dict.get('ShortCD', '')
            orderprice = msg_dict.get('OrderPrice', 0)
            orderqty = msg_dict.get('OrderQty', 0)
            ordertype = msg_dict.get('OrderType', 0)  # 1 = Market, 2 = Limit
            timeinforce = msg_dict.get('TimeInForce', 'GFD')  # GFD, IOC, FOK
            autotrader_id = msg_dict.get('AutoTraderID', '0')
            orgordno = msg_dict.get('OrgOrderNo', -1)

            if not isinstance(orderprice, float) and newamendcancel in ['N', 'A']:
                send_dict['MsgCode'] = 'Not OrderPrice Float'
                self.logger.info('fail: ' + str(msg_dict) + ' orderprice not float')
                self.socket_order.send_pyobj(send_dict)
                continue

            logmsg = pprint.pformat(msg_dict)
            self.logger.info(logmsg)

            if newamendcancel == 'N' and (shortcd[:3] in ['101', '201', '301', '105']):
                msgcode = '0000'
                ordno = '0000'
                msg_dict = dict()
                msg_dict['AutoTraderID'] = autotrader_id
                msg_dict['OrderNo'] = ordno
                msg_dict['TimeStamp'] = nowtime
                msg_dict['ShortCD'] = shortcd
                msg_dict['OrderPrice'] = orderprice
                msg_dict['OrderQty'] = orderqty
                msg_dict['BuySell'] = buysell
                msg_dict['MsgCode'] = msgcode

                self.zmq_socket_order.send_pyobj(msg_dict)

            # elif newamendcancel == 'C' and (shortcd[:3] in ['101', '201', '301', '105']):
            #     send_dict['MsgCode'] = 'OK'
            #     self.logger.info('OK')
            #     self.socket_order.send_pyobj(send_dict)

            self.mutex.lock()
            if self.mt_stop:
                break
            if self.mt_pause:
                self.mt_pauseCondition.wait(self.mutex)
            self.mutex.unlock()

    def mtf_stop(self):
        self.mt_stop = True

    def mtf_pause(self):
        self.mt_pause = True

    def mtf_resume(self):
        self.mt_pause = False
        self.mt_pause_condition.wakeAll()

    def mtf_reset(self):
        self.mt_stop = False
        self.mt_pause = False
        self.mutex.unlock()


