# -*- coding: utf-8 -*-

import os
import sys
import time
import zmq
import ctypes
import json
import logging
import pythoncom

import pyxing as px
import pycybos as pc
from ..CommUtil.FeedCodeList import FeedCodeList

from PyQt4 import QtCore
from PyQt4 import QtGui
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
    def __init__(self,parent=None):
        super(MainForm,self).__init__()
        self.initUI()
        self.initTIMER()
        self.initAPI()
        self.initFeedCode()
        self.initTAQFeederLst()
        self.initZMQ()

        self.filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\zeroetfviewer'
        self.filename = 'prevclose.txt'
        
        f = open('auto_config','r')
        auto_config = json.load(f)
        if auto_config['setauto']:
            print auto_config
            self.setAuto = True
            self.slot_CheckCybosStarter(0,2)
            self.slot_AutoStartXing(auto_config)        
        f.close()

    def __del__(self):
        self.XASession.DisconnectServer()
        ctypes.windll.user32.PostQuitMessage(0)

    def closeEvent(self, event):
        self.XASession.DisconnectServer()
        ctypes.windll.user32.PostQuitMessage(0)
        setting = QtCore.QSettings("ZeroFeeder.ini",QtCore.QSettings.IniFormat)
        setting.setValue("geometry",self.saveGeometry())

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

        setting = QtCore.QSettings("ZeroFeeder.ini",QtCore.QSettings.IniFormat)
        value = setting.value("geometry")
        if value:
            self.restoreGeometry(setting.value("geometry").toByteArray())
        # self.restoreGeometry(setting.value("geometry"))

    def initTIMER(self):
        self.ctimer =  QtCore.QTimer()
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
        self._CpCybos = CpCybosNULL()

    def initFeedCode(self):
        self._FeedCodeList = FeedCodeList()
        self._FeedCodeList.read_code_list()

    def initZMQ(self):
        context = zmq.Context()
        # self.socket = context.socket(zmq.PUB)
        # self.socket.bind("tcp://127.0.0.1:5502")
        self.socket_test = context.socket(zmq.PUB)
        self.socket_test.bind("tcp://127.0.0.1:5503")

    def initZMQSender(self):
        # self.ZMQFuturesTradeSender = ZMQTickSender(self.socket,'xing','T','futures')
        # self.ZMQFuturesQuoteSender = ZMQTickSender(self.socket,'cybos','Q','futures')
        # self.ZMQFuturesExpectSender = ZMQTickSender(self.socket,'cybos','E','futures')
        # self.ZMQFuturesNightQuoteSender = ZMQTickSender(self.socket,'xing','Q','futures')
        # self.ZMQOptionsTradeSender = ZMQTickSender(self.socket,'xing','T','options')
        # self.ZMQOptionsQuoteSender = ZMQTickSender(self.socket,'cybos','Q','options')
        # self.ZMQOptionsNightQuoteSender = ZMQTickSender(self.socket,'xing','Q','options')
        # self.ZMQOptionsExpectSender = ZMQTickSender(self.socket,'cybos','E','options')
        # self.ZMQEquityTradeSender = ZMQTickSender(self.socket,'xing','T','equity')
        # self.ZMQEquityQuoteSender = ZMQTickSender(self.socket,'cybos','Q','equity')
        # self.ZMQEquityExpectSender = ZMQTickSender(self.socket,'xing','E','equity')
        # self.ZMQIndexExpectSender = ZMQTickSender(self.socket,'cybos','E','index')
        # self.ZMQETFNAVSender = ZMQTickSender(self.socket,'xing','N','equity')

        self.ZMQFuturesTradeSender_xing = ZMQTickSender_New(self.socket_test, 'xing', 'T', 'futures')
        self.ZMQFuturesQuoteSender_xing = ZMQTickSender_New(self.socket_test, 'xing', 'Q', 'futures')
        self.ZMQFuturesNightTradeSender_xing = ZMQTickSender_New(self.socket_test, 'xing', 'T', 'futures')
        self.ZMQFuturesNightQuoteSender_xing = ZMQTickSender_New(self.socket_test, 'xing', 'Q', 'futures')
        self.ZMQOptionsTradeSender_xing = ZMQTickSender_New(self.socket_test, 'xing', 'T', 'options')
        self.ZMQOptionsQuoteSender_xing = ZMQTickSender_New(self.socket_test, 'xing', 'Q', 'options')
        self.ZMQOptionsNightTradeSender_xing = ZMQTickSender_New(self.socket_test, 'xing', 'T', 'options')
        self.ZMQOptionsNightQuoteSender_xing = ZMQTickSender_New(self.socket_test, 'xing', 'Q', 'options')
        self.ZMQFuturesExpectSender_xing = ZMQTickSender_New(self.socket_test, 'xing', 'E', 'futures')
        self.ZMQOptionsExpectSender_xing = ZMQTickSender_New(self.socket_test, 'xing', 'E', 'options')
        self.obs = ConsoleObserver()

    def initTAQFeederLst(self):
        self.FutureTAQFeederLst = []
        self.FutureTAQFeederDict = {}
        self.OptionTAQFeederLst = []
        self.OptionTAQFeederDict = {}
        self.EquityTAQFeederLst = []


    def initOptionJpBid(self):
        NewItemQuote = pc.OptionJpBid()
        if 'ZMQOptionsQuoteSender' in self.__dict__:
            NewItemQuote.Attach(self.ZMQOptionsQuoteSender)
            self.OptionTAQFeederDict['OptionJpBid'] = NewItemQuote
            
    def initFC0(self):
        newitem_trade = px.XAReal_FC0(DataType='dictionary')
        if 'ZMQFuturesTradeSender_xing' in self.__dict__:
            newitem_trade.Attach(self.ZMQFuturesTradeSender_xing)
            self.FutureTAQFeederDict['FC0'] = newitem_trade

    def initFH0(self):
        newitem_quote = px.XAReal_FH0(DataType='dictionary')
        if 'ZMQFuturesQuoteSender_xing' in self.__dict__:
            newitem_quote.Attach(self.ZMQFuturesQuoteSender_xing)
            self.FutureTAQFeederDict['FH0'] = newitem_quote

    def initOC0(self):        
        newitem_trade = px.XAReal_OC0(DataType='dictionary')
        if 'ZMQOptionsTradeSender_xing' in self.__dict__:
            newitem_trade.Attach(self.ZMQOptionsTradeSender_xing)
            self.OptionTAQFeederDict['OC0'] = newitem_trade
            
    def initOH0(self):        
        newitemquote = px.XAReal_OH0(DataType='dictionary')
        if 'ZMQOptionsQuoteSender_xing' in self.__dict__:
            newitemquote.Attach(self.ZMQOptionsQuoteSender_xing)
            self.OptionTAQFeederDict['OH0'] = newitemquote

    def initNC0(self):
        newitem_trade = px.XAReal_NC0(DataType='dictionary')
        if 'ZMQFuturesNightTradeSender_xing' in self.__dict__:
            newitem_trade.Attach(self.ZMQFuturesNightTradeSender_xing)
            self.FutureTAQFeederDict['NC0'] = newitem_trade

    def initNH0(self):
        newitem_quote = px.XAReal_NH0(DataType='dictionary')
        if 'ZMQFuturesNightQuoteSender_xing' in self.__dict__:
            newitem_quote.Attach(self.ZMQFuturesNightQuoteSender_xing)
            self.FutureTAQFeederDict['NH0'] = newitem_quote
            
    def initEC0(self):        
        newitem_trade = px.XAReal_EC0(DataType='dictionary')
        if 'ZMQOptionsTradeSender_xing' in self.__dict__:
            newitem_trade.Attach(self.ZMQOptionsNightTradeSender_xing)
            self.OptionTAQFeederDict['EC0'] = newitem_trade

    def initEH0(self):        
        newitemquote = px.XAReal_EH0(DataType='dictionary')
        if 'ZMQOptionsNightQuoteSender_xing' in self.__dict__:
            newitemquote.Attach(self.ZMQOptionsNightQuoteSender_xing)
            self.OptionTAQFeederDict['EH0'] = newitemquote

    def initFOExpect(self):
        NewItemOptionExpect = pc.FOExpectCur()        
        if 'ZMQOptionsExpectSender' in self.__dict__:
            NewItemOptionExpect.Attach(self.ZMQOptionsExpectSender)
            self.OptionTAQFeederDict['OptionExpect'] = NewItemOptionExpect
            
    def initYFC(self):
        NewItemFutureExpect_New = px.XAReal_YFC(DataType='dictionary')
        if 'ZMQFuturesExpectSender_xing' in self.__dict__:
            NewItemFutureExpect_New.Attach(self.ZMQFuturesExpectSender_xing)
            self.FutureTAQFeederDict['YFC'] = NewItemFutureExpect_New
            
    def initYOC(self):
        NewItemOptionExpect_New = px.XAReal_YOC(DataType='dictionary')
        if 'ZMQOptionsExpectSender_xing' in self.__dict__:
            NewItemOptionExpect_New.Attach(self.ZMQOptionsExpectSender_xing)
            self.OptionTAQFeederDict['YOC'] = NewItemOptionExpect_New

    def registerFeedItem_FC0(self, shortcd):
        self.FutureTAQFeederDict['FC0'].SetFieldData('InBlock', 'futcode', shortcd)
        self.FutureTAQFeederDict['FC0'].AdviseRealData()
        
    def registerFeedItem_FH0(self, shortcd):
        self.FutureTAQFeederDict['FH0'].SetFieldData('InBlock', 'futcode', shortcd)
        self.FutureTAQFeederDict['FH0'].AdviseRealData()

    def registerFeedItem_OC0(self, shortcd):        
        self.OptionTAQFeederDict['OC0'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['OC0'].AdviseRealData()

    def registerFeedItem_OH0(self, shortcd):
        self.OptionTAQFeederDict['OH0'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['OH0'].AdviseRealData()

    def registerFeedItem_NC0(self, shortcd):
        self.FutureTAQFeederDict['NC0'].SetFieldData('InBlock', 'futcode', shortcd)
        self.FutureTAQFeederDict['NC0'].AdviseRealData()

    def registerFeedItem_NH0(self, shortcd):
        self.FutureTAQFeederDict['NH0'].SetFieldData('InBlock', 'futcode', shortcd)
        self.FutureTAQFeederDict['NH0'].AdviseRealData()

    def registerFeedItem_EC0(self, shortcd):
        self.OptionTAQFeederDict['EC0'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['EC0'].AdviseRealData()

    def registerFeedItem_EH0(self, shortcd):
        self.OptionTAQFeederDict['EH0'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['EH0'].AdviseRealData()
        
    def registerFeedItem_YFC(self, shortcd):
        self.FutureTAQFeederDict['YFC'].SetFieldData('InBlock', 'futcode', shortcd)
        self.FutureTAQFeederDict['YFC'].AdviseRealData()
        
    def registerFeedItem_YOC(self, shortcd):
        self.OptionTAQFeederDict['YOC'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['YOC'].AdviseRealData()

    # ===============================================================================

    def registerFeedItem_S3_(self, shortcd):
        newitem_trade = px.XAReal_S3_(shortcd, 'list')
        if 'ZMQEquityTradeSender' in self.__dict__:
            newitem_trade.Attach(self.ZMQEquityTradeSender)
            newitem_trade.AdviseRealData()
            self.EquityTAQFeederLst.append(newitem_trade)

    def registerFeedItem_YS3(self, shortcd):
        NewItemExpect = px.XAReal_YS3(shortcd,'list')
        if 'ZMQEquityExpectSender' in self.__dict__:
            NewItemExpect.Attach(self.ZMQEquityExpectSender)
            NewItemExpect.AdviseRealData()
            self.EquityTAQFeederLst.append(NewItemExpect)

    def registerFeedItem_I5_(self, shortcd):
        NewItemNAV = px.XAReal_I5_(shortcd, 'list')
        if 'self.ZMQETFNAVSender' in self.__dict__:
            NewItemNAV.Attach(self.ZMQETFNAVSender)
            NewItemNAV.AdviseRealData()
            self.EquityTAQFeederLst.append(NewItemNAV)

    def registerFeedItem_FOExpect(self, shortcd):
        if shortcd[:3] == '101':
            NewItemExpect = pc.FOExpectCur()
            # if 'ZMQFuturesExpectSender' in self.__dict__:
            #     NewItemExpect.Attach(self.ZMQFuturesExpectSender)
            #     NewItemExpect.SetInputValue(0, shortcd[:-3])
            #     NewItemExpect.SetInputValue(1,'F1')
            #     NewItemExpect.SetInputValue(2, shortcd[3:-3])
            #     NewItemExpect.Subscribe()
            #     self.FutureTAQFeederLst.append(NewItemExpect)
        # elif shortcd[:3] == '201' or shortcd[:3] == '301':
        #     self.OptionTAQFeederDict['OptionExpect'].SetInputValue(0,shortcd)
        #     self.OptionTAQFeederDict['OptionExpect'].SetInputValue(1,'O1')
        #     self.OptionTAQFeederDict['OptionExpect'].SetInputValue(2,shortcd[3:-3])
        #     self.OptionTAQFeederDict['OptionExpect'].Subscribe()

    def registerFeedItem_FutureJpBid(self, shortcd):
        NewItemQuote = pc.FutureJpBid(shortcd[:-3])
        if 'ZMQFuturesQuoteSender' in self.__dict__:
            NewItemQuote.Attach(self.ZMQFuturesQuoteSender)
            NewItemQuote.Subscribe()
            self.FutureTAQFeederLst.append(NewItemQuote)

    def registerFeedItem_CMECurr(self, shortcd):
        NewItemQuote = pc.CmeCurr(shortcd[:-3])
        if 'ZMQFuturesQuoteSender' in self.__dict__:
            NewItemQuote.Attach(self.ZMQFuturesQuoteSender)
            NewItemQuote.Subscribe()
            self.FutureTAQFeederLst.append(NewItemQuote)

    def registerFeedItem_OptionJpBid(self, shortcd):
        # self.OptionTAQFeederDict['OptionJpBid'].Subscribe('0',shortcd)
        pass

    def registerFeedItem_StockJpBid(self, shortcd):
        NewItemQuote = pc.StockJpBid('A' + shortcd)
        if 'ZMQEquityQuoteSender' in self.__dict__:
            NewItemQuote.Attach(self.ZMQEquityQuoteSender)
            NewItemQuote.Subscribe()
            self.EquityTAQFeederLst.append(NewItemQuote)

    def registerFeedItem_ExpectIndexS(self, shortcd):
        NewItemExpectIndex  = pc.ExpectIndexS(shortcd)
        if 'ZMQIndexExpectSender' in self.__dict__:
            NewItemExpectIndex.Attach(self.ZMQIndexExpectSender)
            NewItemExpectIndex.Subscribe()
            self.EquityTAQFeederLst.append(NewItemExpectIndex)

    def slot_ToggleFeed(self, boolToggle):

        if boolToggle:
            #self.slot_RequestPrevClosePrice()
            pythoncom.CoInitialize()
            self.initFeedCode()
            self.initZMQSender()
            self.initTAQFeederLst()
        else:
            logger.info('tick count: %d'%ZMQTickSender.count)

        if self.XASession.IsConnected() and boolToggle:
            nowlocaltime = time.localtime()
            if nowlocaltime.tm_hour >= 6 and nowlocaltime.tm_hour < 16:
                self.initFC0()
                self.initFH0()
                self.initOC0()
                self.initOH0()
                self.initYFC()
                self.initYOC()

                for shortcd in self._FeedCodeList.futureshortcdlst:
                    self.registerFeedItem_FC0(shortcd)
                    self.registerFeedItem_FH0(shortcd)
                    self.registerFeedItem_YFC(shortcd)

                for shortcd in self._FeedCodeList.optionshortcdlst:
                    self.registerFeedItem_OC0(shortcd)
                    self.registerFeedItem_OH0(shortcd)
                    self.registerFeedItem_YOC(shortcd)
            else:
                self.initNC0()
                self.initNH0()
                self.initEC0()
                self.initEH0()
                self.initYFC()
                self.initYOC()

                for shortcd in self._FeedCodeList.futureshortcdlst:
                    self.registerFeedItem_NC0(shortcd)
                    self.registerFeedItem_NH0(shortcd)
                    self.registerFeedItem_YFC(shortcd)

                for shortcd in self._FeedCodeList.optionshortcdlst:
                    self.registerFeedItem_EC0(shortcd)
                    self.registerFeedItem_EH0(shortcd)
                    self.registerFeedItem_YOC(shortcd)

            for shortcd in self._FeedCodeList.equityshortcdlst:
                self.registerFeedItem_S3_(shortcd)
                self.registerFeedItem_YS3(shortcd)
                self.registerFeedItem_I5_(shortcd)


        if self._CpCybos.IsConnect() and boolToggle:
            nowlocaltime = time.localtime()
            for shortcd in self._FeedCodeList.futureshortcdlst:
                if nowlocaltime.tm_hour >= 6 and nowlocaltime.tm_hour < 16:
                    self.registerFeedItem_FutureJpBid(shortcd)
                else:
                    self.registerFeedItem_CMECurr(shortcd)
                self.registerFeedItem_FOExpect(shortcd)

            self.initOptionJpBid()
            self.initFOExpect()
            if nowlocaltime.tm_hour >= 6 and nowlocaltime.tm_hour < 16:
                for shortcd in self._FeedCodeList.optionshortcdlst:
                    self.registerFeedItem_OptionJpBid(shortcd)
                    self.registerFeedItem_FOExpect(shortcd)


            for shortcd in self._FeedCodeList.equityshortcdlst:
                self.registerFeedItem_StockJpBid(shortcd)

            for shortcd in self._FeedCodeList.indexshortcdlst:
                self.registerFeedItem_ExpectIndexS(shortcd)

        if boolToggle:
            pythoncom.PumpMessages()
        else:
            ctypes.windll.user32.PostQuitMessage(0)

        pass


    def slot_RequestPrevClosePrice(self):
        if self._CpCybos.IsConnect():
            filep = open(self.filepath + '\\' + self.filename,'w+')
            msglist = []
            for shortcd in self._FeedCodeList.futureshortcdlst:
                _FutureMst = pc.FutureMst(shortcd[:-3])
                _FutureMst.Request()
                while 1:
                    pythoncom.PumpWaitingMessages()
                    if _FutureMst.data:
                        print shortcd
                        print _FutureMst.data[22]
                        msglist.append(str(_FutureMst.data[22]))
                        break

            for shortcd in self._FeedCodeList.optionshortcdlst:
                _OptionMst = pc.OptionMst(shortcd)
                _OptionMst.Request()
                while 1:
                    pythoncom.PumpWaitingMessages()
                    if _OptionMst.data:
                        print shortcd
                        print round(_OptionMst.data[27],2)
                        break


            strshortcdlist = 'A' + ',A'.join(self._FeedCodeList.equityshortcdlst)
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
            #print("Row %d and Column %d was doblueclicked" % (row,column))
            myform = LoginForm(XASession=proxy(self.XASession))
            myform.show()
            myform.exec_()
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
        #print 'connect server'
        ret = self.XASession.Login(user,password,certpw,servertype,showcerterror)
                
        px.XASessionEvents.session = self.XASession
        self.XASession.flag = True
        while self.XASession.flag:
            pythoncom.PumpWaitingMessages()
            
        self.xingtimer.start(1000)
        pass

    def slot_CheckCybosStarter(self,row,column):
        if row == 0 and column == 2:
            self._CpCybos = pc.CpCybos()
            self.status_cy.setText('connect')
            self.cybostimer.start(1000)

    def NotifyMsg(self,msg):
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
        msg = timestamp + msg
        #self.ui.plainTextEditMsg.appendPlainText(msg)

    def CtimerUpdate(self):
        self.lbltime.setText(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))

    def CybosTimerUpdate(self):
        if self._CpCybos.IsConnect():
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
    def __init__(self,status_xi=None):
        self.status_xi = status_xi
    def Update(self,subject):
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
    myappid = 'zerofeeder'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
#    if myform.setAuto:
#        myform.ui.actionFeed.setChecked(True)
    app.exec_()

