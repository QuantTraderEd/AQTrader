# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 15:37:25 2013

@author: Administrator
"""


import datetime
import sqlite3 as lite
import pyxing as px
import zmq
from PyQt4 import QtCore
from pythoncom import PumpWaitingMessages


class ExecuterThread(QtCore.QThread):
    threadUpdateDB = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(ExecuterThread,self).__init__(parent)
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()
        
        cviewer = ConsoleViewer()
        cviewer0 = ConsolViewerSC0()        
        
        self.qtviewer00600 = QtViewerCSPAT00600()
        self.qtviewer00800 = QtViewerCSPAT00800()
        self.qtviewerSC1 = QtViewerSC1()        
        
        nowtime = datetime.datetime.now()
        strtime = datetime.datetime.strftime(nowtime,'%Y%m%d')
        self.strdbname = "orderlist_%s.db" %(strtime)
        
        self.qtviewer00600.dbname = self.strdbname
        self.qtviewer00800.dbname = self.strdbname
        self.qtviewerSC1.dbname = self.strdbname
        
        #self.connect(self.qtviewer,QtCore.SIGNAL("OnReceiveData (QString)"),self.UpdateDB)
        #self.connect(self.qtviewer1,QtCore.SIGNAL("OnReceiveData (QString)"),self.UpdateDB)
        self.qtviewer00600.receive.connect(self.UpdateDB)
        self.qtviewer00800.receive.connect(self.UpdateDB)
        self.qtviewerSC1.receive.connect(self.UpdateDB)

        
        self.xaquery_CSPAT00600 = px.XAQuery_CSPAT00600()          
        self.xaquery_CSPAT00800 = px.XAQuery_CSPAT00800()          
        self.xareal_SC0 = px.XAReal_SC0()
        self.xareal_SC1 = px.XAReal_SC1()
        self.xaquery_CSPAT00600.observer = self.qtviewer00600
        self.xaquery_CSPAT00800.observer = self.qtviewer00800
        self.xareal_SC0.observer = cviewer0
        self.xareal_SC1.observer = self.qtviewerSC1
                
    
    def run(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:6000")
        self.xareal_SC0.AdviseRealData()
        self.xareal_SC1.AdviseRealData()        
        
        #self.conn_db = lite.connect('orderlist.db')
        #self.cursor_db = self.conn_db.cursor()
            
        while True:
            msg = self.socket.recv()
            nowtime = datetime.datetime.now()
            strnowtime = datetime.datetime.strftime(nowtime,"%Y-%m-%d %H:%M:%S.%f")
            strnowtime = strnowtime[:-3]                        
            print "Got ",strnowtime ,msg
            lst = msg.split(',')
            buysell = ''
            shcode = lst[1]
            price = lst[2]
            qty = lst[3]
            ordno = ''
            
            
            if lst[0] == 'True':
                buysell = '2'
            elif lst[0] == 'False':
                buysell = '1'
            elif lst[0] == 'cancl':
                buysell = 'c'
                ordno = lst[4]            
                
                
            print buysell,shcode,price,qty,ordno
            
            if self._XASession.IsConnected() and (buysell == '2' or buysell == '1'):     
                # equity new order                       
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','AcntNo',0,self._accountlist[1])    
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','InptPwd',0,'0000')    
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','IsuNo',0,str(shcode)) #demo
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','OrdQty',0,int(qty))
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','OrdPrc',0,str(price))
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','BnsTpCode',0,buysell)
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','OrdprcPtnCode',0,'00')        
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','MgntrnCode',0,'000')
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','LoanDt',0,' ')        
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','OrdCndiTpCode',0,'0')        
                ret = self.xaquery_CSPAT00600.Request(False)      
                if ret == None:
                    while self.xaquery_CSPAT00600.observer.flag:
                        PumpWaitingMessages()
                    self.xaquery_CSPAT00600.observer.flag = True
                    szMsgCode = self.xaquery_CSPAT00600.data['szMessageCode']
                    #print szMsgCode
                    if szMsgCode != '00039' and szMsgCode != '00040':
                        self.socket.send('fail: order')
                        continue
                    
#                    while self.xareal_SC0.observer.flag:
#                        PumpWaitingMessages()
#                    self.xareal_SC0.observer.flag = True
                                        
                    self.socket.send('done ' + msg)
            elif self._XASession.IsConnected() and buysell == 'c':
                # equity cancel order                                   
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','OrgOrdNo',0,int(ordno))    
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','AcntNo',0,self._accountlist[1])    
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','InptPwd',0,'0000')    
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','IsuNo',0,str(shcode)) #demo
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','OrdQty',0,int(qty))                                                
                ret = self.xaquery_CSPAT00800.Request(False)    
                print ret
#                if ret == None:
#                    while self.xaquery_CSPAT00800.observer.flag:
#                        PumpWaitingMessages()
#                    self.xaquery_CSPAT00800.observer.flag = True
#                    szMsgCode = self.xaquery_CSPAT00800.data['szMessageCode']
#                    print szMsgCode
#                    if szMsgCode != '00039' and szMsgCode != '00040':
#                        self.socket.send('fail: order')
#                        continue
                self.socket.send('done ' + msg)
                                                                                   
            else:
                self.socket.send('fail: disconnect xsession')
    

            
    def UpdateDB(self):
        print "receive update "
        #self.emit(QtCore.SIGNAL("OnUpdateDB (QString)"),'1')
        self.threadUpdateDB.emit()
        pass





            
class ConsoleViewer:
    def __init__(self):
        self.flag = True
    def Update(self, subject):
        print '-' * 20
        print subject.__class__
        for item in subject.data:            
            if type(subject.data).__name__ == 'dict' : print item,subject.data[item]
            else: print item
        self.flag = False
        pass
    


class ConsolViewerSC0:
    def __init__(self):
        self.flag = True
    def Update(self, subject):
        print '-' * 20                    
        if type(subject.data).__name__ == 'dict':     
            nowtime = datetime.datetime.now()
            #print 'szMessage',  subject.data['szMessage']
            #print 'szMessageCode', subject.data['szMessageCode'],             
#            print 'ordno', subject.data['ordno'],
#            print 'shtcode', subject.data['shtcode'],
#            print 'bnstp', subject.data['bnstp'],
#            print 'ordprice', subject.data['ordprice'],
#            print 'ordqty', subject.data['ordqty'],
#            print 'etfhogagb', subject.data['etfhogagb'],
#            print 'hogagb', subject.data['hogagb'],
#            print 'OrdTime_home', datetime.datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]                        
        self.flag = False
            


            
class QtViewerCSPAT00600(QtCore.QObject):
    receive = QtCore.pyqtSignal()
    def __init__(self):
        super(QtViewerCSPAT00600,self).__init__()
        self.dbname = None
        self.flag = True
        
    def Update(self, subject):
        #print '-' * 20                    
        if type(subject.data).__name__ == 'dict':     
            nowtime = datetime.datetime.now()
            strnowtime = datetime.datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]   
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
        
        
class QtViewerCSPAT00800(QtCore.QObject):
    receive = QtCore.pyqtSignal()
    def __init__(self):
        super(QtViewerCSPAT00800,self).__init__()
        self.dbname = None
        self.flag = True
        
    def Update(self, subject):
        #print '-' * 20                    
        if type(subject.data).__name__ == 'dict':     
            nowtime = datetime.datetime.now()
            strnowtime = datetime.datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]   
            print 'szMessage',  subject.data['szMessage']            
            print 'szMessageCode', subject.data['szMessageCode']             
            
            orgordno = subject.data['OrgOrdNo']
            ordno = subject.data['OrdNo']
                                    
            #-------------------------------
            
            buysell = 'cancl'
            shcode = subject.data['IsuNo']
            #price = subject.data['OrdPrc']
            canclqty = subject.data['OrdQty']
            
            if subject.data['OrdPtnCode'] == '00': type1 = 'limit'                
            elif subject.data['OrdPtnCode'] == '03': type1 = 'market'                
            else: type1 = None
               
            chkreq = subject.data['szMessageCode']
            orderitem = (ordno,orgordno,strnowtime,buysell,shcode,canclqty,chkreq)
            
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
                cursor_db.execute("""INSERT INTO OrderList(OrdNo,OrgOrdNo,Time,BuySell,ShortCD,Qty,ChkReq) 
                                                VALUES(?, ?, ?, ? ,?, ?, ?)""",orderitem)  
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
                cursor_db.execute("""INSERT INTO OrderList(OrdNo,ExecNo,Time,BuySell,ShortCD,ExecQty,ChkReq) 
                                                VALUES(?, ?, ?, ? ,?, ?, ?)""",orderitem) 
            
        self.flag = False    

        
        
class QtViewerSC1(QtCore.QObject):
    receive = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(QtViewerSC1,self).__init__(parent)
        self.dbname = None
        self.flag = True
        
    def Update(self, subject):
        #print '-' * 20                    
        if type(subject.data).__name__ == 'dict':     
            nowtime = datetime.datetime.now()
            strnowtime = datetime.datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]   
            #print 'szMessage',  subject.data['szMessage']
            #print 'szMessageCode', subject.data['szMessageCode'],                 
            
            ordno = subject.data['ordno']
            execno = subject.data['execno']
            
            if subject.data['bnstp'] == '2': buysell = 'buy'                
            elif subject.data['bnstp'] == '1': buysell = 'sell'
            else: buysell = None                
                
            shcode = subject.data['shtnIsuno']
            ordprice = subject.data['ordprc']
            ordqty = subject.data['ordqty']
            execprice = subject.data['execprc']
            execqty = subject.data['execqty']
            unexecqty = subject.data['unercqty']            
            orderitem = (ordno,execno,strnowtime,buysell,shcode,ordprice,ordqty,execprice,execqty,unexecqty)            
            #print orderitem
            if self.dbname != None:
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()
                cursor_db.execute("""INSERT INTO OrderList(OrdNo,ExecNo,Time,BuySell,ShortCD,Price,Qty,ExecPrice,ExecQty,UnExecQty) 
                                                VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?, ?)""",orderitem)  
                cursor_db.execute("""Update OrderList Set UnExecQty=? 
                                                WHERE OrdNo=? and (BuySell = 'buy' or BuySell = 'sell') """, (unexecqty,ordno))
                conn_db.commit()
                conn_db.close()
                #self.emit(QtCore.SIGNAL("OnReceiveData (QString)"),'SC1')
                self.receive.emit()
                
        self.flag = False      
        
class QtViewerSC0(QtCore.QObject):
    receive = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(QtViewerSC0,self).__init__(parent)
        self.dbname = None
        self.flag = True
        
    def Update(self, subject):
        #print '-' * 20                    
        if type(subject.data).__name__ == 'dict':     
            nowtime = datetime.datetime.now()
            strnowtime = datetime.datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]
            ordno = subject.data['ordno']                    
        self.flag = False
        
class QtViewerSC3(QtCore.QObject):
    receive = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(QtViewerSC3,self).__init__(parent)
        self.dbname = None
        self.flag = True
        
    def Update(self, subject):
        #print '-' * 20                    
        if type(subject.data).__name__ == 'dict':     
            nowtime = datetime.datetime.now()
            strnowtime = datetime.datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]                  
            
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
        
        