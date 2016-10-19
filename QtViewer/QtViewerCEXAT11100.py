# -*- coding: utf-8 -*-

import sqlite3 as lite
import redis
from PyQt4 import QtCore
from datetime import datetime


class QtViewerCEXAT11100(QtCore.QObject):
    receive = QtCore.pyqtSignal()

    def __init__(self):
        super(QtViewerCEXAT11100,self).__init__()
        self.dbname = None
        self.flag = True
        self.redis_client = redis.Redis()

    def Update(self, subject):
        print '-' * 20
        if type(subject.data).__name__ == 'dict':
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]
            # print 'szMessage',  subject.data['szMessage']
            # print 'szMessageCode', subject.data['szMessageCode'],

            autotrader_id = subject.autotrader_id
            ordno = subject.data['OrdNo']
            if subject.data['szMessageCode'] in ['00030', '00040']:
                self.redis_client.hset('ordno_dict', int(ordno), autotrader_id)

            if subject.data['BnsTpCode'] == '2': buysell = 'buy'
            elif subject.data['BnsTpCode'] == '1': buysell = 'sell'
            else: buysell = None

            # shcode = subject.data['FnoIsuNo']
            shcode = subject.shortcd
            price = subject.data['OrdPrc']
            qty = subject.data['OrdQty']
            unexecqty = qty
            type1 = None
            type2 = None
            if subject.data['ErxPrcCndiTpCode'] != '':
                if subject.data['ErxPrcCndiTpCode'] == '0': type1 = 'market'
                elif subject.data['ErxPrcCndiTpCode'] == '2':
                    type1 = 'limit'
                    type2 = 'GFD'

            chkreq = subject.data['szMessageCode']

            orderitem = (autotrader_id, ordno,strnowtime,buysell,shcode,price,qty,type1,type2,unexecqty,chkreq)
            # print orderitem
            if self.dbname != None:
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()
                wildcard = '?,' * len(orderitem)
                wildcard = wildcard[:-1]
                cursor_db.execute("""INSERT INTO OrderList(AutoTraderID,
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
                conn_db.commit()
                conn_db.close()
                self.receive.emit()

        self.flag = False
