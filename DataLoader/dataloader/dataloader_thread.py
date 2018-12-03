# -*- coding: utf-8 -*-

import logging
import redis
import datetime as dt

from os import path
from PyQt4 import QtCore
from sqlalchemy import MetaData
from sqlalchemy.ext.serializer import loads, dumps
from SubscribeReceiverThread import SubscribeThread


import sqlalchemy_tickdata_init as tickdata_db_init
from sqlalchemy_tickdata_declarative import TickData
from sqlalchemy_tickdata_insert import insert_new_tickdata


class DBLoaderThread(SubscribeThread):
    MsgNotify = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, subtype='BackTest'):
        SubscribeThread.__init__(self, parent, subtype=subtype)
        self.logger = logging.getLogger('DataLoader.DataLoaderThread')
        self.count = 0
        self.count_remain = 10
        self.count_fo = 0
        self.count_eq = 0
        self.night_chk = 1
        self.redis_client = redis.Redis()
        self.dbname = ''
        self.filepath = path.dirname(__file__)
        # self.initDB()
        pass

    def initDB(self):
        now_dt = dt.datetime.now()
        strtime = now_dt.strftime('%Y%m%d')
        if 7 <= now_dt.hour < 16:
            self.dbname = "TAQ_%s.db" % strtime
            self.night_chk = 0
        elif now_dt.hour >= 16:
            self.dbname = "TAQ_Night_%s.db" % strtime
            self.night_chk = 1
        elif now_dt.hour < 7:
            # need to imporve part of strtime
            strtime = "%d%.2d%.2d" %(now_dt.year, now_dt.month, now_dt.day-1)
            self.dbname = "TAQ_Night_%s.db" % strtime
            self.night_chk = 1

        self.dbname = path.join(self.filepath, self.dbname)
        self.logger.info("set db name: %s" % self.dbname)

        # ORM
        self.MsgNotify.emit('reading from file DB...')
        self._file_session, self._file_engine = tickdata_db_init.init_session(self.dbname)
        self.count = self._file_session.query(TickData).count()
        self.count_fo = self._file_session.query(TickData).filter(
                                                            TickData.securitiestype.in_(['futures', 'options'])
                                                            ).count()
        self.count_eq = self._file_session.query(TickData).filter(TickData.securitiestype == 'equity').count()
        self._memo_session, self._memo_engine = tickdata_db_init.init_session('memory')

        if self.count > 0:
            metadata = MetaData(bind=self._file_engine)
            self._file_session = tickdata_db_init.init_session(self.dbname)[0]
            q = self._file_session.query(TickData)
            serialized_data = dumps(q.all())
            loads(serialized_data, metadata, self._memo_session)
            self._memo_session.commit()
            count = self._memo_session.query(TickData).count()
            self._memo_session.close()

        self._file_session.close()

        self._memo_session = tickdata_db_init.make_session(self._memo_engine)

        self.count_remain = 10
        self.MsgNotify.emit('Start Count: %d' % self.count)
        msg = 'FutOpt Count: %d, Eq Count: %d' % (self.count_fo, self.count_eq)
        self.MsgNotify.emit(msg)
        pass

    def onReceiveData(self, msg_dict):
        nowtime = dt.datetime.now()
        shortcd = msg_dict['ShortCD']
        feedsource = msg_dict['FeedSource']
        taq = msg_dict['TAQ']
        securities_type = msg_dict['SecuritiesType']
        # print msg_dict['TimeStamp'], nowtime
        # print nowtime, msg_dict

        if taq == 'Q' and securities_type in ['futures', 'options']:
            askqty1 = msg_dict['AskQty1']
            ask1 = msg_dict['Ask1']
            bid1 = msg_dict['Bid1']
            bidqty1 = msg_dict['BidQty1']

            self.redis_client.hset('bid1_dict', shortcd, bid1)
            self.redis_client.hset('ask1_dict', shortcd, ask1)
            self.redis_client.hset('bidqty1_dict', shortcd, bidqty1)
            self.redis_client.hset('askqty1_dict', shortcd, askqty1)
            self.redis_client.hset('mid_dict', shortcd, (bid1 + ask1) * .5)

            msg_dict['TimeStamp'] = nowtime
            insert_new_tickdata(self._memo_session, msg_dict)

        elif taq == 'E' and securities_type in ['futures', 'options']:
            msg_dict['TimeStamp'] = nowtime

        elif taq == 'T' and securities_type in ['futures', 'options']:
            lastprice = float(msg_dict['LastPrice'])
            lastqty = int(msg_dict['LastQty'])

            self.redis_client.hset('lastprice_dict', shortcd, lastprice)
            self.redis_client.hset('lastqty_dict', shortcd, lastqty)

            msg_dict['TimeStamp'] = nowtime
            insert_new_tickdata(self._memo_session, msg_dict)

        else:
            return

        if securities_type in ['futures', 'options']:
            self.count_fo += 1
        elif securities_type in ['equity']:
            self.count_eq += 1

        if self.count % 100 == self.count_remain:
            msg = 'FutOpt Count: %d, Eq Count: %d' % (self.count_fo, self.count_eq)
            self.MsgNotify.emit(msg)
            print msg_dict
        self.count += 1
        # print self.count, self.count_fo, self.count_eq
        pass

    def onBackup(self):
        # metadata = MetaData(bind=self._memo_engine)
        # q = self._memo_session.query(TickData)
        # serialized_data = dumps(q.all())
        # loads(serialized_data, metadata, self._file_session)
        # self._file_session.commit()
        pass

    def stop(self):
        SubscribeThread.stop(self)
        self.onBackup()
        pass
