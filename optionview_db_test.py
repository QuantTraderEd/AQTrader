# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 16:52:59 2014

@author: assa
"""

import os
import time
import sqlite3 as lite
from datetime import datetime
from PyQt4 import QtGui
from zerooptionviewer_thread import OptionViewerThread

def convert(strprice):
    return '%.2f' %round(float(strprice),2)


class OptionsDBTest(QtGui.QWidget):
    def __init__(self,parent = None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initDB()
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
        
    def initDB(self):
        strtime = time.strftime('%Y%m%d',time.localtime())
        self.strdbname = "OptionsTAQ_%s.db" %(strtime)
        if not os.path.isfile(self.strdbname):        
            self.conn_db = lite.connect(self.strdbname)
            self.cursor_db = self.conn_db.cursor()
            self.cursor_db.execute("DROP TABLE IF EXISTS TickData")
            self.cursor_db.execute("""CREATE TABLE TickData(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                                           ShortCD TEXT,
                                           FeedSource TEXT,
                                           TAQ TEXT,
                                           SecuritiesType TEXT,
                                           Time TEXT,                  
                                           BuySell TEXT,                                                                           
                                           LastPrice TEXT,
                                           LastQty TEXT,
                                           Bid1 TEXT,
                                           Ask1 TEXT,
                                           Bid2 TEXT,
                                           Ask2 TEXT,
                                           Bid3 TEXT,
                                           Ask3 TEXT,
                                           Bid4 TEXT,
                                           Ask4 TEXT,
                                           Bid5 TEXT,
                                           Ask5 TEXT,
                                           BidQty1 TEXT,
                                           AskQty1 TEXT,
                                           BidQty2 TEXT,
                                           AskQty2 TEXT,
                                           BidQty3 TEXT,
                                           AskQty3 TEXT,
                                           BidQty4 TEXT,
                                           AskQty4 TEXT,
                                           BidQty5 TEXT,
                                           AskQty5 TEXT,
                                           BidCnt1 TEXT,
                                           AskCnt1 TEXT,
                                           BidCnt2 TEXT,
                                           AskCnt2 TEXT,
                                           BidCnt3 TEXT,
                                           AskCnt3 TEXT,
                                           BidCnt4 TEXT,
                                           AskCnt4 TEXT,
                                           BidCnt5 TEXT,
                                           AskCnt5 TEXT,
                                           TotalBidQty TEXT,
                                           TotalAskQty TEXT,
                                           TotalBidCnt TEXT,
                                           TotalAskCnt TEXT
                                           )""")
            self.conn_db.close()
            
        self.conn_db = lite.connect(self.strdbname)
        self.cursor_db = self.conn_db.cursor()
        pass
    
    def onReceiveData(self,msg):
        nowtime = datetime.now()
        strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')
        lst = msg.split(',')
        chk = ''
        if lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'futures':
            shcode = str(lst[4]) + '000'
            if nowtime.hour >= 7 and nowtime.hour < 17:
                ask1 = convert(lst[18])
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
            taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,bid1,ask1,bidqty1,askqty1,totalbidqty,totalaskqty)
            chk = 'Q'
            print taqitem            
        elif lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'options':
            shcode = str(lst[4])                    
            if nowtime.hour >= 7 and nowtime.hour < 17:
                ask1 = convert(lst[6])
                bid1 = convert(lst[23])
                askqty1 = str(lst[11])
                bidqty1 = str(lst[28])
                totalaskqty = None
                totalbidqty = None
            taqitem = (shcode,str(lst[1]),str(lst[2]),str(lst[3]),strnowtime,bid1,ask1,bidqty1,askqty1,totalbidqty,totalaskqty)
            chk = 'Q'
            print taqitem
            
        if chk == 'Q':
            self.cursor_db.execute("""INSERT INTO TickData(ShortCD,FeedSource,TAQ,SecuritiesType,Time,Bid1,Ask1,BidQty1,AskQty1,TotalBidQty,TotalAskQty) 
                                                VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?)""",taqitem)
            self.conn_db.commit()
        elif chk == 'T':
            
            self.conn_db.commit()    
        
        pass
    
    def onClick(self):
        if not self.mythread.isRunning():                        
            self.mythread.start()
            self.button.setText('Running')
        pass
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = OptionsDBTest()    
    wdg.show()    
    sys.exit(app.exec_())
        
        
