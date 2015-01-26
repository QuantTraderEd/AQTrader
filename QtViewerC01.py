# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 22:10:53 2014

@author: assa
"""

import sqlite3 as lite
from PyQt4 import QtCore
from datetime import datetime

def convert(strprice):
    return '%.2f' %round(float(strprice),2)


class QtViewerC01(QtCore.QObject):
    receive = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(QtViewerC01,self).__init__(parent)
        self.dbname = None
        self.flag = True
        
    def Update(self, subject):
        #print '-' * 20                    
        if type(subject.data).__name__ == 'dict':
            print subject.data
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]   
            #print 'szMessage',  subject.data['szMessage']
            #print 'szMessageCode', subject.data['szMessageCode'],       
            
            ordno = unicode(int(subject.data['ordno']))
            execno = None
            #execno = subject.data['execno']
            
            if subject.data['dosugb'] == '2': buysell = 'buy'                
            elif subject.data['dosugb'] == '1': buysell = 'sell'
            else: buysell = None                
                
            shcode = subject.data['expcode'][3:11]
            ordprice = None
            ordqty = None
            execprice = subject.data['cheprice']
            execqty = subject.data['chevol']
            unexecqty = None
            orderitem = (ordno,execno,strnowtime,buysell,shcode,ordprice,ordqty,execprice,execqty,unexecqty)            
            print orderitem            
            if self.dbname != None:
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()
                cursor_db.execute("""INSERT INTO OrderList(OrgOrdNo,ExecNo,Time,BuySell,ShortCD,Price,Qty,ExecPrice,ExecQty,UnExecQty) 
                                                VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?, ?)""",orderitem) 
                                                
                cursor_db.execute("""Select ExecPrice,ExecQty,UnExecQty From OrderList 
                                    WHERE OrdNo = ? and ShortCD = ? and ChkReq is not null """,(str(ordno),str(shcode),))
                rows = cursor_db.fetchall()                
                unexecqty = 0
                avgExecPrice = 0
                avgExecQty = 0
                if len(rows) == 1:
                    if rows[0][0]:
                        avgExecPrice = float(rows[0][0])
                    if rows[0][1]:
                        avgExecQty = int(rows[0][1])
                    unexecqty = int(rows[0][2])
                    avgExecPrice = (avgExecPrice * avgExecQty + float(execprice) * int(execqty)) / (avgExecQty + int(execqty))
                    avgExecQty =  avgExecQty + int(execqty)    
                    avgExecPrice = convert(avgExecPrice)
                    
                
                if unexecqty > 0:
                    cursor_db.execute("""Update OrderList Set ExecPrice=?, ExecQty=?, UnExecQty=? 
                                                                    WHERE OrdNo=? and ShortCD = ? and (BuySell = 'buy' or BuySell = 'sell') 
                                                                    and ChkReq is not null
                                                                    """, 
                                                                    (str(avgExecPrice), str(avgExecQty),str(unexecqty - int(execqty)),str(ordno),str(shcode),))
                

                conn_db.commit()
                conn_db.close()
                self.receive.emit()
                
        self.flag = False      
