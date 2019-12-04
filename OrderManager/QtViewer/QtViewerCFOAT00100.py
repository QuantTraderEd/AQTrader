# -*- coding: utf-8 -*-


import logging
import sqlite3 as lite
import redis
from PyQt4 import QtCore
from datetime import datetime


class QtViewerCFOAT00100(QtCore.QObject):
    """
    kospi200 futures & options normal order
    """
    receive = QtCore.pyqtSignal()

    def __init__(self, zmq_socket_order=None, parent=None):
        super(QtViewerCFOAT00100, self).__init__(parent)
        self.zmq_socket_order = zmq_socket_order
        self.dbname = None
        self.flag = True
        self.conn = None
        self.redis_client = redis.Redis()
        self.logger = logging.getLogger('ZeroOMS.Thread.CFOAT00100')
        self.logger.info('init QtViewerCFOAT00100')

    def initDB(self):
        if self.dbname is not None:
            self.conn = lite.connect(self.dbname)
        pass
        
    def Update(self, subject):
        if type(subject.data) != dict:
            self.flag = False
            return

        nowtime = datetime.now()
        strnowtime = datetime.strftime(nowtime, '%H:%M:%S.%f')[:-3]
        sz_msg = subject.data['szMessage']
        msgcode = subject.data['szMessageCode']
        self.logger.info(sz_msg.strip() + msgcode)

        autotrader_id = subject.autotrader_id
        ordno = subject.data['OrdNo']
        self.logger.info('Update: OrdNo-> %s, autotrader_id-> %s' % (ordno, autotrader_id))
        # if subject.data['szMessageCode'] in ['00030', '00040']:
        if str(ordno).isdigit():
            self.redis_client.hset('ordno_dict', int(ordno), autotrader_id)

        if subject.data['BnsTpCode'] == '2': buysell = 'buy'
        elif subject.data['BnsTpCode'] == '1': buysell = 'sell'
        else: buysell = None

        shortcd = subject.data['FnoIsuNo']
        ordprice = subject.data['OrdPrc']
        ordqty = subject.data['OrdQty']
        unexecqty = ordqty
        type1 = None
        type2 = None
        if subject.data['FnoOrdPtnCode'] != '':
            if subject.data['FnoOrdPtnCode'][1] == '0': type1 = 'limit'
            elif subject.data['FnoOrdPtnCode'][1] == '3': type1 = 'market'

            if subject.data['FnoOrdPtnCode'][0] == '0': type2 = 'GFD'
            elif subject.data['FnoOrdPtnCode'][0] == '1': type2 = 'IOC'
            elif subject.data['FnoOrdPtnCode'][0] == '2': type2 = 'FOK'

        orderitem = (autotrader_id, ordno, strnowtime, buysell, shortcd, ordprice, ordqty,
                     type1, type2, unexecqty, msgcode)
        wildcard = "?," * len(orderitem)
        wildcard = wildcard[:-1]

        if buysell == 'buy': buysell = 'B'
        elif buysell == 'sell': buysell = 'S'
        else: buysell = ''

        msg_dict = dict()
        msg_dict['AutoTraderID'] = autotrader_id
        msg_dict['OrderNo'] = ordno
        msg_dict['TimeStamp'] = nowtime
        msg_dict['ShortCD'] = shortcd
        msg_dict['OrderPrice'] = ordprice
        msg_dict['OrderQty'] = ordqty
        msg_dict['BuySell'] = buysell
        msg_dict['MsgCode'] = msgcode

        self.zmq_socket_order.send_pyobj(msg_dict)

        # print orderitem
        self.logger.info('%s' % str(orderitem))
        if type(self.conn) == lite.Connection:
            # conn_db = lite.connect(self.dbname)
            # cursor_db = conn_db.cursor()
            self.conn.execute("""INSERT INTO OrderList
                                 (AutoTraderID,
                                  OrdNo,
                                  Time,
                                  BuySell,
                                  ShortCD,
                                  Price,
                                  Qty,
                                  Type1,
                                  Type2,
                                  UnExecQty,
                                  ChkReq)
                                  VALUES(%s)""" % wildcard, orderitem)
            self.conn.commit()
            # conn_db.close()
            # self.emit(QtCore.SIGNAL("OnReceiveData (QString)"),'CSPAT00600')
            self.receive.emit()

        self.flag = False    
