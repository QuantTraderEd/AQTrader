# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 22:10:53 2014

@author: assa
"""

import sqlite3 as lite
from PyQt4 import QtCore
from datetime import datetime


class QtViewerC01(QtCore.QObject):
    receive = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(QtViewerC01,self).__init__(parent)
        self.dbname = None
        self.flag = True
        
    def Update(self, subject):
        #print '-' * 20                    
        if type(subject.data).__name__ == 'dict':     
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]   
            #print 'szMessage',  subject.data['szMessage']
            #print 'szMessageCode', subject.data['szMessageCode'],       
            
            ordno = subject.data['ordno']
            execno = None
            #execno = subject.data['execno']
            
            if subject.data['dosugb'] == '2': buysell = 'buy'                
            elif subject.data['dosugb'] == '1': buysell = 'sell'
            else: buysell = None                
                
            shcode = subject.data['expcode']
            ordprice = None
            ordqty = None
            execprice = subject.data['cheprice']
            execqty = subject.data['chevol']
            unexecqty = None
            orderitem = (ordno,execno,strnowtime,buysell,shcode,ordprice,ordqty,execprice,execqty,unexecqty)            
            print orderitem
#            if self.dbname != None:
#                conn_db = lite.connect(self.dbname)
#                cursor_db = conn_db.cursor()
#                cursor_db.execute("""INSERT INTO OrderList(OrdNo,ExecNo,Time,BuySell,ShortCD,Price,Qty,ExecPrice,ExecQty,UnExecQty) 
#                                                VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?, ?)""",orderitem)  
#                cursor_db.execute("""Update OrderList Set UnExecQty=? 
#                                                WHERE OrdNo=? and (BuySell = 'buy' or BuySell = 'sell') """, (unexecqty,ordno))
#                conn_db.commit()
#                conn_db.close()
#                #self.emit(QtCore.SIGNAL("OnReceiveData (QString)"),'SC1')
#                self.receive.emit()
                
        self.flag = False      
