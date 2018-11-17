# -*- coding: utf-8 -*-

import os
import sys
import time
import zmq
import json
import logging
import pythoncom

from PyQt4 import QtCore
from PyQt4 import QtGui

from AQTrader.PyXing import pyxing as px
from AQTrader.PyCybos import pycybos as pc
from AQTrader.CommUtil.FeedCodeList import FeedCodeList
from ui_zerofeeder import Ui_MainWindow
from xinglogindlg import LoginForm
from ZMQTickSender import ZMQTickSender, ZMQTickSender_New

from weakref import proxy

logger = logging.getLogger('ZeroFeeder')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('ZeroFeeder.log')
# fh = logging.Handlers.RotatingFileHandler('ZeroOMS.log',maxBytes=104857,backupCount=3)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
# logger.addHandler(ch)


class ConsoleObserver:
    def Update(self,subject):
        for i in xrange(len(subject.data)):
            print subject.data[i],
        print


class MainForm(QtGui.QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.port = 5500
        self.initUI()
        self.initTIMER()
        self.initAPI()
        self.initFeedCode()
        self.initTAQFeederLst()
        self.initZMQ()

        self.filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\zeroetfviewer'
        self.filename = 'prevclose.txt'
        
        f = open('auto_config', 'r')
        auto_config = json.load(f)
        if auto_config['setauto']:
            print auto_config
            self.setAuto = True
            self.slot_CheckCybosStarter(0, 2)
            self.slot_AutoStartXing(auto_config)        
        f.close()

    def __del__(self):
        self.XASession.DisconnectServer()
        ctypes.windll.user32.PostQuitMessage(0)

    def closeEvent(self, event):
        self.XASession.DisconnectServer()
        ctypes.windll.user32.PostQuitMessage(0)
        setting = QtCore.QSettings("ZeroFeeder.ini", QtCore.QSettings.IniFormat)
        setting.setValue("geometry", self.saveGeometry())
        setting.setValue("port", self.port)

    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conn_cy = QtGui.QTableWidgetItem("conn cy")
        self.conn_xi = QtGui.QTableWidgetItem("conn xi")
        self.status_xi = QtGui.QTableWidgetItem("ready")
        self.status_cy = QtGui.QTableWidgetItem("ready")
        self.ui.tableWidget.setItem(0,2,self.conn_cy)
        self.ui.tableWidget.setItem(1,2,self.conn_xi)
        self.ui.tableWidget.setItem(0,1,self.status_cy)
        self.ui.tableWidget.setItem(1,1,self.status_xi)
        # self.ui.tableWidget.cellClicked.connect(self.cell_was_clicked)

        setting = QtCore.QSettings("ZeroFeeder.ini", QtCore.QSettings.IniFormat)
        value = setting.value("geometry")
        if value:
            self.restoreGeometry(setting.value("geometry").toByteArray())
        value = setting.value("port", type=int)
        if value:
            self.port = value

    def initTIMER(self):
        self.ctimer = QtCore.QTimer()
        self.ctimer.start(1000)
        self.ctimer.timeout.connect(self.CtimerUpdate)
        self.cybostimer = QtCore.QTimer()
        self.cybostimer.timeout.connect(self.CybosTimerUpdate)
        self.xingtimer = QtCore.QTimer()
        self.xingtimer.timeout.connect(self.XingTimerUpdate)
        self.lbltime = QtGui.QLabel(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        self.statusBar().addPermanentWidget(self.lbltime)

    def initAPI(self):
        self.XASession_observer = XingXASessionUpdate(proxy(self.status_xi))
        self.XASession = px.XASession()
        self.XASession.Attach(self.XASession_observer)
        self.cpcybos = CpCybosNULL()

    def initFeedCode(self):
        self._FeedCodeList = FeedCodeList()
        self._FeedCodeList.read_code_list()

    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://127.0.0.1:%d" % self.port)
        logger.info('zmq port: %d' % self.port)

        self.socket_test = context.socket(zmq.PUB)
        self.socket_test.bind("tcp://127.0.0.1:%d" % (self.port + 1))
        logger.info('zmq test port: %d' % (self.port + 1))

    def initZMQSender(self):
        self.ZMQFuturesTradeSender = ZMQTickSender(self.socket, 'xing', 'T', 'futures')
        self.ZMQFuturesQuoteSender = ZMQTickSender(self.socket, 'cybos', 'Q', 'futures')
        self.ZMQFuturesTradeSender_test = ZMQTickSender_New(self.socket_test, 'xing', 'T', 'futures')
        self.ZMQFuturesQuoteSender_test = ZMQTickSender_New(self.socket_test, 'xing', 'Q', 'futures')
        self.ZMQFuturesExpectSender = ZMQTickSender(self.socket, 'cybos', 'E', 'futures')
        self.ZMQFuturesNightQuoteSender = ZMQTickSender(self.socket, 'xing', 'Q', 'futures')
        self.ZMQFuturesNightTradeSender_test = ZMQTickSender_New(self.socket_test, 'xing', 'T', 'futures')
        self.ZMQFuturesNightQuoteSender_test = ZMQTickSender_New(self.socket_test, 'xing', 'Q', 'futures')
        self.ZMQOptionsTradeSender = ZMQTickSender(self.socket, 'xing', 'T', 'options')
        self.ZMQOptionsQuoteSender = ZMQTickSender(self.socket, 'cybos', 'Q', 'options')
        self.ZMQOptionsTradeSender_test = ZMQTickSender_New(self.socket_test, 'xing', 'T', 'options')
        self.ZMQOptionsQuoteSender_test = ZMQTickSender_New(self.socket_test, 'xing', 'Q', 'options')
        self.ZMQOptionsNightQuoteSender = ZMQTickSender(self.socket, 'xing', 'Q', 'options')
        self.ZMQOptionsNightTradeSender_test = ZMQTickSender_New(self.socket_test, 'xing', 'T', 'options')
        self.ZMQOptionsNightQuoteSender_test = ZMQTickSender_New(self.socket_test, 'xing', 'Q', 'options')
        self.ZMQOptionsExpectSender = ZMQTickSender(self.socket, 'cybos', 'E', 'options')
        self.ZMQEquityTradeSender = ZMQTickSender(self.socket, 'xing', 'T', 'equity')
        self.ZMQEquityQuoteSender = ZMQTickSender(self.socket, 'cybos', 'Q', 'equity')
        self.ZMQFuturesExpectSender_xing = ZMQTickSender_New(self.socket_test, 'xing', 'E', 'futures')
        self.ZMQOptionsExpectSender_xing = ZMQTickSender_New(self.socket_test, 'xing', 'E', 'options')
        self.ZMQEquityExpectSender = ZMQTickSender(self.socket, 'xing', 'E', 'equity')
        self.ZMQIndexExpectSender = ZMQTickSender(self.socket, 'cybos', 'E', 'index')
        self.ZMQETFNAVSender = ZMQTickSender(self.socket, 'xing', 'N', 'equity')
        self.obs = ConsoleObserver()

    def initTAQFeederLst(self):
        self.FutureTAQFeederLst = []
        self.FutureTAQFeederDict = {}
        self.OptionTAQFeederLst = []
        self.OptionTAQFeederDict = {}
        self.EquityTAQFeederLst = []


    def initOptionJpBid(self):
        newitemquote = pc.OptionJpBid()        
        newitemquote.Attach(self.ZMQOptionsQuoteSender)
        self.OptionTAQFeederDict['OptionJpBid'] = newitemquote

    def initOC0(self):
        newitemtrade = px.XAReal_OC0(DataType='list')
        newitemtrade_new = px.XAReal_OC0(DataType='dictionary')
        newitemtrade.Attach(self.ZMQOptionsTradeSender)
        newitemtrade_new.Attach(self.ZMQOptionsTradeSender_test)
        self.OptionTAQFeederDict['OC0'] = newitemtrade
        self.OptionTAQFeederDict['OC0_New'] = newitemtrade_new
            
    def initOH0(self):
        # newitemquote = px.XAReal_OH0(DataType='list')
        newitemquote_new = px.XAReal_OH0(DataType='dictionary')
        # newitemquote.Attach(self.ZMQOptionsQuoteSender)
        newitemquote_new.Attach(self.ZMQOptionsQuoteSender_test)
        # self.OptionTAQFeederDict['OH0'] = newitemquote
        self.OptionTAQFeederDict['OH0_New'] = newitemquote_new
            
    def initEC0(self):
        newitemtrade = px.XAReal_EC0(DataType='list')
        newitemtrade_new = px.XAReal_EC0(DataType='dictionary')        
        newitemtrade.Attach(self.ZMQOptionsTradeSender)
        newitemtrade_new.Attach(self.ZMQOptionsNightTradeSender_test)
        self.OptionTAQFeederDict['EC0'] = newitemtrade
        self.OptionTAQFeederDict['EC0_New'] = newitemtrade_new

    def initEH0(self):
        newitemquote = px.XAReal_EH0(DataType='list')
        newitemquote_new = px.XAReal_EH0(DataType='dictionary')        
        newitemquote.Attach(self.ZMQOptionsNightQuoteSender)
        newitemquote_new.Attach(self.ZMQOptionsNightQuoteSender_test)
        self.OptionTAQFeederDict['EH0'] = newitemquote
        self.OptionTAQFeederDict['EH0_New'] = newitemquote_new

    def initFOExpect(self):
        newitemoption_aution = pc.FOExpectCur()
        newitemoption_aution.Attach(self.ZMQOptionsExpectSender)
        self.OptionTAQFeederDict['OptionExpect'] = newitemoption_aution
            
    def initYFC(self):
        newitemfuture_aution_new = px.XAReal_YFC(DataType='dictionary')
        newitemfuture_aution_new.Attach(self.ZMQFuturesExpectSender_xing)
        self.FutureTAQFeederDict['YFC'] = newitemfuture_aution_new
            
    def initYOC(self):
        newitemoption_aution_new = px.XAReal_YOC(DataType='dictionary')        
        newitemoption_aution_new.Attach(self.ZMQOptionsExpectSender_xing)
        self.OptionTAQFeederDict['YOC'] = newitemoption_aution_new

    def registerFeedItem_FC0(self, shortcd):
        newitemtrade = px.XAReal_FC0(shortcd, 'list')
        newitemtrade.Attach(self.ZMQFuturesTradeSender)
        newitemtrade.AdviseRealData()
        self.FutureTAQFeederLst.append(newitemtrade)
        #==================================================
        newitemtrade_new = px.XAReal_FC0(shortcd, 'dictionary')
        newitemtrade_new.Attach(self.ZMQFuturesTradeSender_test)
        newitemtrade_new.AdviseRealData()
        self.FutureTAQFeederLst.append(newitemtrade_new)
        
    def registerFeedItem_FH0(self, shortcd):
        #==================================================
        newitemquote_new = px.XAReal_FH0(shortcd, 'dictionary')
        newitemquote_new.Attach(self.ZMQFuturesQuoteSender_test)
        newitemquote_new.AdviseRealData()
        self.FutureTAQFeederLst.append(newitemquote_new)

    def registerFeedItem_NC0(self, shortcd):
        newitemtrade = px.XAReal_NC0(shortcd, 'list')
        newitemtrade.Attach(self.ZMQFuturesTradeSender)
        newitemtrade.AdviseRealData()
        self.FutureTAQFeederLst.append(newitemtrade)
        #==================================================
        newitemtrade_new = px.XAReal_NC0(shortcd, 'dictionary')
        newitemtrade_new.Attach(self.ZMQFuturesNightTradeSender_test)
        newitemtrade_new.AdviseRealData()
        self.FutureTAQFeederLst.append(newitemtrade_new)

    def registerFeedItem_OC0(self, shortcd):
        self.OptionTAQFeederDict['OC0'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['OC0'].AdviseRealData()
        self.OptionTAQFeederDict['OC0_New'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['OC0_New'].AdviseRealData()

    def registerFeedItem_EC0(self, shortcd):
        self.OptionTAQFeederDict['EC0'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['EC0'].AdviseRealData()
        self.OptionTAQFeederDict['EC0_New'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['EC0_New'].AdviseRealData()
        
    def registerFeedItem_YFC(self, shortcd):
        self.FutureTAQFeederDict['YFC'].SetFieldData('InBlock', 'futcode', shortcd)
        self.FutureTAQFeederDict['YFC'].AdviseRealData()
        
    def registerFeedItem_YOC(self, shortcd):
        self.OptionTAQFeederDict['YOC'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['YOC'].AdviseRealData()

    def registerFeedItem_S3_(self, shortcd):
        newitemtrade = px.XAReal_S3_(shortcd, 'list')
        newitemtrade.Attach(self.ZMQEquityTradeSender)
        newitemtrade.AdviseRealData()
        self.EquityTAQFeederLst.append(newitemtrade)

    def registerFeedItem_YS3(self, shortcd):
        newitem_aution = px.XAReal_YS3(shortcd, 'list')
        newitem_aution.Attach(self.ZMQEquityExpectSender)
        newitem_aution.AdviseRealData()
        self.EquityTAQFeederLst.append(newitem_aution)

    def registerFeedItem_I5_(self, shortcd):
        NewItemNAV = px.XAReal_I5_(shortcd, 'list')
        NewItemNAV.Attach(self.ZMQETFNAVSender)
        NewItemNAV.AdviseRealData()
        self.EquityTAQFeederLst.append(NewItemNAV)

    def registerFeedItem_FOExpect(self, shortcd):
        if shortcd[:3] in ['101', '105']:
            newitem_aution = pc.FOExpectCur()
            newitem_aution.Attach(self.ZMQFuturesExpectSender)
            newitem_aution.SetInputValue(0, shortcd[:-3])
            newitem_aution.SetInputValue(1, 'F1')
            newitem_aution.SetInputValue(2, shortcd[3:-3])
            newitem_aution.Subscribe()
            self.FutureTAQFeederLst.append(newitem_aution)
        elif shortcd[:3] == '201' or shortcd[:3] == '301':
            self.OptionTAQFeederDict['OptionExpect'].SetInputValue(0, shortcd)
            self.OptionTAQFeederDict['OptionExpect'].SetInputValue(1, 'O1')
            self.OptionTAQFeederDict['OptionExpect'].SetInputValue(2, shortcd[3:-3])
            self.OptionTAQFeederDict['OptionExpect'].Subscribe()

    def registerFeedItem_FutureJpBid(self, shortcd):
        newitemquote = pc.FutureJpBid(shortcd[:-3])
        newitemquote.Attach(self.ZMQFuturesQuoteSender)
        newitemquote.Subscribe()
        self.FutureTAQFeederLst.append(newitemquote)

    def registerFeedItem_CMECurr(self, shortcd):
        newitemquote = pc.CmeCurr(shortcd[:-3])
        newitemquote.Attach(self.ZMQFuturesQuoteSender)
        newitemquote.Subscribe()
        self.FutureTAQFeederLst.append(newitemquote)

    def registerFeedItem_OptionJpBid(self, shortcd):
        self.OptionTAQFeederDict['OptionJpBid'].Subscribe('0', shortcd)

    def registerFeedItem_NH0(self, shortcd):
        newitemquote = px.XAReal_NH0(shortcd, 'list')
        newitemquote.Attach(self.ZMQFuturesNightQuoteSender)
        newitemquote.AdviseRealData()
        self.FutureTAQFeederLst.append(newitemquote)
        #===================================================
        newitemquote_new = px.XAReal_NH0(shortcd, 'dictionary')
        newitemquote_new.Attach(self.ZMQFuturesNightQuoteSender_test)
        newitemquote_new.AdviseRealData()
        self.FutureTAQFeederLst.append(newitemquote_new)

    def registerFeedItem_OH0(self, shortcd):
        self.OptionTAQFeederDict['OH0_New'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['OH0_New'].AdviseRealData()

    def registerFeedItem_EH0(self, shortcd):
        self.OptionTAQFeederDict['EH0'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['EH0'].AdviseRealData()
        self.OptionTAQFeederDict['EH0_New'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['EH0_New'].AdviseRealData()

    def registerFeedItem_StockJpBid(self, shortcd):
        newitemquote = pc.StockJpBid('A' + shortcd)
        newitemquote.Attach(self.ZMQEquityQuoteSender)
        newitemquote.Subscribe()
        self.EquityTAQFeederLst.append(newitemquote)

    def registerFeedItem_ExpectIndexS(self, shortcd):
        newitem_index_expect = pc.ExpectIndexS(shortcd)
        newitem_index_expect.Attach(self.ZMQIndexExpectSender)
        newitem_index_expect.Subscribe()
        self.EquityTAQFeederLst.append(newitem_index_expect)

    def slot_ToggleFeed(self, boolToggle):
        if boolToggle:
            # self.slot_RequestPrevClosePrice()
            pythoncom.CoInitialize()
            self.initFeedCode()
            self.initZMQSender()
            self.initTAQFeederLst()
        else:
            logger.info('tick count: %d'%ZMQTickSender.count)

        if self.XASession.IsConnected() and boolToggle:
            nowlocaltime = time.localtime()
            if nowlocaltime.tm_hour >= 6 and nowlocaltime.tm_hour < 16:
                self.initYFC()
                for shortcd in self._FeedCodeList.future_shortcd_list:
                    self.registerFeedItem_FC0(shortcd)
                    self.registerFeedItem_FH0(shortcd)
                    self.registerFeedItem_YFC(shortcd)
            else:
                for shortcd in self._FeedCodeList.future_shortcd_list:
                    self.registerFeedItem_NC0(shortcd)
                    self.registerFeedItem_NH0(shortcd)

            if nowlocaltime.tm_hour >= 6 and nowlocaltime.tm_hour < 16:
                self.initOC0()
                self.initOH0()
                self.initYOC()
                for shortcd in self._FeedCodeList.option_shortcd_list:
                    self.registerFeedItem_OC0(shortcd)
                    self.registerFeedItem_OH0(shortcd)
                    self.registerFeedItem_YOC(shortcd)
            else:
                self.initEC0()
                self.initEH0()
                for shortcd in self._FeedCodeList.option_shortcd_list:
                    self.registerFeedItem_EC0(shortcd)
                    self.registerFeedItem_EH0(shortcd)
                for shortcd in self._FeedCodeList.future_shortcd_list:
                    if shortcd[:3] == '105':
                        self.registerFeedItem_EC0(shortcd)
                        self.registerFeedItem_EH0(shortcd)

            for shortcd in self._FeedCodeList.equity_shortcd_list:
                self.registerFeedItem_S3_(shortcd)
                self.registerFeedItem_YS3(shortcd)
                self.registerFeedItem_I5_(shortcd)

        if self.cpcybos.IsConnect() and boolToggle:
            nowlocaltime = time.localtime()
            for shortcd in self._FeedCodeList.future_shortcd_list:
                if nowlocaltime.tm_hour >= 6 and nowlocaltime.tm_hour < 16:
                    self.registerFeedItem_FutureJpBid(shortcd)
                else:
                    self.registerFeedItem_CMECurr(shortcd)
                self.registerFeedItem_FOExpect(shortcd)

            self.initOptionJpBid()
            self.initFOExpect()
            if nowlocaltime.tm_hour >= 6 and nowlocaltime.tm_hour < 16:
                for shortcd in self._FeedCodeList.option_shortcd_list:
                    self.registerFeedItem_OptionJpBid(shortcd)
                    self.registerFeedItem_FOExpect(shortcd)

            for shortcd in self._FeedCodeList.equity_shortcd_list:
                self.registerFeedItem_StockJpBid(shortcd)

            for shortcd in self._FeedCodeList.index_shortcd_list:
                self.registerFeedItem_ExpectIndexS(shortcd)

        if boolToggle:
            pythoncom.PumpMessages()

        pass

    def slot_RequestPrevClosePrice(self):
        if self.cpcybos.IsConnect():
            filep = open(self.filepath + '\\' + self.filename,'w+')
            msglist = []
            for shortcd in self._FeedCodeList.future_shortcd_list:
                _FutureMst = pc.FutureMst(shortcd[:-3])
                _FutureMst.Request()
                while 1:
                    pythoncom.PumpWaitingMessages()
                    if _FutureMst.data:
                        print shortcd
                        print _FutureMst.data[22]
                        msglist.append(str(_FutureMst.data[22]))
                        break

            for shortcd in self._FeedCodeList.option_shortcd_list:
                _OptionMst = pc.OptionMst(shortcd)
                _OptionMst.Request()
                while 1:
                    pythoncom.PumpWaitingMessages()
                    if _OptionMst.data:
                        print shortcd
                        print round(_OptionMst.data[27],2)
                        break

            strshortcdlist = 'A' + ',A'.join(self._FeedCodeList.equity_shortcd_list)
            _StockMst2 = pc.StockMst2(strshortcdlist)
            _StockMst2.Request()
            while 1:
                pythoncom.PumpWaitingMessages()
                if _StockMst2.data:
                    for i in xrange(_StockMst2.count):
                        print _StockMst2.data[19+30*i]
                        msglist.append(str(_StockMst2.data[19+30*i]))
                    break
            filep.write(','.join(msglist) + '\n')
            filep.close()
        pass

    def slot_StartXingDlg(self,row,column):
        if row == 1 and column == 2:
            # print("Row %d and Column %d was doblueclicked" % (row,column))
            local_login_form = LoginForm(XASession=proxy(self.XASession))
            local_login_form.show()
            local_login_form.exec_()
            self.xingtimer.start(1000)
            
    def slot_AutoStartXing(self, auto_config):
        server = 'hts.ebestsec.co.kr'
        port = 20001
        servertype = 0
        showcerterror = 1
        user = str(auto_config['id'])
        password = str(auto_config['pwd'].decode('hex'))
        certpw = str(auto_config['cetpwd'].decode('hex'))
        
        self.XASession.ConnectServer(server,port)
        # print 'connect server'
        ret = self.XASession.Login(user, password, certpw, servertype, showcerterror)
                
        px.XASessionEvents.session = self.XASession
        self.XASession.flag = True
        while self.XASession.flag:
            pythoncom.PumpWaitingMessages()
            
        self.xingtimer.start(1000)
        pass

    def slot_CheckCybosStarter(self, row, column):
        if row == 0 and column == 2:
            self.cpcybos = pc.CpCybos()
            self.status_cy.setText('connect')
            self.cybostimer.start(1000)

    def CtimerUpdate(self):
        now_time = time.localtime()
        self.lbltime.setText(time.strftime("%Y-%m-%d %H:%M:%S",now_time))
        close_trigger = False
        if now_time.tm_hour == 6 and  now_time.tm_min == 25:
            self.cpcybos.PlusDisconnect()
            close_trigger = True
        elif now_time.tm_hour == 17 and  now_time.tm_min == 25:
            self.slot_ToggleFeed(True)

        if close_trigger:
            self.close()

    def CybosTimerUpdate(self):
        if self.cpcybos.IsConnect():
            if self.status_cy.text() == 'connect':
                self.status_cy.setText('connect.')
            elif self.status_cy.text() == 'connect.':
                self.status_cy.setText('connect..')
            elif self.status_cy.text() == 'connect..':
                self.status_cy.setText('connect...')
            elif self.status_cy.text() == 'connect...':
                self.status_cy.setText('connect')
        else:
            self.status_cy.setText('disconnect')

    def XingTimerUpdate(self):
        if self.XASession.IsConnected():
            if self.status_xi.text() == 'connect' or self.status_xi.text() == 'connect: 0000':
                self.status_xi.setText('connect.')
            elif self.status_xi.text() == 'connect.':
                self.status_xi.setText('connect..')
            elif self.status_xi.text() == 'connect..':
                self.status_xi.setText('connect...')
            elif self.status_xi.text() == 'connect...':
                self.status_xi.setText('connect')
        else:
            self.status_xi.setText('disconnect')


class XingXASessionUpdate():
    def __init__(self, status_xi=None):
        self.status_xi = status_xi

    def Update(self, subject):
        msg =''
        for item in subject.data:
            msg = msg + ' ' + item
        if msg[:5] == ' 0000':
            self.status_xi.setText('connect:' + msg[:5])
        pass


class CpCybosNULL():
    def IsConnect(self):
        return False


if __name__ == '__main__':
    import ctypes
    myappid = 'zerofeeder'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
#    if myform.setAuto:
#        myform.ui.actionFeed.setChecked(True)
    app.exec_()

