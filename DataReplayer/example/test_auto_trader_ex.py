# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
import zmq
from PyQt4 import QtCore

from DataLoader.dataloader.SubscribeReceiverThread import SubscribeThread

logger = logging.getLogger('Test_AutoTrader')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('Test_AutoTrader.log')
fh = RotatingFileHandler('Test_AutoTrader.log', maxBytes=5242*10, backupCount=2)
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


class RecvThread(SubscribeThread):
    trading_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, port=5503):
        SubscribeThread.__init__(self, parent, port)
        self.big_shortcd = '101Q6000'
        self.mini_shortcd = '105Q6000'
        self.big_mid = 0
        self.mini_mid = 0
        self.big_mini_spread = 0
        self.position_limit = 6
        self.position = 0
        self.big_bid = 0
        self.big_ask = 0
        self.mini_bid = 0
        self.mini_ask = 0
        self.mini_spread = 0
        self.cash = 0
        self.big_pnl = 0
        self.mini_pnl = 0
        self.order_thread1 = OrderThread()
        self.order_thread2 = OrderThread()
        self.order_thread1.init_zmq()
        self.order_thread2.init_zmq()
        self.order_thread1.receive_data.connect(self.update_position)
        self.order_thread2.receive_data.connect(self.update_position)
        logger.info('Init RecvThread')

    def onReceiveData(self, msg_dict):
        # logger.info("recv data: %s" % msg_dict)
        if msg_dict['securitiestype'] != u'futures': return

        mid_price = (msg_dict['bid1'] + msg_dict['ask1']) * 0.5
        if msg_dict['shortcd'] == self.big_shortcd:
            self.big_mid = mid_price
            self.big_bid = msg_dict['bid1']
            self.big_ask = msg_dict['ask1']
        elif msg_dict['shortcd'] == self.mini_shortcd:
            self.mini_mid = mid_price
            self.mini_bid = msg_dict['bid1']
            self.mini_ask = msg_dict['ask1']
            self.mini_spread = self.mini_ask - self.mini_bid

        if self.big_mid > 0 and self.mini_mid > 0 and self.mini_spread <= 0.2:
            big_mini_spread = self.big_mid - self.mini_mid
            # msg = "%s %.3f %.3f %.3f" % (msg_dict['datetime'], self.big_mid, self.mini_mid, big_mini_spread)
            # logger.info("%s" % msg)
            if (not self.order_thread1.isRunning()) and (not self.order_thread2.isRunning()):
                if big_mini_spread > 0.04 and self.position < self.position_limit:
                    self.trading_signal.emit(1)
                    self.order_thread1.set_neworder('test01', '101Q6000', self.big_bid, 1, 'S')
                    self.order_thread1.run()
                    self.order_thread2.set_neworder('test01', '105Q5000', self.mini_ask, 5, 'B')
                    self.order_thread2.run()
                elif big_mini_spread < -0.04 and self.position > self.position_limit * -1:
                    self.trading_signal.emit(-1)
                    self.order_thread1.set_neworder('test01', '101Q6000', self.big_ask, 1, 'B')
                    self.order_thread1.run()
                    self.order_thread2.set_neworder('test01', '105Q5000', self.mini_bid, 5, 'S')
                    self.order_thread2.run()

    def update_position(self, msg_dict):
        """
        msg_dict format:
        {
        'AutoTraderID': 'test01',
        'BuySell': 'B',
        'NewAmendCancel': 'N',
        'OrderPrice': 254.0,
        'OrderQty': 1,
        'OrderType': 2,
        'ShortCD': '101Q6000',
        }
        """
        if msg_dict['ShortCD'][:3] in ['101']:
            if msg_dict['BuySell'] == 'S':
                self.position += 1
            elif msg_dict['BuySell'] == 'B':
                self.position -= 1
            logger.info('position: %d' % self.position)

        buysell = 0
        if msg_dict['BuySell'] == 'B':
            buysell = -1
        elif msg_dict['BuySell'] == 'S':
            buysell = 1
        if msg_dict['ShortCD'][:3] in ['101']:
            self.big_pnl += msg_dict['OrderPrice'] * msg_dict['OrderQty'] * buysell
            self.cash += msg_dict['OrderPrice'] * msg_dict['OrderQty'] * buysell * -1
        elif msg_dict['ShortCD'][:3] in ['105']:
            self.mini_pnl += msg_dict['OrderPrice'] * msg_dict['OrderQty'] * buysell * 0.2
            self.cash += msg_dict['OrderPrice'] * msg_dict['OrderQty'] * buysell * 0.2 * -1
            logger.info("pnl: %.3f %.3f %.3f" % (self.big_pnl, self.mini_pnl,
                                                 self.big_pnl + self.mini_pnl))
                                                 # self.position * self.big_mid + self.position * self.mini_mid * -1
                                                 # + self.cash))
        pass


class OrderThread(QtCore.QThread):
    receive_data = QtCore.pyqtSignal(dict)

    def __init__(self, id=0):
        QtCore.QThread.__init__(self)
        self.id = id
        self.msg = ''
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()
        self.socket = None
        self.port = 6010  # Replay Order_Port
        self.order_dict = dict()
        logger.info('Init OrderThread')

    def run(self):
        shortcd = self.order_dict['ShortCD']
        if shortcd[:3] not in ['101', '105']:
            logger.info("shortcd not in [101, 105]")
            return
        logger.info('Send Order->' + str(self.order_dict))
        try:
            self.socket.send_pyobj(self.order_dict)
            msg_dict = self.socket.recv_pyobj()
        except Exception as ex:
            logger.info("zmq send/recv error: %s" % str(ex))
            # msg_dict = dict()
            # msg_dict['MsgCode'] = 'ERROR'
            # msg_dict['NewAmendCancel'] = self.order_dict['NewAmendCancel']
            # self.receiveData.emit(msg_dict)
            self.init_zmq()
            # Re-send order
            self.run()
            raise
        msg_dict['NewAmendCancel'] = self.order_dict['NewAmendCancel']
        logger.info('Recv Ack Msg->' + str(msg_dict))
        self.receive_data.emit(msg_dict)
        pass

    def init_zmq(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        # self.socket.setsockopt(zmq.REQ_CORRELATE, 1)
        # self.socket.setsockopt(zmq.REQ_RELAXED, 1)

        # self.socket.setsockopt(zmq.LINGER, 0)
        # self.socket.setsockopt(zmq.SNDTIMEO, 3000)
        # self.socket.setsockopt(zmq.RCVTIMEO, 3000)
        self.socket.connect("tcp://127.0.0.1:%d" % self.port)
        logger.info('init_zmq done')
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


def main():
    sub_thread = RecvThread(port=5510)
    sub_thread.daemon = True
    sub_thread.run()


if __name__ == "__main__":
    main()
