# -*- coding: utf-8 -*-
"""
Created on Fri Jul 04 23:28:45 2014

@author: assa
"""

import sqlite3 as lite
from PyQt4 import QtCore
from datetime import datetime


class QtViewerCFOAT00100(QtCore.QObject):
    receive = QtCore.pyqtSignal()

    def __init__(self):
        super(QtViewerCFOAT00100, self).__init__()
        self.dbname = None
        self.flag = True
        
    def Update(self, subject):
        # print '-' * 20
        if type(subject.data).__name__ == 'dict':     
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]   
            # print 'szMessage',  subject.data['szMessage']
            # print 'szMessageCode', subject.data['szMessageCode'],

            autotrader_id = subject.autotrader_id
            ordno = subject.data['OrdNo']
            
            if subject.data['BnsTpCode'] == '2': buysell = 'buy'
            elif subject.data['BnsTpCode'] == '1': buysell = 'sell'                
            else: buysell = None
        
            shcode = subject.data['FnoIsuNo']
            price = subject.data['OrdPrc']
            qty = subject.data['OrdQty']
            unexecqty = qty
            type1 = None
            type2 = None
            if subject.data['FnoOrdPtnCode'] != '':
                if subject.data['FnoOrdPtnCode'][1] == '0': type1 = 'limit'                
                elif subject.data['FnoOrdPtnCode'][1] == '3': type1 = 'market'                
                                    
                if subject.data['FnoOrdPtnCode'][0] == '0': type2 = 'GFD'                
                elif subject.data['FnoOrdPtnCode'][0] == '1': type2 = 'IOC'                
                elif subject.data['FnoOrdPtnCode'][0] == '2': type2 = 'FOK'                
                            
            chkreq = subject.data['szMessageCode']
            
            orderitem = (autotrader_id, ordno, strnowtime, buysell, shcode, price, qty, type1, type2, unexecqty, chkreq)
            wildcard = "?, " * len(orderitem)
            wildcard = wildcard[:-1]
            # print orderitem
            if self.dbname != None:
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()
                cursor_db.execute("""INSERT INTO OrderList
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
                conn_db.commit()
                conn_db.close()                
                # self.emit(QtCore.SIGNAL("OnReceiveData (QString)"),'CSPAT00600')
                self.receive.emit()

        self.flag = False    
