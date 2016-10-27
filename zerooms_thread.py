# -*- coding: utf-8 -*-

import pyxing as px
import zmq
import logging
import redis
from PyQt4 import QtCore
from pythoncom import PumpWaitingMessages
from datetime import datetime

from QtViewer.QtViewerCSPAT00600 import QtViewerCSPAT00600
from QtViewer.QtViewerCSPAT00800 import QtViewerCSPAT00800
from QtViewer.QtViewerCFOAT00100 import QtViewerCFOAT00100
from QtViewer.QtViewerCFOAT00300 import QtViewerCFOAT00300
from QtViewer.QtViewerCEXAT11100 import QtViewerCEXAT11100
from QtViewer.QtViewerCEXAT11300 import QtViewerCEXAT11300
from QtViewer.QtViewerSC1 import QtViewerSC1
from QtViewer.QtViewerC01 import QtViewerC01
from QtViewer.QtViewerEU1 import QtViewerEU1


class OrderMachineThread(QtCore.QThread):
    threadUpdateDB = QtCore.pyqtSignal()
    
    def __init__(self, order_port=6001, exec_report_port=7001, parent=None):
        super(OrderMachineThread, self).__init__(parent)
        self.initVar()
        self.order_port = order_port
        self.exec_report_port = exec_report_port
        self.init_zmq()
        self.initThread()
        self.initViewer()
        self.initQuery()
        self.redis_client = redis.Redis()
        self.logger = logging.getLogger('ZeroOMS.Thread')
        self.logger.info('Init Thread')

    def initVar(self):
        self._accountlist = []
        self._servername = ''
        self.fo_account_index = 0
        self.eq_account_index = 1
        self.ordno_dict = {}
        self.db_path = 'C:/Python/ZeroTrader_Test/ZeroOMS/orderlist_db/'
        
    def initThread(self):
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()

    def init_zmq(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:%d" % self.order_port)
        # self.socket = context.socket(zmq.DEALER)
        # self.socket.connect("tcp://127.0.0.1:6001")

        self.socket_execution_report = context.socket(zmq.PUB)
        self.socket_execution_report.bind("tcp://127.0.0.1:%d" % self.exec_report_port)

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
        self.qtviewerC01 = QtViewerC01(self.socket_execution_report)
        self.qtviewerEU1 = QtViewerEU1(self.socket_execution_report)
        # self.qtviewerC01.ordno_dict = proxy(self.ordno_dict)
        # self.qtviewerEU1.ordno_dict = proxy(self.ordno_dict)
        
        nowtime = datetime.now()
        strtime = datetime.strftime(nowtime,'%Y%m%d')                        
        if nowtime.hour >= 6 and nowtime.hour < 16:
            self.strdbname = "orderlist_%s.db" %(strtime)
        elif nowtime.hour >= 16:
            self.strdbname = "orderlist_night_%s.db" %(strtime)
        else:
            strtime = "%d%.2d%.2d" %(nowtime.year,nowtime.month,nowtime.day-1)
            self.strdbname = "orderlist_night_%s.db" %(strtime)

        self.strdbname = self.db_path + self.strdbname
        
        self.qtviewer00600.dbname = self.strdbname
        self.qtviewer00800.dbname = self.strdbname
        self.qtviewer00100.dbname = self.strdbname
        self.qtviewer00300.dbname = self.strdbname
        self.qtviewer11100.dbname = self.strdbname
        self.qtviewer11300.dbname = self.strdbname
        self.qtviewerSC1.dbname = self.strdbname
        self.qtviewerC01.dbname = self.strdbname
        self.qtviewerEU1.dbname = self.strdbname

        self.qtviewer00100.initDB()
        self.qtviewer00300.initDB()
        self.qtviewer11100.initDB()
        self.qtviewer11300.initDB()
        
        self.qtviewer00600.receive.connect(self.UpdateDB)
        self.qtviewer00800.receive.connect(self.UpdateDB)
        self.qtviewer00100.receive.connect(self.UpdateDB)
        self.qtviewer00300.receive.connect(self.UpdateDB)
        self.qtviewer11100.receive.connect(self.UpdateDB)
        self.qtviewer11300.receive.connect(self.UpdateDB)
        self.qtviewerSC1.receive.connect(self.UpdateDB)
        self.qtviewerC01.receive.connect(self.UpdateDB)
        self.qtviewerEU1.receive.connect(self.UpdateDB)
        
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
        self.xareal_EU1 = px.XAReal_EU1()
        self.xaquery_CSPAT00600.observer = self.qtviewer00600
        self.xaquery_CSPAT00800.observer = self.qtviewer00800
        self.xaquery_CFOAT00100.observer = self.qtviewer00100
        self.xaquery_CFOAT00300.observer = self.qtviewer00300
        self.xaquery_CEXAT11100.observer = self.qtviewer11100
        self.xaquery_CEXAT11300.observer = self.qtviewer11300
        self.xareal_SC0.observer = self.cviewer0
        self.xareal_SC1.observer = self.qtviewerSC1
        self.xareal_C01.observer = self.qtviewerC01
        self.xareal_EU1.observer = self.qtviewerEU1

    
    def run(self):
        self.mt_stop = False
        self.mt_pause = False

        if len(self._accountlist) == 0 :
            self.logger.info('fail: no account')
            return

        if self._servername[:3] == 'MIS':
            accountpwd = ['0000','0000']
        elif self._servername[:1] == 'X':
            accountpwd = ['0302','']
        else:
            self.logger.info('fail: not available servername')
            accountpwd = []
            return

        nowtime = datetime.now()
        if nowtime.hour >= 6 and nowtime.hour < 16:
            self.xareal_SC0.AdviseRealData()
            self.xareal_SC1.AdviseRealData()
            self.xareal_C01.AdviseRealData()
        elif nowtime.hour >= 16 or nowtime.hour < 6:
            self.xareal_EU1.AdviseRealData()

        #self.conn_db = lite.connect('orderlist.db')
        #self.cursor_db = self.conn_db.cursor()

        self.logger.info('Ready')
            
        while True:
            # self.mutex.lock()
            if self.mt_stop: break
            # self.mutex.unlock()

            msg_dict = self.socket.recv_pyobj()
            if not self._XASession.IsConnected():
                self.logger.info('fail: disconnect xsession')
                self.socket.send('fail: disconnect xsession')
                continue
            
            if type(msg_dict) != dict:
                self.logger.info(str(msg_dict) + 'is not dict')
                self.socket.send('fail: msg_dict is not dict')
                continue
            
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime, "%Y-%m-%d %H:%M:%S.%f")
            strnowtime = strnowtime[:-3]                                    
            self.logger.info('receive_order')

            newamendcancel = msg_dict.get('NewAmendCancel', ' ') # 'N' = New, 'A' = Amend, 'C' = Cancel
            buysell = msg_dict.get('BuySell', ' ')   # 'B' = Buy, 'S' = 'Sell'
            shortcd = msg_dict.get('ShortCD', 'NotCD')
            orderprice = msg_dict.get('OrderPrice', 0)
            orderqty = msg_dict.get('OrderQty', 0)
            ordertype = msg_dict.get('OrderType', 0)   # 1 = Market, 2 = Limit
            timeinforce = msg_dict.get('TimeInForce', 'GFD')  # GFD, IOC, FOK
            autotrader_id = msg_dict.get('AutoTraderID', '0')
            orgordno = msg_dict.get('OrgOrderNo', -1)

            if not isinstance(orderprice, float) and newamendcancel in ['N', 'A']:
                self.logger.info('fail: ' + str(msg_dict) + ' orderprice not float')
                self.socket.send('fail: orderprice not float')
                continue
            
            logmsg = '%s, %s, %s, %f, %d, %s, %s' % (
                     autotrader_id,
                     newamendcancel,
                     shortcd,
                     orderprice,
                     int(orderqty),
                     buysell,
                     orgordno, )
                                           
            self.logger.info(logmsg)
            
            if newamendcancel == 'N' and buysell == 'B':
                buysell = '2'
            elif newamendcancel == 'N' and buysell == 'S':
                buysell = '1'
            elif newamendcancel == 'N':
                self.logger.info('invalid newamendcancel, buysell')
                continue

            if newamendcancel == 'N' and shortcd[0] == 'A':
                # equity new order                       
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','AcntNo',0,self._accountlist[self.eq_account_index])
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','InptPwd',0,accountpwd[self.eq_account_index])
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','IsuNo',0,str(shortcd)) #demo
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','OrdQty',0,int(orderqty))
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','OrdPrc',0,str(orderprice))
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','BnsTpCode',0,buysell)
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','OrdprcPtnCode',0,'00')        
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','MgntrnCode',0,'000')
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','LoanDt',0,' ')        
                self.xaquery_CSPAT00600.SetFieldData('CSPAT00600InBlock1','OrdCndiTpCode',0,'0')        
                ret = self.xaquery_CSPAT00600.Request(False)      
                if ret is None:
                    while self.xaquery_CSPAT00600.observer.flag:
                        PumpWaitingMessages()
                    self.xaquery_CSPAT00600.observer.flag = True
                    szMsgCode = self.xaquery_CSPAT00600.data['szMessageCode']
                    if szMsgCode != '00039' and szMsgCode != '00040':
                        # self.ordno_dict[self.xaquery_CSPAT00600.data['OrdNo']] = autotrader_id
                        # self.redis_client.hset('ordno_dict', self.xaquery_CSPAT00600.data['OrdNo'], autotrader_id)
                        self.socket.send(str(szMsgCode))
                    else:
                        self.socket.send(str(szMsgCode))
                    
            elif newamendcancel == 'C' and shortcd[0] == 'A':
                # equity cancel order                                   
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','OrgOrdNo',0,int(orgordno))
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','AcntNo',0,self._accountlist[self.eq_account_index])
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','InptPwd',0,accountpwd[self.eq_account_index])
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','IsuNo',0,str(shortcd)) #demo
                self.xaquery_CSPAT00800.SetFieldData('CSPAT00800InBlock1','OrdQty',0,int(orderqty))                                                
                ret = self.xaquery_CSPAT00800.Request(False)
                if ret is None:
                    # self.ordno_dict[self.xaquery_CSPAT00800.data['OrdNo']] = autotrader_id
                    # self.redis_client.hset('ordno_dict', self.xaquery_CSPAT00800.data['OrdNo'], autotrader_id)
                    self.socket.send('OK')
                    self.logger.info('OK')
                else:
                    self.socket.send('Reject')
                    self.logger.info('Reject')
                
            elif newamendcancel == 'N' and (shortcd[:3] in ['101', '201', '301', '105']):
                if nowtime.hour >= 6 and nowtime.hour < 16:
                    # KRX Futures, Options new order
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','AcntNo',0,self._accountlist[self.fo_account_index])
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','Pwd',0,accountpwd[self.fo_account_index])
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','FnoIsuNo',0,str(shortcd))
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','BnsTpCode',0,buysell)
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','FnoOrdprcPtnCode',0,'00')
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','OrdPrc',0,str(orderprice))
                    self.xaquery_CFOAT00100.SetFieldData('CFOAT00100InBlock1','OrdQty',0,int(orderqty))
                    self.xaquery_CFOAT00100.autotrader_id = autotrader_id
                    ret = self.xaquery_CFOAT00100.Request(False)
                    self.logger.info(str(ret))
                    if not ret:
                        while self.xaquery_CFOAT00100.observer.flag:
                            PumpWaitingMessages()
                        self.xaquery_CFOAT00100.observer.flag = True
                        szMsg = self.xaquery_CFOAT00100.data['szMessage']
                        szMsgCode = self.xaquery_CFOAT00100.data['szMessageCode']
                        self.logger.info(szMsg.strip() + szMsgCode)
                        # if szMsgCode in ['00030', '00040']:
                            # self.ordno_dict[int(self.xaquery_CFOAT00100.data['OrdNo'])] = autotrader_id
                            # self.redis_client.hset('ordno_dict', self.xaquery_CFOAT00100.data['OrdNo'], autotrader_id)
                        self.socket.send(str(szMsgCode))
                else:
                    if shortcd[:3] in ['101', '105']:
                        self.logger.info('not yet implement... 101, 105')
                        self.socket.send('not yet implement...')
                        continue
                    else:
                        # Eurex Options new order
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','AcntNo',0,self._accountlist[self.fo_account_index])
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','Pwd',0,accountpwd[self.fo_account_index])
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','FnoIsuNo',0,str(shortcd))
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','BnsTpCode',0,buysell)
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','ErxPrcCndiTpCode',0,'2')
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','OrdPrc',0,str(orderprice))
                        self.xaquery_CEXAT11100.SetFieldData('CEXAT11100InBlock1','OrdQty',0,int(orderqty))
                        self.xaquery_CEXAT11100.autotrader_id = autotrader_id
                        self.xaquery_CEXAT11100.shortcd = str(shortcd)
                        ret = self.xaquery_CEXAT11100.Request(False)
                        self.logger.info(str(ret))
                        if not ret:
                            while self.xaquery_CEXAT11100.observer.flag:
                                PumpWaitingMessages()
                            self.xaquery_CEXAT11100.observer.flag = True
                            self.shortcd = ''
                            szMsg = self.xaquery_CEXAT11100.data['szMessage']
                            szMsgCode = self.xaquery_CEXAT11100.data['szMessageCode']
                            self.logger.info(szMsg.strip() + szMsgCode)
                            # if szMsgCode in['00030', '00040']:
                                # self.ordno_dict[int(self.xaquery_CEXAT11100.data['OrdNo'])] = autotrader_id
                                # self.redis_client.hset('ordno_dict', self.xaquery_CEXAT11100.data['OrdNo'], autotrader_id)
                            self.socket.send(str(szMsgCode))
                            # self.socket.send('async_ret_ok')
                        else:
                            self.socket.send('async_rect_error %d' % ret)

            elif newamendcancel == 'C' and (shortcd[:3] in ['101', '201', '301', '105']):
                if nowtime.hour >= 6 and nowtime.hour < 16:
                    # KRX Futures, Options Cancel Order
                    self.xaquery_CFOAT00300.SetFieldData('CFOAT00300InBlock1','AcntNo',0,self._accountlist[self.fo_account_index])
                    self.xaquery_CFOAT00300.SetFieldData('CFOAT00300InBlock1','Pwd',0,accountpwd[self.fo_account_index])
                    self.xaquery_CFOAT00300.SetFieldData('CFOAT00300InBlock1','FnoIsuNo',0,shortcd)
                    self.xaquery_CFOAT00300.SetFieldData('CFOAT00300InBlock1','OrgOrdNo',0,int(orgordno))
                    self.xaquery_CFOAT00300.SetFieldData('CFOAT00300InBlock1','CancQty',0,int(orderqty))
                    self.xaquery_CFOAT00300.autotrader_id = autotrader_id
                    ret = self.xaquery_CFOAT00300.Request(False)
                    if ret is None:
                        # self.ordno_dict[self.xaquery_CFOAT00300.data['OrdNo']] = autotrader_id
                        # self.redis_client.hset('ordno_dict', self.xaquery_CFOAT00300.data['OrdNo'], autotrader_id)
                        self.socket.send('OK')
                        self.logger.info('OK')
                    else:
                        self.socket.send('Reject')
                        self.logger.info('Reject')
                else:
                    if shortcd[:3] in ['101', '105']:
                        self.logger.info('not yet implement... 101, 105')
                        self.socket.send('not yet implement...')
                        continue
                    else:
                        # Eurex Options Cancel Order
                        self.xaquery_CEXAT11300.SetFieldData('CEXAT11300InBlock1','OrgOrdNo',0,int(orgordno))
                        self.xaquery_CEXAT11300.SetFieldData('CEXAT11300InBlock1','AcntNo',0,self._accountlist[self.fo_account_index])
                        self.xaquery_CEXAT11300.SetFieldData('CEXAT11300InBlock1','Pwd',0,accountpwd[self.fo_account_index])
                        self.xaquery_CEXAT11300.SetFieldData('CEXAT11300InBlock1','FnoIsuNo',0,str(shortcd))
                        self.xaquery_CEXAT11300.autotrader_id = autotrader_id
                        ret = self.xaquery_CEXAT11300.Request(False)
                        if ret is None:
                            # self.ordno_dict[autotrader_id] = self.xaquery_CEXAT11300.data['OrdNo']
                            # self.redis_client.hset('ordno_dict', self.xaquery_CEXAT11300.data['OrdNo'], autotrader_id)
                            self.socket.send('OK')
                            self.logger.info('OK')
                        else:
                            self.socket.send('Reject')
                            self.logger.info('Reject')
            else:
                self.logger.info('not yet implement other case order')
                self.socket.send('not yet implement other case order')
    

    def stop(self):
        self.mt_stop = True
        pass
        
    def UpdateDB(self):
        #print "receive update "
        self.logger.info('receive_update')
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
            # print 'szMessage',  subject.data['szMessage']
            # print 'szMessageCode', subject.data['szMessageCode'],
#            print 'ordno', subject.data['ordno'],
#            print 'shtcode', subject.data['shtcode'],
#            print 'bnstp', subject.data['bnstp'],
#            print 'ordprice', subject.data['ordprice'],
#            print 'ordqty', subject.data['ordqty'],
#            print 'etfhogagb', subject.data['etfhogagb'],
#            print 'hogagb', subject.data['hogagb'],
#            print 'OrdTime_home', datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]                        
        self.flag = False

