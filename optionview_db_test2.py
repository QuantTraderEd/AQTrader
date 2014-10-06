# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 16:52:59 2014

@author: assa
"""

import os
import time
import pandas as pd
import sqlite3 as lite
from datetime import datetime
from PyQt4 import QtGui, QtCore
from zerooptionviewer_thread import OptionViewerThread

def convert(strprice):
    return '%.2f' %round(float(strprice),2)


class OptionsDBTest(QtGui.QWidget):
    def __init__(self,parent = None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initDB()
        self.initTimer()
        self.initThread()
        
    def initUI(self):
        self.button = QtGui.QPushButton('Start', self)
        self.button.clicked.connect(self.onClick)
        self.button.move(60, 50)
        self.setWindowTitle('TAQ_DB')
        self.resize(200, 120)
        pass
    
    def initThread(self):
        self.mythread = OptionViewerThread(None)
        self.mythread.receiveData[str].connect(self.onReceiveData)
        pass

    def initTimer(self):
        self.XTimer = QtCore.QTimer()
        self.XTimer.timeout.connect(self.onXTimerUpdate)
        pass
        
    def initDB(self):
        strtime = time.strftime('%Y%m%d',time.localtime())
        self.strdbname = "TAQ_%s.db" %(strtime)
        self.initMemoryDB()
        self.initBufferDB()
        if not os.path.isfile(self.strdbname):        
            self.initFileDB()
        else:
            print 'loading from file DB to memory DB'
            self.conn_file = lite.connect(self.strdbname)
            self.cursor_file = self.conn_file.cursor()
            df = pd.read_sql("""SELECT * From FutOptTickData""",self.conn_file)
            pd.io.sql.write_frame(df, "FutOptTickData", self.conn_memory,'sqlite','replace')
        pass

    def initMemoryDB(self):
        self.conn_memory = lite.connect(":memory:")
        self.cursor_memory = self.conn_memory.cursor()
        self.cursor_memory.execute("DROP TABLE IF EXISTS FutOptTickData")
        self.cursor_memory.execute("""CREATE TABLE FutOptTickData(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
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
        pass

    def initBufferDB(self):
        self.conn_buffer = lite.connect(":memory:")
        self.cursor_buffer = self.conn_buffer.cursor()
        self.cursor_buffer.execute("DROP TABLE IF EXISTS FutOptTickData")
        self.cursor_buffer.execute("""CREATE TABLE FutOptTickData(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
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
        pass

    def initFileDB(self):
        self.conn_file = lite.connect(self.strdbname)
        self.cursor_file = self.conn_file.cursor()
        self.cursor_file.execute("DROP TABLE IF EXISTS FutOptTickData")
        self.cursor_file.execute("""CREATE TABLE FutOptTickData(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
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
        pass
    
    def onReceiveData(self,msg):
        nowtime = datetime.now()
        strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]
        lst = msg.split(',')
        chk = ''
        buysell = ''     
        taqitem = ()
        
        if lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'futures':            
            shcode = str(lst[4]) + '000'
            if nowtime.hour >= 7 and nowtime.hour < 17:
                ask1 = convert(lst[6])
                bid1 = convert(lst[23])
                askqty1 = str(lst[11])
                bidqty1 = str(lst[28])
            else:
                ask1 = convert(lst[29])
                bid1 = convert(lst[18])
                askqty1 = str(lst[30])
                bidqty1 = str(lst[19])
                totalaskqty = str(lst[28])
                totalbidqty = str(lst[17])[:-2]
            taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,bid1,ask1,bidqty1,askqty1)
            chk = 'Q'
            print lst[0], shcode, taqitem            
            
        elif lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'options':
            shcode = str(lst[4])                    
            ask1 = convert(lst[6])
            bid1 = convert(lst[23])
            askqty1 = str(lst[11])
            bidqty1 = str(lst[28])
            taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,bid1,ask1,bidqty1,askqty1)
            chk = 'Q'   
            print lst[0], shcode, taqitem  
            
        elif lst[1] == 'cybos' and lst[2] == 'E' and lst[3] == 'options':
            shcode = str(lst[4])
            expectprice = convert(lst[6])
            expectqty = 'E'
            taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,expectprice,expectqty)
            chk = 'E'
            print lst[0], shcode, taqitem  
            
        elif lst[1] == 'xing' and lst[2] == 'T' and lst[3] == 'options':
            shcode = str(lst[31])
            lastprice = convert(lst[8])
            lastqty = str(lst[13])            
            if lst[12] == '+':
                buysell = 'B'
            elif lst[12] == '-':
                buysell = 'S'
            else:
                buysell = ''
            taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,lastprice,lastqty,buysell)
            print lst[0], shcode, taqitem       
            #print msg                   
            chk = 'T'
            
        elif lst[1] == 'xing' and lst[2] == 'T' and lst[3] == 'futures':
            shcode = str(lst[32])
            lastprice = convert(lst[8])
            lastqty = str(lst[13])
            if lst[12] == '+':
                buysell = 'B'
            elif lst[12] == '-':
                buysell = 'S'
            else:
                buysell = ''
            taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,lastprice,lastqty,buysell)
            print lst[0], shcode, taqitem                        
            chk = 'T'
            
        if chk == 'Q':
            sqltext = """INSERT INTO FutOptTickData(ShortCD,FeedSource,TAQ,SecuritiesType,Time,Bid1,Ask1,BidQty1,AskQty1)
                                               VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?)"""
        elif chk == 'E':
            sqltext = """INSERT INTO FutOptTickData(ShortCD,FeedSource,TAQ,SecuritiesType,Time,LastPrice,BuySell)
                                               VALUES(?, ?, ?, ? ,?, ?, ?)"""
        elif chk == 'T':
            sqltext = """INSERT INTO FutOptTickData(ShortCD,FeedSource,TAQ,SecuritiesType,Time,LastPrice,LastQty,BuySell)
                                               VALUES(?, ?, ?, ? ,?, ?, ?, ?)"""

        if chk != '':
            self.cursor_memory.execute(sqltext,taqitem)
            self.cursor_buffer.execute(sqltext,taqitem)
            self.conn_memory.commit()
            self.conn_buffer.commit()

        
        pass

    def onXTimerUpdate(self):
        if os.path.isfile(self.strdbname):
            #self.cursor_memory.execute("""SELECT * From FutOptTickData""")
            df_buffer = pd.read_sql("""SELECT * From FutOptTickData""",self.conn_buffer)
            pd.io.sql.write_frame(df_buffer, "FutOptTickData", self.conn_file,'sqlite','append')
            self.cursor_buffer.execute("""DELECT FROM FutOptTickData""")
            self.conn_buffer.commit()
        else:
            # make new file db
            print "make new file db"
        pass

    def onClick(self):
        if not self.mythread.isRunning():                        
            self.mythread.start()
            self.XTimer.start(60000)
            self.button.setText('Stop')
        else:
            self.mythread.terminate()
            self.XTimer.stop()
            self.button.setText('Start')
        pass
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = OptionsDBTest()    
    wdg.show()    
    sys.exit(app.exec_())
        
        
