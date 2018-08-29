# -*- coding: utf-8 -*-
"""
Created on Fri Jul 04 22:26:38 2014

@author: assa
"""

import sqlite3 as lite
from PyQt4 import QtCore
from datetime import datetime

class QtViewerSC3(QtCore.QObject):
    receive = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(QtViewerSC3,self).__init__(parent)
        self.dbname = None
        self.flag = True
        
    def Update(self, subject):
        #print '-' * 20                    
        if type(subject.data).__name__ == 'dict':     
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]                  
            
            orgordno = subject.data['orgordno']
            ordno = subject.data['ordno']
                                    
            #-------------------------------
                                    
            if self.dbname != None:
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()
                cursor_db.execute("""Select OrdNo, OrgOrdNo From OrderList 
                                    WHERE OrdNo = ? and ExecNo is null and BuySell = 'cancl' """,(str(ordno),))
                rows_cancl = cursor_db.fetchall()                
                
                cursor_db.execute("""Select UnExecQty From OrderList 
                                    WHERE OrdNo = ? and ExecNo is null """,(str(orgordno),))
                rows_unexecqty = cursor_db.fetchall()
                unexecqty = 0
                
                if len(rows_unexecqty) == 1: unexecqty = int(rows[0][0])
                if len(rows_cancl) == 0:            
                    buysell = 'cancl'
                    shcode = subject.data['Isuno']
                    canclqty = subject.data['canccnfqty']
                    
                    if subject.data['ordptncode'] == '00': type1 = 'limit'                
                    elif subject.data['ordptncode'] == '03': type1 = 'market'                
                    else: type1 = None
                                                           
                    chkreq = ''
                    orderitem = (ordno,orgordno,strnowtime,buysell,shcode,canclqty,chkreq)            
                    cursor_db.execute("""INSERT INTO OrderList(OrdNo,OrgOrdNo,Time,BuySell,ShortCD,Qty,ChkReq) 
                                                VALUES(?, ?, ?, ? ,?, ?, ?)""",orderitem)  
                    
                    if unexecqty > 0:
                        cursor_db.execute("""Update OrderList Set UnExecQty=? 
                                                        WHERE OrdNo=? and (BuySell = 'buy' or BuySell = 'sell') """, 
                                                        (str(unexecqty - int(canclqty)),orgordno))
                    conn_db.commit()
                    conn_db.close()
                    #self.emit(QtCore.SIGNAL("OnReceiveData (QString)"),'CSPAT00800')
                self.receive.emit()
            
        self.flag = False
        
        