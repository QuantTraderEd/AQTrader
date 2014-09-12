# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 16:52:59 2014

@author: assa
"""

import time
import sqlite3 as lite


class OptionsDBTest:
    def __init__(self):    
        self.initDB()
        
    def initDB(self):
        strtime = time.strftime('%Y%m%d',time.localtime())
        strdbname = "OptionsTAQ_%s.db" %(strtime)
        if not os.path.isfile(strdbname):        
            self.conn_db = lite.connect(strdbname)
            self.cursor_db = self.conn_db.cursor()
            self.cursor_db.execute("DROP TABLE IF EXISTS OrderList")
            self.cursor_db.execute("""CREATE TABLE TickData(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                                           ShortCD TEXT,
                                           FeedSource TEXT,
                                           TAQ TEXT,
                                           SecuritiesType TEXT,
                                           Time TEXT,                  
                                           BuySell TEXT,                                                                           
                                           LastPrice TEXT,
                                           Qty TEXT,
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
        pass
