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


class OptionDBThread(OptionViewerThread):
    def __init__(self,parent=None):
        OptionViewerThread.__init__(self,parent)
        self.strdbname = ''
        self.initDB()
        self.Id_tag = -1
        self.time_chk = True

    def initDB(self):
        strtime = time.strftime('%Y%m%d',time.localtime())
        nowtime = time.localtime()
        if nowtime.tm_hour >= 6 and nowtime.tm_hour < 16:
            self.strdbname = "TAQ_%s.db" %(strtime)
        elif nowtime.tm_hour >= 16:
            self.strdbname = "TAQ_Night_%s.db" %(strtime)
        elif nowtime.tm_hour < 6:
            strtime = "%d%.2d%.2d" %(nowtime.tm_year,nowtime.tm_mon,nowtime.tm_mday-1)
            self.strdbname = "TAQ_Night_%s.db" %(strtime)

        self.initMemoryDB()
        if not os.path.isfile(self.strdbname):
            self.initFileDB()
        else:
            print 'loading from file DB to memory DB'
            self.conn_file = lite.connect(self.strdbname,check_same_thread=False)
            self.cursor_file = self.conn_file.cursor()
            df = pd.read_sql("""SELECT * From FutOptTickData""",self.conn_file)
            pd.io.sql.write_frame(df, "FutOptTickData", self.conn_memory,'sqlite','replace')
        pass

    def initMemoryDB(self):
        self.conn_memory = lite.connect(":memory:",check_same_thread=False)
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


    def initFileDB(self):
        self.conn_file = lite.connect(self.strdbname,check_same_thread=False)
        self.cursor_file = self.conn_file.cursor()
        self.cursor_file.execute("DROP TABLE IF EXISTS FutOptTickData")
        self.cursor_file.execute("""CREATE TABLE FutOptTickData(
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
        nightshift = 0
        if nowtime.hour >= 7 and nowtime.hour < 17:
            nightshift = 0
        else:
            nightshift = 1

        if lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'futures':
            shcode = str(lst[4]) + '000'
            if nightshift == 0:
                ask1 = convert(lst[6])
                ask2 = convert(lst[7])
                ask3 = convert(lst[8])
                ask4 = convert(lst[9])
                ask5 = convert(lst[10])
                bid1 = convert(lst[23])
                bid2 = convert(lst[24])
                bid3 = convert(lst[25])
                bid4 = convert(lst[26])
                bid5 = convert(lst[27])
                askqty1 = str(lst[11])
                askqty2 = str(lst[12])
                askqty3 = str(lst[13])
                askqty4 = str(lst[14])
                askqty5 = str(lst[15])
                totalaskqty = str(lst[16])
                askcnt1 = str(lst[17])
                askcnt2 = str(lst[18])
                askcnt3 = str(lst[19])
                askcnt4 = str(lst[20])
                askcnt5 = str(lst[21])
                totalaskcnt = str(lst[22])
                bidqty1 = str(lst[28])
                bidqty2 = str(lst[29])
                bidqty3 = str(lst[30])
                bidqty4 = str(lst[31])
                bidqty5 = str(lst[32])
                totalbidqty = str(lst[33])
                bidcnt1 = str(lst[34])
                bidcnt2 = str(lst[35])
                bidcnt3 = str(lst[36])
                bidcnt4 = str(lst[37])
                bidcnt5 = str(lst[38])
                totalbidcnt = str(lst[39])

            else:
                ask1 = convert(lst[29])
                bid1 = convert(lst[18])
                askqty1 = str(lst[30])
                bidqty1 = str(lst[19])

                ask2 = convert(lst[27])
                bid2 = convert(lst[20])
                askqty2 = str(lst[28])
                bidqty2 = str(lst[21])

                ask3 = convert(lst[29])
                bid3 = convert(lst[22])
                askqty3 = str(lst[30])
                bidqty3 = str(lst[23])

                ask4 = convert(lst[31])
                bid4 = convert(lst[24])
                askqty4 = str(lst[32])
                bidqty4 = str(lst[25])

                ask5 = convert(lst[33])
                bid5 = convert(lst[26])
                askqty5 = str(lst[34])
                bidqty5 = str(lst[27])


                totalaskqty = str(lst[28])
                totalbidqty = str(lst[17])[:-2]

                bidcnt1 = str(lst[40])
                bidcnt2 = str(lst[41])
                bidcnt3 = str(lst[42])
                bidcnt4 = str(lst[43])
                bidcnt5 = str(lst[44])
                totalbidcnt = str(lst[39])

                askcnt1 = str(lst[46])
                askcnt2 = str(lst[47])
                askcnt3 = str(lst[48])
                askcnt4 = str(lst[49])
                askcnt5 = str(lst[50])
                totalaskcnt = str(lst[45])

            taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,bid1,ask1,bidqty1,askqty1,bidcnt1,askcnt1,
                       bid2,ask2,bidqty2,askqty2,bidcnt2,askcnt2,
                       bid3,ask3,bidqty3,askqty3,bidcnt3,askcnt3,
                       bid4,ask4,bidqty4,askqty4,bidcnt4,askcnt4,
                       bid5,ask5,bidqty5,askqty5,bidcnt5,askcnt5,
                       totalbidqty,totalaskqty,totalbidcnt,totalaskcnt)

            chk = 'Q'
            print lst[0], shcode, taqitem

        elif lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'options':
            shcode = str(lst[4])
            ask1 = convert(lst[6])
            ask2 = convert(lst[7])
            ask3 = convert(lst[8])
            ask4 = convert(lst[9])
            ask5 = convert(lst[10])
            bid1 = convert(lst[23])
            bid2 = convert(lst[24])
            bid3 = convert(lst[25])
            bid4 = convert(lst[26])
            bid5 = convert(lst[27])
            askqty1 = str(lst[11])
            askqty2 = str(lst[12])
            askqty3 = str(lst[13])
            askqty4 = str(lst[14])
            askqty5 = str(lst[15])
            totalaskqty = str(lst[16])
            askcnt1 = str(lst[17])
            askcnt2 = str(lst[18])
            askcnt3 = str(lst[19])
            askcnt4 = str(lst[20])
            askcnt5 = str(lst[21])
            totalaskcnt = str(lst[22])
            bidqty1 = str(lst[28])
            bidqty2 = str(lst[29])
            bidqty3 = str(lst[30])
            bidqty4 = str(lst[31])
            bidqty5 = str(lst[32])
            totalbidqty = str(lst[33])
            bidcnt1 = str(lst[34])
            bidcnt2 = str(lst[35])
            bidcnt3 = str(lst[36])
            bidcnt4 = str(lst[37])
            bidcnt5 = str(lst[38])
            totalbidcnt = str(lst[39])
            taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,bid1,ask1,bidqty1,askqty1,bidcnt1,askcnt1,
                       bid2,ask2,bidqty2,askqty2,bidcnt2,askcnt2,
                       bid3,ask3,bidqty3,askqty3,bidcnt3,askcnt3,
                       bid4,ask4,bidqty4,askqty4,bidcnt4,askcnt4,
                       bid5,ask5,bidqty5,askqty5,bidcnt5,askcnt5,
                       totalbidqty,totalaskqty,totalbidcnt,totalaskcnt)
            chk = 'Q'
            #print lst[0], shcode, taqitem

        elif lst[1] == 'cybos' and lst[2] == 'E' and lst[3] == 'options':
            shcode = str(lst[4])
            expectprice = convert(lst[6])
            expectqty = ''
            taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,expectprice,expectqty)
            chk = 'E'
            print lst[0], shcode, taqitem

        elif lst[1] == 'xing' and lst[2] == 'T' and lst[3] == 'options':            
            shcode = str(lst[31 + nightshift])
            lastprice = convert(lst[8 + nightshift])
            lastqty = str(lst[13 + nightshift])
            if lst[12 + nightshift] == '+':
                buysell = 'B'
            elif lst[12 + nightshift] == '-':
                buysell = 'S'
            else:
                buysell = ''
            bid1 = convert(lst[21 + nightshift])
            ask1 = convert(lst[20 + nightshift])
            taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,bid1,ask1,lastprice,lastqty,buysell)
            print lst[0], shcode, taqitem
            #print msg
            chk = 'T'

        elif lst[1] == 'xing' and lst[2] == 'T' and lst[3] == 'futures':
            shcode = str(lst[31 + nightshift])
            lastprice = convert(lst[8 + nightshift])
            lastqty = str(lst[13 + nightshift])
            if lst[12 + nightshift] == '+':
                buysell = 'B'
            elif lst[12 + nightshift] == '-':
                buysell = 'S'
            else:
                buysell = ''
            bid1 = convert(lst[21 + nightshift])
            ask1 = convert(lst[20 + nightshift])
            taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,bid1,ask1,lastprice,lastqty,buysell)
            print lst[0], shcode, taqitem
            chk = 'T'

        elif lst[1] == 'xing' and lst[2] == 'Q' and lst[3] == 'options':
            if nightshift == 1:
                shcode = str(lst[22])

                ask1 = convert(lst[6])
                ask2 = convert(lst[10])
                ask3 = convert(lst[14])

                bid1 = convert(lst[7])
                bid2 = convert(lst[11])
                bid3 = convert(lst[15])

                askqty1 = str(lst[8])
                askqty2 = str(lst[12])
                askqty3 = str(lst[16])

                bidqty1 = str(lst[9])
                bidqty2 = str(lst[13])
                bidqty3 = str(lst[17])


                totalaskqty = str(lst[18])
                totalbidqty = str(lst[19])

                totalaskcnt = str(lst[20])
                totalbidcnt = str(lst[21])

                taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,bid1,ask1,bidqty1,askqty1,'','',
                           bid2,ask2,bidqty2,askqty2,'','',
                           bid3,ask3,bidqty3,askqty3,'','',
                           '','','','','','',
                           '','','','','','',
                           totalbidqty,totalaskqty,totalbidcnt,totalaskcnt)
                chk = 'Q'

                print lst[0], shcode, taqitem

        elif lst[1] == 'xing' and lst[2] == 'Q' and lst[3] == 'futures':
            if nightshift == 1:
                shcode = str(lst[40])

                ask1 = convert(lst[6])
                ask2 = convert(lst[12])
                ask3 = convert(lst[18])
                ask4 = convert(lst[24])
                ask5 = convert(lst[30])

                bid1 = convert(lst[7])
                bid2 = convert(lst[13])
                bid3 = convert(lst[19])
                bid4 = convert(lst[25])
                bid5 = convert(lst[31])

                askqty1 = str(lst[8])
                askqty2 = str(lst[14])
                askqty3 = str(lst[20])
                askqty4 = str(lst[26])
                askqty5 = str(lst[32])

                bidqty1 = str(lst[9])
                bidqty2 = str(lst[15])
                bidqty3 = str(lst[21])
                bidqty4 = str(lst[27])
                bidqty5 = str(lst[33])

                askcnt1 = str(lst[10])
                askcnt2 = str(lst[16])
                askcnt3 = str(lst[22])
                askcnt4 = str(lst[28])
                askcnt5 = str(lst[34])

                bidcnt1 = str(lst[11])
                bidcnt2 = str(lst[17])
                bidcnt3 = str(lst[23])
                bidcnt4 = str(lst[29])
                bidcnt5 = str(lst[35])

                totalaskqty = str(lst[36])
                totalbidqty = str(lst[37])

                totalaskcnt = str(lst[38])
                totalbidcnt = str(lst[39])
                taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,bid1,ask1,bidqty1,askqty1,bidcnt1,askcnt1,
                       bid2,ask2,bidqty2,askqty2,bidcnt2,askcnt2,
                       bid3,ask3,bidqty3,askqty3,bidcnt3,askcnt3,
                       bid4,ask4,bidqty4,askqty4,bidcnt4,askcnt4,
                       bid5,ask5,bidqty5,askqty5,bidcnt5,askcnt5,
                       totalbidqty,totalaskqty,totalbidcnt,totalaskcnt)

                chk = 'Q'
                print lst[0], shcode, taqitem

        if chk == 'Q':
            wildcard = ','.join('?'*39)
            sqltext = """INSERT INTO FutOptTickData(ShortCD,FeedSource,TAQ,SecuritiesType,Time,Bid1,Ask1,BidQty1,AskQty1,BidCnt1,AskCnt1,
                                                    Bid2,Ask2,BidQty2,AskQty2,BidCnt2,AskCnt2,
                                                    Bid3,Ask3,BidQty3,AskQty3,BidCnt3,AskCnt3,
                                                    Bid4,Ask4,BidQty4,AskQty4,BidCnt4,AskCnt4,
                                                    Bid5,Ask5,BidQty5,AskQty5,BidCnt5,AskCnt5,
                                                    TotalBidQty, TotalAskQty,TotalBidCnt, TotalAskCnt
                                                    )
                                               VALUES(%s)"""%wildcard
        elif chk == 'E':
            sqltext = """INSERT INTO FutOptTickData(ShortCD,FeedSource,TAQ,SecuritiesType,Time,LastPrice,BuySell)
                                               VALUES(?, ?, ?, ? ,?, ?, ?)"""
        elif chk == 'T':
            sqltext = """INSERT INTO FutOptTickData(ShortCD,FeedSource,TAQ,SecuritiesType,Time,Bid1,Ask1,LastPrice,LastQty,BuySell)
                                               VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?, ?)"""

        if chk != '':
            self.cursor_memory.execute(sqltext,taqitem)
            self.conn_memory.commit()


        if nowtime.second % 60 == 15 and self.time_chk:
            self.onXTimerUpdate()
            self.time_chk = False
        elif nowtime.second % 60 != 15:
            self.time_chk = True


        pass

    def onXTimerUpdate(self):
        if os.path.isfile(self.strdbname):
            print 'read memomry db...'
            try:

                df_memory = pd.read_sql("""SELECT * From FutOptTickData WHERE Id > %d """%self.Id_tag,self.conn_memory)
                self.Id_tag = df_memory['Id'].irow(-1)
            except lite.Error as e:
                print "An error occurred:", e.args[0]
                return
            print 'test: write file db...'
            #pdb.set_trace()
            df_memory = df_memory.iloc[:,1:len(df_memory.columns)]
            pd.io.sql.write_frame(df_memory, "FutOptTickData", self.conn_file,'sqlite','append')

        else:
            # make new file db
            print "make new file db"
        pass



class OptionsDBTest(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initThread()
        
    def initUI(self):
        self.button = QtGui.QPushButton('Start', self)
        self.button.clicked.connect(self.onClick)        
        self.vboxlayout = QtGui.QVBoxLayout(self)
        self.vboxlayout.addWidget(self.button)
        self.setWindowTitle('TAQ_DB')
        self.resize(260, 50)
        pass
    
    def initThread(self):
        self.mythread = OptionDBThread()
        #self.mythread.receiveData[str].connect(self.onReceiveData)
        pass


    def onClick(self):
        if not self.mythread.isRunning():                        
            self.mythread.start()
            self.button.setText('Stop')
        else:
            self.mythread.stop()
            if self.mythread.wait():
                self.mythread.onXTimerUpdate()
            self.button.setText('Start')
        pass
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = OptionsDBTest()    
    wdg.show()    
    sys.exit(app.exec_())
        
        
