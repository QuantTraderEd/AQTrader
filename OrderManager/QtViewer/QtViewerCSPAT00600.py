# -*- coding: utf-8 -*-
"""
Created on Fri Jul 04 22:07:40 2014

@author: assa
"""
import sqlite3 as lite
from PyQt4 import QtCore
from datetime import datetime

class QtViewerCSPAT00600(QtCore.QObject):
    receive = QtCore.pyqtSignal()
    def __init__(self):
        super(QtViewerCSPAT00600,self).__init__()
        self.dbname = None
        self.flag = True
        
    def Update(self, subject):
        #print '-' * 20                    
        if type(subject.data).__name__ == 'dict':     
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]   
            #print 'szMessage',  subject.data['szMessage']
            #print 'szMessageCode', subject.data['szMessageCode'],             
            
            ordno = subject.data['OrdNo']
            
            if subject.data['BnsTpCode'] == '2': buysell = 'buy'
            elif subject.data['BnsTpCode'] == '1': buysell = 'sell'                
            else: buysell = None
        
            shcode = subject.data['IsuNo']
            price = subject.data['OrdPrc']
            qty = subject.data['OrdQty']
            unexecqty = qty
            
            if subject.data['OrdprcPtnCode'] == '00': type1 = 'limit'                
            elif subject.data['OrdprcPtnCode'] == '03': type1 = 'market'                
            else: type1 = None
                                
            if subject.data['OrdCndiTpCode'] == '0': type2 = 'GFD'                
            elif subject.data['OrdCndiTpCode'] == '1': type2 = 'IOC'                
            elif subject.data['OrdCndiTpCode'] == '2': type2 = 'FOK'                
            else: type2 =None                
                            
            chkreq = subject.data['szMessageCode']
            
            orderitem = (ordno,strnowtime,buysell,shcode,price,qty,type1,type2,unexecqty,chkreq)
            #print orderitem          
            if self.dbname != None:
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()
                cursor_db.execute("""INSERT INTO OrderList(OrdNo,Time,BuySell,ShortCD,Price,Qty,Type1,Type2,UnExecQty,ChkReq) 
                                                VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?, ?)""",orderitem)            
                conn_db.commit()
                conn_db.close()                
                #self.emit(QtCore.SIGNAL("OnReceiveData (QString)"),'CSPAT00600')
                self.receive.emit()
                
                
            
        self.flag = False    

        