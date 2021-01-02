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
    def __init__(self, tick_port=5510, order_port=6010, exec_report_port=7010, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.tick_port = tick_port      # real:5500 test: 5510
        self.order_port = order_port    # real: 6001 test: 6002
        self.exec_report_port = exec_report_port   # real: 7001 test: 7002
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pause_condition = QtCore.QWaitCondition()
        self.context = None
        self.logger = logging.getLogger('replay_order_manager.RepThread')
        self.logger.info('Init Thread')

    def init_zmq(self):
        if self.context is None:
            self.logger.warn('context is None / create new context')
            self.context = zmq.Context()

        self.socket_tick = self.context.socket(zmq.SUB)
        self.socket_tick.connect("tcp://127.0.0.1:%s" % self.tick_port)
        self.socket_tick.setsockopt(zmq.SUBSCRIBE, "")

        self.socket_order = self.context.socket(zmq.REP)
        self.socket_order.bind("tcp://127.0.0.1:%d" % self.order_port)
        # self.socket = context.socket(zmq.DEALER)
        # self.socket.connect("tcp://127.0.0.1:6001")

        self.socket_execution_report = self.context.socket(zmq.PUB)
        self.socket_execution_report.bind("tcp://127.0.0.1:%d" % self.exec_report_port)

        self.poller = zmq.Poller()
        self.poller.register(self.socket_tick, zmq.POLLIN)
        self.poller.register(self.socket_order, zmq.POLLIN)

        self.logger.info('tick_port: %d' % self.tick_port)
        self.logger.info('order_port: %d' % self.order_port)
        self.logger.info('exec_report_port: %d' % self.exec_report_port)

    def run(self):

        while True:
            socks = dict(self.poller.poll())
            if self.socket_order in socks and socks[self.socket_order] == zmq.POLLIN:
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
                self.logger.info('===================' * 2)
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
                self.logger.info('\n' + logmsg)

                if newamendcancel == 'N' and (shortcd[:3] in ['101', '105', '201', '301', ]):
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

                    self.socket_order.send_pyobj(msg_dict)

                # elif newamendcancel == 'C' and (shortcd[:3] in ['101', '201', '301', '105']):
                #     send_dict['MsgCode'] = 'OK'
                #     self.logger.info('OK')
                #     self.socket_order.send_pyobj(send_dict)

            elif self.socket_tick in socks and socks[self.socket_tick] == zmq.POLLIN:
                msg_dict = self.socket_tick.recv_pyobj()
                msg = "%s %s %.2f %.2f" % (msg_dict['datetime'],
                                           msg_dict['shortcd'],
                                           msg_dict['bid1'],
                                           msg_dict['ask1'])
                self.logger.info("recv: %s" % msg)

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


