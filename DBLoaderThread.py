# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 15:00:36 2015

@author: assa
"""

import os
import redis
import pandas as pd
import datetime as dt
import sqlite3 as lite
import zerooptionviewer_parser as fo_parser
import zeroequityviewer_parser as eq_parser
from PyQt4 import QtCore
from SubscribeReceiverThread import SubscribeThread


class DBLoaderThread(SubscribeThread):
    MsgNotify = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, subtype='BackTest'):
        SubscribeThread.__init__(self, parent, subtype=subtype)
        self.count = 0
        self.count_remain = 10
        self.FutOpt_Id_tag = -1
        self.Equity_Id_tag = -1
        self.night_chk = 1
        self.time_chk = True
        self.redis_client = 0
        self.initDB()
        pass

    def initDB(self):
        import time
        strtime = time.strftime('%Y%m%d',time.localtime())
        nowtime = time.localtime()
        self.redis_client = redis.Redis()
        if 7 <= nowtime.tm_hour < 16:
            self.strdbname = "TAQ_%s.db" % strtime
            self.night_chk = 0
        elif nowtime.tm_hour >= 16:
            self.strdbname = "TAQ_Night_%s.db" % strtime
            self.night_chk = 1
        elif nowtime.tm_hour < 7:
            # need to imporve part of strtime
            strtime = "%d%.2d%.2d" %(nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday-1)
            self.strdbname = "TAQ_Night_%s.db" % strtime
            self.night_chk = 1

        self.initMemoryDB(self.night_chk)
        if not os.path.isfile(self.strdbname):
            self.initFileDB(self.night_chk)
        else:
            self.conn_file = lite.connect(self.strdbname, check_same_thread=False)
            self.MsgNotify.emit('reading from file DB...')
            df = pd.read_sql("""SELECT * From FutOptTickData""", self.conn_file)
            if len(df) > 0:
                self.MsgNotify.emit('loading from file DB to memory DB...')
                # pd.io.sql.write_frame(df, "FutOptTickData", self.conn_memory, 'sqlite', 'replace')
                df.to_sql("FutOptTickData", self.conn_memory, 'sqlite', if_exists='replace')
                self.count = int(df['Id'].irow(-1))
                self.FutOpt_Id_tag = df['Id'].irow(-1)
                self.count_remain = self.count % 1000 + 10
                self.MsgNotify.emit('Start Count: ' + str(self.count))
        pass

    def initMemoryDB(self,night_chk):
        self.conn_memory = lite.connect(":memory:", check_same_thread=False)
        self.conn_memory.execute("DROP TABLE IF EXISTS FutOptTickData")
        # Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
        self.conn_memory.execute("""CREATE TABLE FutOptTickData(Id INTEGER NOT NULL PRIMARY KEY,
                                       ShortCD TEXT,
                                       FeedSource TEXT,
                                       TAQ TEXT,
                                       SecuritiesType TEXT,
                                       Time TEXT,
                                       BuySell TEXT,
                                       LastPrice TEXT, LastQty TEXT,
                                       Bid1 TEXT, Ask1 TEXT,
                                       Bid2 TEXT, Ask2 TEXT,
                                       Bid3 TEXT, Ask3 TEXT,
                                       Bid4 TEXT, Ask4 TEXT,
                                       Bid5 TEXT, Ask5 TEXT,
                                       BidQty1 TEXT, AskQty1 TEXT,
                                       BidQty2 TEXT, AskQty2 TEXT,
                                       BidQty3 TEXT, AskQty3 TEXT,
                                       BidQty4 TEXT, AskQty4 TEXT,
                                       BidQty5 TEXT, AskQty5 TEXT,
                                       BidCnt1 TEXT, AskCnt1 TEXT,
                                       BidCnt2 TEXT, AskCnt2 TEXT,
                                       BidCnt3 TEXT, AskCnt3 TEXT,
                                       BidCnt4 TEXT, AskCnt4 TEXT,
                                       BidCnt5 TEXT, AskCnt5 TEXT,
                                       TotalBidQty TEXT, TotalAskQty TEXT,
                                       TotalBidCnt TEXT, TotalAskCnt TEXT
                                       )""")

        if not night_chk:
            self.conn_memory.execute("DROP TABLE IF EXISTS EquityTickData")
            self.conn_memory.execute("""CREATE TABLE EquityTickData(Id INTEGER NOT NULL PRIMARY KEY,
                                           ShortCD TEXT,
                                           FeedSource TEXT,
                                           TAQ TEXT,
                                           SecuritiesType TEXT,
                                           Time TEXT,
                                           BuySell TEXT,
                                           LastPrice TEXT, LastQty TEXT,
                                           Bid1 TEXT, Ask1 TEXT,
                                           Bid2 TEXT, Ask2 TEXT,
                                           Bid3 TEXT, Ask3 TEXT,
                                           Bid4 TEXT, Ask4 TEXT,
                                           Bid5 TEXT, Ask5 TEXT,
                                           Bid6 TEXT, Ask6 TEXT,
                                           Bid7 TEXT, Ask7 TEXT,
                                           Bid8 TEXT, Ask8 TEXT,
                                           Bid9 TEXT, Ask9 TEXT,
                                           Bid10 TEXT, Ask10 TEXT,
                                           BidQty1 TEXT, AskQty1 TEXT,
                                           BidQty2 TEXT, AskQty2 TEXT,
                                           BidQty3 TEXT, AskQty3 TEXT,
                                           BidQty4 TEXT, AskQty4 TEXT,
                                           BidQty5 TEXT, AskQty5 TEXT,
                                           BidQty6 TEXT, AskQty6 TEXT,
                                           BidQty7 TEXT, AskQty7 TEXT,
                                           BidQty8 TEXT, AskQty8 TEXT,
                                           BidQty9 TEXT, AskQty9 TEXT,
                                           BidQty10 TEXT, AskQty10 TEXT,
                                           TotalBidQty TEXT, TotalAskQty TEXT
                                           )""")
        self.conn_memory.commit()
        pass

    def initFileDB(self, night_chk):
        self.conn_file = lite.connect(self.strdbname, check_same_thread=False)
        self.conn_file.execute("DROP TABLE IF EXISTS FutOptTickData")
        self.conn_file.execute("""CREATE TABLE FutOptTickData(Id INTEGER NOT NULL PRIMARY KEY,
                                       ShortCD TEXT,
                                       FeedSource TEXT,
                                       TAQ TEXT,
                                       SecuritiesType TEXT,
                                       Time TEXT,
                                       BuySell TEXT,
                                       LastPrice TEXT, LastQty TEXT,
                                       Bid1 TEXT, Ask1 TEXT,
                                       Bid2 TEXT, Ask2 TEXT,
                                       Bid3 TEXT, Ask3 TEXT,
                                       Bid4 TEXT, Ask4 TEXT,
                                       Bid5 TEXT, Ask5 TEXT,
                                       BidQty1 TEXT, AskQty1 TEXT,
                                       BidQty2 TEXT, AskQty2 TEXT,
                                       BidQty3 TEXT, AskQty3 TEXT,
                                       BidQty4 TEXT, AskQty4 TEXT,
                                       BidQty5 TEXT, AskQty5 TEXT,
                                       BidCnt1 TEXT, AskCnt1 TEXT,
                                       BidCnt2 TEXT, AskCnt2 TEXT,
                                       BidCnt3 TEXT, AskCnt3 TEXT,
                                       BidCnt4 TEXT, AskCnt4 TEXT,
                                       BidCnt5 TEXT, AskCnt5 TEXT,
                                       TotalBidQty TEXT, TotalAskQty TEXT,
                                       TotalBidCnt TEXT, TotalAskCnt TEXT
                                       )""")

        if not night_chk:
            self.conn_file.execute("DROP TABLE IF EXISTS EquityTickData")
            self.conn_file.execute("""CREATE TABLE EquityTickData(Id INTEGER NOT NULL PRIMARY KEY,
                                           ShortCD TEXT,
                                           FeedSource TEXT,
                                           TAQ TEXT,
                                           SecuritiesType TEXT,
                                           Time TEXT,
                                           BuySell TEXT,
                                           LastPrice TEXT, LastQty TEXT,
                                           Bid1 TEXT, Ask1 TEXT,
                                           Bid2 TEXT, Ask2 TEXT,
                                           Bid3 TEXT, Ask3 TEXT,
                                           Bid4 TEXT, Ask4 TEXT,
                                           Bid5 TEXT, Ask5 TEXT,
                                           Bid6 TEXT, Ask6 TEXT,
                                           Bid7 TEXT, Ask7 TEXT,
                                           Bid8 TEXT, Ask8 TEXT,
                                           Bid9 TEXT, Ask9 TEXT,
                                           Bid10 TEXT, Ask10 TEXT,
                                           BidQty1 TEXT, AskQty1 TEXT,
                                           BidQty2 TEXT, AskQty2 TEXT,
                                           BidQty3 TEXT, AskQty3 TEXT,
                                           BidQty4 TEXT, AskQty4 TEXT,
                                           BidQty5 TEXT, AskQty5 TEXT,
                                           BidQty6 TEXT, AskQty6 TEXT,
                                           BidQty7 TEXT, AskQty7 TEXT,
                                           BidQty8 TEXT, AskQty8 TEXT,
                                           BidQty9 TEXT, AskQty9 TEXT,
                                           BidQty10 TEXT, AskQty10 TEXT,
                                           TotalBidQty TEXT, TotalAskQty TEXT
                                           )""")
        self.conn_file.commit()
        pass

    def onReceiveData(self, msg):
        chk = ''
        taqitem = ()
        if type(msg) == str:            
            nowtime = dt.datetime.now()
            lst = msg.split(',')
            chk = lst[2]
            if 7 <= nowtime.hour < 17:
                nightshift = 0
            else:
                nightshift = 1
            if lst[3] in ['futures', 'options']:
                taqitem = fo_parser.msgParser(msg, nightshift, tuple, self.count)
            elif lst[3] == 'equity':
                taqitem = eq_parser.msgParser(msg, tuple, self.count)
        else:
            return

        if chk == 'Q' and lst[3] in ['futures', 'options']:
            wildcard = ','.join('?'*40)
            sqltext = """INSERT INTO FutOptTickData(Id,ShortCD,FeedSource,TAQ,SecuritiesType,Time,Bid1,Ask1,BidQty1,AskQty1,BidCnt1,AskCnt1,
                                                    Bid2,Ask2,BidQty2,AskQty2,BidCnt2,AskCnt2,
                                                    Bid3,Ask3,BidQty3,AskQty3,BidCnt3,AskCnt3,
                                                    Bid4,Ask4,BidQty4,AskQty4,BidCnt4,AskCnt4,
                                                    Bid5,Ask5,BidQty5,AskQty5,BidCnt5,AskCnt5,
                                                    TotalBidQty, TotalAskQty,TotalBidCnt, TotalAskCnt
                                                    )
                                               VALUES(%s)""" % wildcard
            self.redis_client.hset('bid1_dict', taqitem[1], float(taqitem[6]))
            self.redis_client.hset('ask1_dict', taqitem[1], float(taqitem[7]))
            self.redis_client.hset('bidqty1_dict', taqitem[1], float(taqitem[8]))
            self.redis_client.hset('askqty1_dict', taqitem[1], float(taqitem[9]))
            self.redis_client.hset('mid_dict', taqitem[1], (float(taqitem[6]) + float(taqitem[7])) * .5)
        elif chk == 'E' and lst[3] in ['futures', 'options']:
            sqltext = """INSERT INTO FutOptTickData(Id,ShortCD,FeedSource,TAQ,SecuritiesType,Time,LastPrice,BuySell)
                                               VALUES(?, ?, ?, ? ,?, ?, ?, ?)"""
        elif chk == 'T' and lst[3] in ['futures', 'options']:
            # print taqitem
            sqltext = """INSERT INTO FutOptTickData(Id,ShortCD,FeedSource,TAQ,SecuritiesType,Time,LastPrice,LastQty,BuySell,Bid1,Ask1)
                                               VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?)"""
            self.redis_client.hset('lastprice_dict', taqitem[1], float(taqitem[6]))
            self.redis_client.hset('lastqty_dict', taqitem[1], float(taqitem[7]))
            self.redis_client.hset('bid1_dict', taqitem[1], float(taqitem[9]))
            self.redis_client.hset('ask1_dict', taqitem[1], float(taqitem[10]))
            self.redis_client.hset('mid_dict', taqitem[1], (float(taqitem[9]) + float(taqitem[10])) * .5)
        elif chk == 'Q' and lst[3] == 'equity':
            wildcard = ','.join('?'*48)
            sqltext = """INSERT INTO EquityTickData(Id,ShortCD,FeedSource,TAQ,SecuritiesType,Time,
                                                    Bid1,Ask1,BidQty1,AskQty1,
                                                    Bid2,Ask2,BidQty2,AskQty2,
                                                    Bid3,Ask3,BidQty3,AskQty3,
                                                    Bid4,Ask4,BidQty4,AskQty4,
                                                    Bid5,Ask5,BidQty5,AskQty5,
                                                    Bid6,Ask6,BidQty6,AskQty6,
                                                    Bid7,Ask7,BidQty7,AskQty7,
                                                    Bid8,Ask8,BidQty8,AskQty8,
                                                    Bid9,Ask9,BidQty9,AskQty9,
                                                    Bid10,Ask10,BidQty10,AskQty10,
                                                    TotalBidQty, TotalAskQty
                                                    )
                                               VALUES(%s)""" % wildcard
        elif chk == 'E' and lst[3] == 'equity':
            sqltext = """INSERT INTO EquityTickData(Id,ShortCD,FeedSource,TAQ,SecuritiesType,Time,LastPrice,BuySell)
                                               VALUES(?, ?, ?, ? ,?, ?, ?, ?)"""
        elif chk == 'T' and lst[3] == 'equity':
            sqltext = """INSERT INTO EquityTickData(Id,ShortCD,FeedSource,TAQ,SecuritiesType,Time,LastPrice,LastQty,BuySell,Bid1,Ask1)
                                               VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?)"""
        else:
            print taqitem
            print 'no chk type and no parser type'
            return

        if chk != '' and taqitem:
            try:
                self.conn_memory.execute(sqltext, taqitem)
                self.conn_memory.commit()
                if self.count % 1000 == self.count_remain:
                    cursor_fo = self.conn_memory.execute("""SELECT COUNT(*) FROM FutOptTickData""")
                    row_fo = cursor_fo.fetchone()
                    if not self.night_chk:
                        cursor_eq = self.conn_memory.execute("""SELECT COUNT(*) FROM EquityTickData""")
                        row_eq = cursor_eq.fetchone()
                    else:
                        row_eq = [0]
                    msg = 'FutOpt Count: %d, Eq Count: %d' % (row_fo[0], row_eq[0])
                    self.MsgNotify.emit(msg)
                self.count += 1
            except lite.Error as e:
                self.MsgNotify.emit(e.args[0])

        if nowtime.second % 60 == 15 and self.time_chk:
            self.onXTimerUpdate()
            self.time_chk = False
        elif nowtime.second % 60 != 15:
            self.time_chk = True
        pass

    def onXTimerUpdate(self):
        if os.path.isfile(self.strdbname):
            try:
                df_memory = pd.read_sql("""SELECT * From FutOptTickData WHERE Id > %d """ % self.FutOpt_Id_tag, self.conn_memory)
                if len(df_memory) > 0:
                    self.FutOpt_Id_tag = df_memory['Id'].irow(-1)
                    # pd.io.sql.write_frame(df_memory, "FutOptTickData", self.conn_file, 'sqlite', 'append')
                    df_memory.to_sql("FutOptTickData", self.conn_file, 'sqlite', None, 'append', index=False)
                    self.MsgNotify.emit('replicate memory db FutOptTickDataTable to file db: %d' % self.FutOpt_Id_tag)
                else:
                    return
            except Exception, e:
                msg = "An error occurred while futopt replacing : %s" % str(e)
                self.MsgNotify.emit(msg)
                return
            if not self.night_chk:
                try:
                    df_memory = pd.read_sql("""SELECT * From EquityTickData WHERE Id > %d """ % self.Equity_Id_tag, self.conn_memory)
                    if len(df_memory) > 0:
                        self.Equity_Id_tag = df_memory['Id'].irow(-1)
                        # pd.io.sql.write_frame(df_memory, "EquityTickData", self.conn_file, 'sqlite', 'append')
                        df_memory.to_sql("EquityTickData", self.conn_file, 'sqlite', None, 'append', index=False)
                        self.MsgNotify.emit('replicate memory db EquityTickDataTable to file db: %d' % self.Equity_Id_tag)
                    else:
                        return
                except Exception, e:
                    msg = "An error occurred while eq replacing : %s" % str(e)
                    self.MsgNotify.emit(msg)
                    return
        pass

    def stop(self):        
        SubscribeThread.stop(self)
        self.onXTimerUpdate()
        pass
