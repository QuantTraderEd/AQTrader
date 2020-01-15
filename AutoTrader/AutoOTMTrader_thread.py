# -*- coding: utf-8 -*-

import zmq
import logging
from PyQt4 import QtCore


class TickDataReceiverThread(QtCore.QThread):
    receiveData = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.msg = ''
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()
        self.port = 5500
        self.logger = logging.getLogger('AutoOTMTrader.TickDataReceiveThread')
        self.logger.info('Init TickDataReceiveThread')

    def run(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:%d" % self.port)
        self.socket.setsockopt(zmq.SUBSCRIBE, "")
        
        while True:
            self.mutex.lock()
            if self.mt_stop: break
            self.mutex.unlock()

            msg_dict = self.socket.recv_pyobj()
            self.receiveData.emit(msg_dict)
            self.onReceiveData(msg_dict)

        pass

    def onReceiveData(self, msg_dict):
        pass
    
    def stop(self):
        self.mt_stop = True
        pass


class ExecutionReportThread(QtCore.QThread):
    receiveData = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.msg = ''
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()
        self.port = 7001
        self.logger = logging.getLogger('AutoOTMTrader.ExecThread')
        self.logger.info('Init ExecThread')

    def run(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:%d" % self.port)
        self.socket.setsockopt(zmq.SUBSCRIBE, "")

        self.logger.info('start')

        while True:
            self.mutex.lock()
            if self.mt_stop: break
            self.mutex.unlock()

            data_dict = self.socket.recv_pyobj()
            self.onReceiveData(data_dict)
            self.receiveData.emit(data_dict)

        pass

    def onReceiveData(self, data_dict):
        self.logger.info('Recv ExecReport -> %s', str(data_dict))
        pass
    
    def stop(self):
        self.mt_stop = True
        pass


class OrderThread(QtCore.QThread):
    receiveData = QtCore.pyqtSignal(dict)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.msg = ''
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()
        self.socket = None
        self.port = 6000  # Real Order_Port
        self.order_dict = dict()
        self.logger = logging.getLogger('AutoOTMTrader.OrderThread')
        self.logger.info('Init OrderThread')

    def run(self):
        shortcd = self.order_dict['ShortCD']
        if shortcd[:3] not in ['201', '301']:
            self.logger.info("shortcd not in [201, 301]")
            return
        self.logger.info('Send Order->' + str(self.order_dict))
        try:
            self.socket.send_pyobj(self.order_dict)
            msg_dict = self.socket.recv_pyobj()
            msg_dict['NewAmendCancel'] = self.order_dict['NewAmendCancel']
            self.logger.info('Recv Ack Msg->' + str(msg_dict))
            self.receiveData.emit(msg_dict)
        except Exception as ex:
            self.logger.info("zmq send/recv error: %s" % str(ex))
            msg_dict = dict()
            msg_dict['MsgCode'] = 'ERROR'
            msg_dict['NewAmendCancel'] = self.order_dict['NewAmendCancel']
            self.receiveData.emit(msg_dict)
            raise
        pass

    def init_zmq(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        # self.socket.setsockopt(zmq.REQ_CORRELATE, 1)
        # self.socket.setsockopt(zmq.REQ_RELAXED, 1)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.setsockopt(zmq.SNDTIMEO, 3000)
        self.socket.setsockopt(zmq.RCVTIMEO, 3000)
        self.socket.connect("tcp://127.0.0.1:%d" % self.port)
        pass

    def set_neworder(self, autotrader_id, shortcd, orderprice, orderqty, buysell):
        self.order_dict.clear()
        self.order_dict['AutoTraderID'] = autotrader_id
        self.order_dict['ShortCD'] = shortcd
        self.order_dict['OrderPrice'] = orderprice
        self.order_dict['OrderQty'] = orderqty
        self.order_dict['BuySell'] = buysell
        self.order_dict['NewAmendCancel'] = 'N'
        self.order_dict['OrderType'] = 2  # market = 1 limit = 2
        self.order_dict['TimeInForce'] = 'GFD'
        pass

    def send_neworder(self):
        self.run()
        pass

    def set_canclorder(self, autotrader_id, org_order_no, shortcd, orderqty):
        self.order_dict.clear()
        self.order_dict['AutoTraderID'] = autotrader_id
        self.order_dict['ShortCD'] = shortcd
        self.order_dict['OrgOrderNo'] = org_order_no
        self.order_dict['OrderQty'] = orderqty
        self.order_dict['NewAmendCancel'] = 'C'
        pass

    def send_canclorder(self):
        self.run()
