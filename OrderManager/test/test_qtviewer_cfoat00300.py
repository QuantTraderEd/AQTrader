# -*- coding: utf-8 -*-

import sys
import logging

import zmq
import redis

from PyQt4 import QtGui

from OrderManager.zerooms_main import MainForm
from commutil.FeedCodeList import FeedCodeList
from Script.TotalRun_live_patch import get_process_list


class TestClass(object):
    """
    KOSPI200 Futures Cancel Order Test (KRX or CME)
    """
    logger = logging.getLogger('ZeroOMS.QtViewer_CFOAT00300')

    redis_client = redis.Redis(port=6479)

    # app = QtGui.QApplication(sys.argv)
    # myform = MainForm()
    # myform.show()

    order_port = 6002
    exec_report_port = 7002

    feedcode_list = FeedCodeList()
    feedcode_list.read_code_list()
    futures_shortcd_lst = [feedcode_list.future_shortcd_list[0],
                           feedcode_list.future_shortcd_list[2],
                           ]

    big_shortcd = futures_shortcd_lst[0]
    mini_shortcd = futures_shortcd_lst[1]

    autotrader_id = 'test01'
    shortcd = big_shortcd
    # orderprice = float(redis_client.hget('bid1_dict', shortcd)) - 3.00
    orderprice = 270.00
    orderqty = 1
    buysell = 'B'

    orgordno = ''

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:%d" % order_port)
    socket_exec_report = context.socket(zmq.SUB)
    socket_exec_report.connect("tcp://127.0.0.1:%d" % exec_report_port)
    socket_exec_report.setsockopt(zmq.SUBSCRIBE, "")

    order_dict = dict()
    msg_dict = dict()

    # def test_auto_config(self):
    #     assert self.myform.set_auto
    #     if self.myform.set_auto:
    #         self.myform.slot_ToggleExecute(True)
    #         self.myform.ui.actionExecute.setChecked(True)
    #
    #     assert self.myform.ordermachineThread.isRunning()

    def test_send_neworder_cancelorder(self):

        prcslst = get_process_list()
        assert ("redis-server.exe" in prcslst)

        self.order_dict.clear()
        self.order_dict['AutoTraderID'] = self.autotrader_id
        self.order_dict['ShortCD'] = self.shortcd
        self.order_dict['OrderPrice'] = self.orderprice
        self.order_dict['OrderQty'] = self.orderqty
        self.order_dict['BuySell'] = self.buysell
        self.order_dict['NewAmendCancel'] = 'N'
        self.order_dict['OrderType'] = 2  # market = 1 limit = 2
        self.order_dict['TimeInForce'] = 'GFD'

        # new order
        self.logger.info('Send Order->' + str(self.order_dict))
        self.socket.send_pyobj(self.order_dict)
        msg_dict = self.socket.recv_pyobj()
        self.logger.info('Recv Ack->' + str(msg_dict))
        assert isinstance(msg_dict, dict)
        assert msg_dict['MsgCode'] in ['00040', '00039', 'OK', '00000']
        self.orgordno = msg_dict['OrderNo']

        self.order_dict.clear()
        self.order_dict['AutoTraderID'] = self.autotrader_id
        self.order_dict['ShortCD'] = self.shortcd
        self.order_dict['NewAmendCancel'] = 'C'
        self.order_dict['OrderQty'] = self.orderqty
        self.order_dict['OrgOrderNo'] = self.orgordno

        # cancel order
        self.logger.info('Send Order->' + str(self.order_dict))
        self.socket.send_pyobj(self.order_dict)
        msg_dict = self.socket.recv_pyobj()
        self.logger.info('Recv Ack->' + str(msg_dict))
        assert msg_dict == 'OK'

        while True:
            msg_dict = self.socket_exec_report.recv_pyobj()
            self.logger.info('ExecReport->' + str(msg_dict))
            assert isinstance(msg_dict, dict)
            assert msg_dict['autotrader_id'] == self.autotrader_id
            assert msg_dict['new_amend_cancel'] == 'C'
            assert msg_dict['shortcd'] == self.shortcd
            assert msg_dict['orgordno'] == self.order_dict['OrgOrderNo']
            assert msg_dict['msg_code'] in ['00000', '00156']
            break


