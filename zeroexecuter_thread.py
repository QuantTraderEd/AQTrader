# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 15:37:25 2013

@author: Administrator
"""

import sqlite3 as lite
import pyxing as px
import zmq
from PyQt4 import QtCore
from pythoncom import PumpWaitingMessages
from datetime import datetime

from QtViewerCSPAT00600 import QtViewerCSPAT00600
from QtViewerCSPAT00800 import QtViewerCSPAT00800
from QtViewerCFOAT00100 import QtViewerCFOAT00100
from QtViewerCFOAT00300 import QtViewerCFOAT00300
from QtViewerSC1 import QtViewerSC1

class ExecuterThread(QtCore.QThread):
    threadUpdateDB = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(ExecuterThread,self).__init__(parent)
        self.initThread()
        self.initViewer()
        self.initQuery()
        

        
        
    def initThread(self):
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()
        
        
    def initViewer(self):
        self.cviewer = ConsoleViewer()
        self.cviewer0 = ConsolViewerSC0()        
        self.qtviewer00600 = QtViewerCSPAT00600()
        self.qtviewer00800 = QtViewerCSPAT00800()
        self.qtviewer00100 = QtViewerCFOAT00100()
        self.qtviewer00300 = QtViewerCFOAT00300()
        self.qtviewerSC1 = QtViewerSC1()        
        
        nowtime = datetime.now()
        strtime = datetime.strftime(nowtime,'%Y%m%d')
        self.strdbname = "orderlist_%s.db" %(strtime)
        
        self.qtviewer00600.dbname = self.strdbname
        self.qtviewer00800.dbname = self.strdbname
        self.qtviewer00100.dbname = self.strdbname
        self.qtviewer00300.dbname = self.strdbname
        self.qtviewerSC1.dbname = self.strdbname
        
        self.qtviewer00600.receive.connect(self.UpdateDB)
        self.qtviewer00800.receive.connect(self.UpdateDB)
        self.qtviewer00100.receive.connect(self.UpdateDB)
        self.qtviewer00300.receive.connect(self.UpdateDB)
        self.qtviewerSC1.receive.connect(self.UpdateDB)
        
    def initQuery(self):
        self.xaquery_CFOAT00100 = px.XAQuery_CFOAT00100()
        self.xaquery_CFOAT00200 = px.XAQuery_CFOAT00200()
        self.xaquery_CFOAT00300 = px.XAQuery_CFOAT00300()
        self.xaquery_CSPAT00600 = px.XAQuery_CSPAT00600()          
        self.xaquery_CSPAT00800 = px.XAQuery_CSPAT00800()          
        self.xareal_SC0 = px.XAReal_SC0()
        self.xareal_SC1 = px.XAReal_SC1()
        self.xaquery_CSPAT00600.observer = self.qtviewer00600
        self.xaquery_CSPAT00800.observer = self.qtviewer00800
        self.xaquery_CFOAT00100.observer = self.qtviewer00100
        self.xaquery_CFOAT00300.observer = self.qtviewer00300
        self.xareal_SC0.observer = self.cviewer0
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
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime,"%Y-%m-%d %H:%M:%S.%f")
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
            
            if self._XASession.IsConnected() and (buysell == '2' or buysell == '1') and shcode[0] == 'A':     
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
            elif self._XASession.IsConnected() and buysell == 'c' and shcode == 'A':
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
                
            elif self._XASession.IsConnected() and (buysell == '2' or buysell == '1') and (shcode[:3] == '101' or shcode[:3] == '201' or shcode[:3] == '301'):
                pass
            elif self._XASession.IsConnected() and buysell == 'c' and (shcode[:3] == '101' or shcode[:3] == '201' or shcode[:3] == '301'):
                pass 
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
            nowtime = datetime.now()
            #print 'szMessage',  subject.data['szMessage']
            #print 'szMessageCode', subject.data['szMessageCode'],             
#            print 'ordno', subject.data['ordno'],
#            print 'shtcode', subject.data['shtcode'],
#            print 'bnstp', subject.data['bnstp'],
#            print 'ordprice', subject.data['ordprice'],
#            print 'ordqty', subject.data['ordqty'],
#            print 'etfhogagb', subject.data['etfhogagb'],
#            print 'hogagb', subject.data['hogagb'],
#            print 'OrdTime_home', datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]                        
        self.flag = False
            


            
