# -*- coding: utf-8 -*-

import sqlite3 as lite
from PyQt4 import QtCore
from datetime import datetime


class QtViewerCFOAT00300(QtCore.QObject):
    receive = QtCore.pyqtSignal()

    def __init__(self):
        super(QtViewerCFOAT00300,self).__init__()
        self.dbname = None
        self.flag = True
        
    def Update(self, subject):
        # print '-' * 20
        if type(subject.data).__name__ == 'dict':     
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]   
            # print 'szMessage',  subject.data['szMessage']
            # print 'szMessageCode', subject.data['szMessageCode']
            
            orgordno = subject.data['OrgOrdNo']
            ordno = subject.data['OrdNo']
            autotrader_id = subject.autotrader_id
                                    
            # -------------------------------
            
            buysell = 'cancl'
            shcode = subject.data['FnoIsuNo']
            # price = subject.data['OrdPrc']
            canclqty = subject.data['CancQty']
            type1 = None
            type2 = None
            if subject.data['FnoOrdPtnCode'] != '':
                if subject.data['FnoOrdPtnCode'][1] == '0': type1 = 'limit'                
                elif subject.data['FnoOrdPtnCode'][1] == '3': type1 = 'market'                
                                    
                if subject.data['FnoOrdPtnCode'][0] == '0': type2 = 'GFD'                
                elif subject.data['FnoOrdPtnCode'][0] == '1': type2 = 'IOC'                
                elif subject.data['FnoOrdPtnCode'][0] == '2': type2 = 'FOK'                
               
            chkreq = subject.data['szMessageCode']
            orderitem = (autotrader_id,ordno,orgordno,strnowtime,buysell,shcode,canclqty,chkreq)
            
            if self.dbname != None and subject.data['szMessageCode'] == '00156':
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()
                
                cursor_db.execute("""Select OrdNo, OrgOrdNo From OrderList 
                                    WHERE OrdNo = ? and ExecNo is null and BuySell = 'cancl' """,(str(ordno),))
                rows_cancl = cursor_db.fetchall() 
                
                
                cursor_db.execute("""Select UnExecQty From OrderList 
                                    WHERE OrdNo = ? and ExecNo is null """,(str(orgordno),))
                rows = cursor_db.fetchall()
                unexecqty = 0
                if len(rows) == 1:
                    unexecqty = int(rows[0][0])
                wildcard = '?,' * len(orderitem)
                wildcard = wildcard[:-1]
                cursor_db.execute("""INSERT INTO OrderList(AutoTraderID,OrdNo,OrgOrdNo,Time,BuySell,ShortCD,Qty,ChkReq)
                                                VALUES(%s)""" % wildcard, orderitem)
                if len(rows_cancl) == 0 and unexecqty > 0:
                    cursor_db.execute("""Update OrderList Set UnExecQty=? 
                                                    WHERE OrdNo=? and (BuySell = 'buy' or BuySell = 'sell') """, 
                                                    (str(unexecqty - int(canclqty)),orgordno))
                conn_db.commit()
                conn_db.close()
                #self.emit(QtCore.SIGNAL("OnReceiveData (QString)"),'CSPAT00800')
                self.receive.emit()
            elif self.dbname != None and subject.data['szMessageCode'] != '00156':
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()
                wildcard = '?,' * len(orderitem)
                wildcard = wildcard[:-1]
                cursor_db.execute("""INSERT INTO OrderList(AutoTraderID, OrdNo,ExecNo,Time,BuySell,ShortCD,ExecQty,ChkReq)
                                                VALUES(%s)""" % wildcard, orderitem)
            
        self.flag = False    
