# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 15:00:36 2015

@author: assa
"""

import os
import pandas as pd
import datetime as dt
import sqlite3 as lite
import zerooptionviewer_parser as parser
from PyQt4 import QtCore
from SubscribeReceiverThread import SubscribeThread


class DBLoaderThread(SubscribeThread):
    MsgNotify = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, subtype='BackTest'):
        SubscribeThread.__init__(self, parent, subtype=subtype)
        self.count = 0
        self.count_remain = 10
        self.Id_tag = -1
        self.time_chk = True
        self.initDB()
        pass

    def initDB(self):
        import time
        strtime = time.strftime('%Y%m%d',time.localtime())
        nowtime = time.localtime()
        if 6 <= nowtime.tm_hour < 16:
            self.strdbname = "TAQ_%s.db" % strtime
        elif nowtime.tm_hour >= 16:
            self.strdbname = "TAQ_Night_%s.db" % strtime
        elif nowtime.tm_hour < 6:
            strtime = "%d%.2d%.2d" %(nowtime.tm_year,nowtime.tm_mon,nowtime.tm_mday-1)
            self.strdbname = "TAQ_Night_%s.db" % strtime

        self.initMemoryDB()
        if not os.path.isfile(self.strdbname):
            self.initFileDB()
        else:
            self.MsgNotify.emit('loading from file DB to memory DB...')
            self.conn_file = lite.connect(self.strdbname, check_same_thread=False)
            df = pd.read_sql("""SELECT * From FutOptTickData""", self.conn_file)
            pd.io.sql.write_frame(df, "FutOptTickData", self.conn_memory,'sqlite','replace')
            self.count = int(df['Id'].irow(-1))
            self.Id_tag = df['Id'].irow(-1)
            self.count_remain = self.count % 1000 + 10
            self.MsgNotify.emit('Start Count: ' + str(self.count))
        pass

    def initMemoryDB(self):
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
        self.conn_memory.commit()
        pass

    def initFileDB(self):
        self.conn_file = lite.connect(self.strdbname,check_same_thread=False)
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
            taqitem = parser.msgParser(msg, nightshift, tuple, self.count)
        elif type(msg) == dict:
            row = msg.copy()
            chk = row['TAQ']
            if chk == 'Q':
                taqitem = (self.count, row['ShortCD'],
                           row['FeedSource'],
                           row['TAQ'],
                           row['SecuritiesType'],
                           row['Time'],
                           row['Bid1'], row['Ask1'], row['BidQty1'], row['AskQty1'], row['BidCnt1'], row['AskCnt1'],
                           row['Bid2'], row['Ask2'], row['BidQty2'], row['AskQty2'], row['BidCnt2'], row['AskCnt2'],
                           row['Bid3'], row['Ask3'], row['BidQty3'], row['AskQty3'], row['BidCnt3'], row['AskCnt3'],
                           row['Bid4'], row['Ask4'], row['BidQty4'], row['AskQty4'], row['BidCnt4'], row['AskCnt4'],
                           row['Bid5'], row['Ask5'], row['BidQty5'], row['AskQty5'], row['BidCnt5'], row['AskCnt5'],
                           row['TotalBidQty'], row['TotalAskQty'],
                           row['TotalBidCnt'], row['TotalAskCnt']
                           )
            elif chk == 'T':
                taqitem = (self.count, row['ShortCD'],
                           row['FeedSource'],
                           row['TAQ'],
                           row['SecuritiesType'],
                           row['Time'],
                           row['LastPrice'], row['LastQty'], row['BuySell'],
                           row['Bid1'], row['Ask1']
                           )
            elif chk == 'E':
                taqitem = (self.count, row['ShortCD'],
                           row['FeedSource'],
                           row['TAQ'],
                           row['SecuritiesType'],
                           row['Time'],
                           row['LastPrice'], row['BuySell']
                           )


        if chk == 'Q':
            wildcard = ','.join('?'*40)
            sqltext = """INSERT INTO FutOptTickData(Id,ShortCD,FeedSource,TAQ,SecuritiesType,Time,Bid1,Ask1,BidQty1,AskQty1,BidCnt1,AskCnt1,
                                                    Bid2,Ask2,BidQty2,AskQty2,BidCnt2,AskCnt2,
                                                    Bid3,Ask3,BidQty3,AskQty3,BidCnt3,AskCnt3,
                                                    Bid4,Ask4,BidQty4,AskQty4,BidCnt4,AskCnt4,
                                                    Bid5,Ask5,BidQty5,AskQty5,BidCnt5,AskCnt5,
                                                    TotalBidQty, TotalAskQty,TotalBidCnt, TotalAskCnt
                                                    )
                                               VALUES(%s)""" % wildcard
        elif chk == 'E':
            sqltext = """INSERT INTO FutOptTickData(Id,ShortCD,FeedSource,TAQ,SecuritiesType,Time,LastPrice,BuySell)
                                               VALUES(?, ?, ?, ? ,?, ?, ?, ?)"""
        elif chk == 'T':
            sqltext = """INSERT INTO FutOptTickData(Id,ShortCD,FeedSource,TAQ,SecuritiesType,Time,LastPrice,LastQty,BuySell,Bid1,Ask1)
                                               VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?)"""

        if chk != '':
            try:
                if not nightshift: print taqitem
                self.conn_memory.execute(sqltext, taqitem)
                self.conn_memory.commit()
                if self.count % 1000 == self.count_remain:
                    cursor = self.conn_memory.execute("""SELECT COUNT(*) FROM FutOptTickData""")
                    row = cursor.fetchone()
                    msg = 'Count: %d' % row[0]
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
            self.MsgNotify.emit('replicate memory db to file db, %d, %d' % (self.Id_tag, self.count))
            try:
                df_memory = pd.read_sql("""SELECT * From FutOptTickData WHERE Id > %d """ % self.Id_tag, self.conn_memory)
                self.Id_tag = df_memory['Id'].irow(-1)
                pd.io.sql.write_frame(df_memory, "FutOptTickData", self.conn_file, 'sqlite', 'append')
            except lite.Error as e:
                msg = "An error occurred:", e.args[0]
                self.MsgNotify.emit(msg)
                return
            # print 'test: write file db...'
            # df_memory = df_memory.iloc[:,1:len(df_memory.columns)]


        # else:
            # print 'make new file db'
        pass

    def stop(self):        
        SubscribeThread.stop(self)
        pass
