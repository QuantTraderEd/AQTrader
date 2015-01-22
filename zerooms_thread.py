# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 15:37:25 2013

@author: Administrator
"""

import pyxing as px
import zmq
from PyQt4 import QtCore
from pythoncom import PumpWaitingMessages
from datetime import datetime

from QtViewerCSPAT00600 import QtViewerCSPAT00600
from QtViewerCSPAT00800 import QtViewerCSPAT00800
from QtViewerCFOAT00100 import QtViewerCFOAT00100
from QtViewerCFOAT00300 import QtViewerCFOAT00300
from QtViewerCEXAT11100 import QtViewerCEXAT11100
from QtViewerCEXAT11300 import QtViewerCEXAT11300
from QtViewerSC1 import QtViewerSC1
from QtViewerC01 import QtViewerC01

class ExecuterThread(QtCore.QThread):
    threadUpdateDB = QtCore.pyqtSignal()
    
    def __init__(self,parent=None):
        super(ExecuterThread,self).__init__(parent)
        self.initVar()
        self.initThread()
        self.initViewer()
        self.initQuery()

    def initVar(self):
        self._accountlist = []
        self._servername = ''
        
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
        self.qtviewer11100 = QtViewerCEXAT11100()
        self.qtviewer11300 = QtViewerCEXAT11300()
        self.qtviewerSC1 = QtViewerSC1()       
        self.qtviewerC01 = QtViewerC01()
        
        nowtime = datetime.now()
        strtime = datetime.strftime(nowtime,'%Y%m%d')                        
        if nowtime.hour >= 6 and nowtime.hour < 16:
            self.strdbname = "orderlist_%s.db" %(strtime)
        elif nowtime.hour >= 16:
            self.strdbname = "orderlist_night_%s.db" %(strtime)
        else:
            strtime = "%d%.2d%.2d" %(nowtime.year,nowtime.month,nowtime.day-1)
            self.strdbname = "orderlist_night_%s.db" %(strtime)
        
        self.qtviewer00600.dbname = self.strdbname
        self.qtviewer00800.dbname = self.strdbname
        self.qtviewer00100.dbname = self.strdbname
        self.qtviewer00300.dbname = self.strdbname
        self.qtviewer11100.dbname = self.strdbname
        self.qtviewer11300.dbname = self.strdbname
        self.qtviewerSC1.dbname = self.strdbname
        self.qtviewerC01.dbname = self.strdbname
        
        self.qtviewer00600.receive.connect(self.UpdateDB)
        self.qtviewer00800.receive.connect(self.UpdateDB)
        self.qtviewer00100.receive.connect(self.UpdateDB)
        self.qtviewer00300.receive.connect(self.UpdateDB)
        self.qtviewer11100.receive.connect(self.UpdateDB)
        self.qtviewer11300.receive.connect(self.UpdateDB)
        self.qtviewerSC1.receive.connect(self.UpdateDB)
        self.qtviewerC01.receive.connect(self.UpdateDB)
        
    def initQuery(self):
        self.xaquery_CFOAT00100 = px.XAQuery_CFOAT00100()
        self.xaquery_CFOAT00200 = px.XAQuery_CFOAT00200()
        self.xaquery_CFOAT00300 = px.XAQuery_CFOAT00300()
        self.xaquery_CSPAT00600 = px.XAQuery_CSPAT00600()          
        self.xaquery_CSPAT00800 = px.XAQuery_CSPAT00800()
        self.xaquery_CEXAT11100 = px.XAQuery_CEXAT11100()
        self.xaquery_CEXAT11300 = px.XAQuery_CEXAT11300()
        self.xareal_SC0 = px.XAReal_SC0()
        self.xareal_SC1 = px.XAReal_SC1()
        self.xareal_C01 = px.XAReal_C01()
        self.xaquery_CSPAT00600.observer = self.qtviewer00600
        self.xaquery_CSPAT00800.observer = self.qtviewer00800
        self.xaquery_CFOAT00100.observer = self.qtviewer00100
        self.xaquery_CFOAT00300.observer = self.qtviewer00300
        self.xaquery_CEXAT11100.observer = self.qtviewer11100
        self.xaquery_CEXAT11300.observer = self.qtviewer11300
        self.xareal_SC0.observer = self.cviewer0
        self.xareal_SC1.observer = self.qtviewerSC1
        self.xareal_C01.observer = self.qtviewerC01

    
    def run(self):
        if len(self._accountlist) == 0 :
            print 'fail: no account'
            return

        if self._servername[:3] == 'MIS':
            accountpwd = ['0000','0000']
        elif self._servername[:1] == 'X':
            accountpwd = ['0302','']
        else:
            print 'fail: not available servername'
            accountpwd = []
            return

        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:6000")
        self.xareal_SC0.AdviseRealData()
        self.xareal_SC1.AdviseRealData()        
        self.xareal_C01.AdviseRealData()
        #self.conn_db = lite.connect('orderlist.db')
        #self.cursor_db = self.conn_db.cursor()
            
        while True:
            msg = self.socket.recv()
            if not self._XASession.IsConnected():
                self.socket.send('fail: disconnect xsession')
                continue
            
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
            
            if (buysell == '2' or buysell == '1') and shcode[0] == 'A':     
                # equity new order                       
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','AcntNo',0,self._accountlist[1])    
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','InptPwd',0,accountpwd[1])
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
                    if szMsgCode != '00039' and szMsgCode != '00040':
                        self.socket.send('errCode: ' + str(szMsgCode))
                    else:
                        self.socket.send('msgCode: ' + str(szMsgCode))                
                    
            elif buysell == 'c' and shcode[0] == 'A':
                # equity cancel order                                   
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','OrgOrdNo',0,int(ordno))    
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','AcntNo',0,self._accountlist[1])    
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','InptPwd',0,accountpwd[1])
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
                
            elif (buysell == '2' or buysell == '1') and (shcode[:3] == '101' or shcode[:3] == '201' or shcode[:3] == '301'):
                if nowtime.hour >= 6 and nowtime.hour < 16:
                    # KRX Futures, Options new order
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','AcntNo',0,self._accountlist[0])
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','Pwd',0,accountpwd[0])
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','FnoIsuNo',0,str(shcode))
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','BnsTpCode',0,buysell)
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','FnoOrdprcPtnCode',0,'00')
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','OrdPrc',0,str(price))
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','OrdQty',0,int(qty))
                    ret = self.xaquery_CFOAT00100.Request(False)
                    print ret
                    if not ret:
                        while self.xaquery_CFOAT00100.observer.flag:
                            PumpWaitingMessages()
                        self.xaquery_CFOAT00100.observer.flag = True
                        szMsgCode = self.xaquery_CFOAT00100.data['szMessageCode']
                        print szMsgCode
                        if szMsgCode != '00039' and szMsgCode != '00040':
                            self.socket.send('errCode: ' + str(szMsgCode))
                        else:
                            self.socket.send('msgCode: ' + str(szMsgCode))
                else:
                    if shcode[:3] == '101':
                        self.socket.send('not yet implement...')
                        return
                    else:
                        # Eurex Futures, Options new order
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','AcntNo',0,self._accountlist[0])
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','Pwd',0,accountpwd[0])
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','FnoIsuNo',0,str(shcode))
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','BnsTpCode',0,buysell)
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','ErxPrcCndiTpCode',0,'2')
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','OrdPrc',0,str(price))
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','OrdQty',0,int(qty))
                        self.xaquery_CEXAT11100.shortcd = shcode
                        ret = self.xaquery_CEXAT11100.Request(False)
                        print ret
                        if not ret:
                            while self.xaquery_CEXAT11100.observer.flag:
                                PumpWaitingMessages()
                            self.xaquery_CEXAT11100.observer.flag = True
                            self.shortcd = ''
                            szMsgCode = self.xaquery_CEXAT11100.data['szMessageCode']
                            print szMsgCode
                            if szMsgCode != '00039' and szMsgCode != '00040':
                                self.socket.send('errCode: ' + str(szMsgCode))
                            else:
                                self.socket.send('msgCode: ' + str(szMsgCode))

            elif buysell == 'c' and (shcode[:3] == '101' or shcode[:3] == '201' or shcode[:3] == '301'):
                if nowtime.hour >= 6 and nowtime.hour < 16:
                    # KRX Futures, Options new order
                    self.xaquery_CFOAT00300.SetFieldData('CFOAT00300InBlock1','AcntNo',0,self._accountlist[0])
                    self.xaquery_CFOAT00300.SetFieldData('CFOAT00300InBlock1','Pwd',0,accountpwd[0])
                    self.xaquery_CFOAT00300.SetFieldData('CFOAT00300InBlock1','FnoIsuNo',0,shcode)
                    self.xaquery_CFOAT00300.SetFieldData('CFOAT00300InBlock1','OrgOrdNo',0,int(ordno))
                    self.xaquery_CFOAT00300.SetFieldData('CFOAT00300InBlock1','CancQty',0,int(qty))
                    ret = self.xaquery_CFOAT00300.Request(False)
                    self.socket.send('msgCode: ')
                    print ret
                else:
                    if shcode[:3] == '101':
                        self.socket.send('not yet implement...')
                        return
                    else:
                        # Eurex Futures, Options new order
                        self.xaquery_CEXAT11300.SetFieldData('CEXAT11300InBlock1','OrgOrdNo',0,int(ordno))
                        self.xaquery_CEXAT11300.SetFieldData('CEXAT11300InBlock1','AcntNo',0,self._accountlist[0])
                        self.xaquery_CEXAT11300.SetFieldData('CEXAT11300InBlock1','Pwd',0,accountpwd[0])
                        self.xaquery_CEXAT11300.SetFieldData('CEXAT11300InBlock1','FnoIsuNo',0,str(shcode))
                        ret = self.xaquery_CEXAT11300.Request(False)
                        self.socket.send('msgCode: ')
                        print ret
            else:
                self.socket.send('fail: other case order')
    

            
    def UpdateDB(self):
        print "receive update "
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
            


            
