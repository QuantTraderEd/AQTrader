# -*- coding: utf-8 -*-

import os
import time
import zmq
import json
import logging
import pythoncom

import ctypes
from PyQt4 import QtCore
from PyQt4 import QtGui

from commutil.comm_function import  read_config
from commutil.FeedCodeList import FeedCodeList
import pyxing as px
import pycybos as pc
from ui_zerofeeder import Ui_MainWindow
from xinglogindlg import LoginForm
from ZMQTickSender import ZMQTickSender_New

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
    def Update(self, subject):
        for i in xrange(len(subject.data)):
            print subject.data[i],
        print


class MainForm(QtGui.QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.port = 5501  # Real: 5501, RealTest 5502, BackTest 5503
        self.set_auto = False
        self.auto_config = self.set_auto_config()

        self.init_ui()
        self.init_timer()
        self.init_api()
        self.init_feedcode()
        self.init_taq_feederlist()
        self.init_zmq()

        self.exchange_code = 'KRX'
        self.filename = 'prevclose.txt'

        if self.set_auto:
            self.slot_CheckCybosStarter(0, 2)
            self.auto_start_xing(self.auto_config)

    def set_auto_config(self):
        setting = QtCore.QSettings("ZeroFeeder.ini", QtCore.QSettings.IniFormat)
        self.set_auto = setting.value("setauto", type=bool)
        if setting.value("port", type=int) != 0:
            self.port = setting.value("port", type=int)
        comm_config = read_config()
        auto_config = dict()
        auto_config['id'] = comm_config.get('ebest_id', '')
        auto_config['pwd'] = comm_config.get('ebest_pw', '')
        auto_config['cetpwd'] = comm_config.get('ebest_cetpwd', '')
        auto_config['servertype'] = comm_config.get('ebest_servertype', 1)
        if self.set_auto:
            logger.info("setauto: True")
        else:
            logger.info("setauto: False")
        logger.info("zmq port: %d" % self.port)
        print auto_config
        return auto_config

    def closeEvent(self, event):
        self.XASession.DisconnectServer()
        ctypes.windll.user32.PostQuitMessage(0)
        setting = QtCore.QSettings("ZeroFeeder.ini", QtCore.QSettings.IniFormat)
        setting.setValue("geometry", self.saveGeometry())
        setting.setValue("setauto", self.set_auto)
        setting.setValue("port", self.port)
        logger.info("Close DataFeeder")
        super(MainForm, self).closeEvent(event)

    def init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QtGui.qApp.setStyle('Cleanlooks')
        self.conn_cy = QtGui.QTableWidgetItem("conn cy")
        self.conn_xi = QtGui.QTableWidgetItem("conn xi")
        self.status_xi = QtGui.QTableWidgetItem("ready")
        self.status_cy = QtGui.QTableWidgetItem("ready")
        self.ui.tableWidget.setItem(0, 2, self.conn_cy)
        self.ui.tableWidget.setItem(1, 2, self.conn_xi)
        self.ui.tableWidget.setItem(0, 1, self.status_cy)
        self.ui.tableWidget.setItem(1, 1, self.status_xi)
        # self.ui.tableWidget.cellClicked.connect(self.cell_was_clicked)

        setting = QtCore.QSettings("ZeroFeeder.ini", QtCore.QSettings.IniFormat)
        value = setting.value("geometry")
        if value:
            self.restoreGeometry(setting.value("geometry").toByteArray())
        pass

    def init_timer(self):
        self.ctimer = QtCore.QTimer()
        self.ctimer.start(1000)
        self.ctimer.timeout.connect(self.ctimer_update)
        self.cybostimer = QtCore.QTimer()
        self.cybostimer.timeout.connect(self.cybos_timer_update)
        self.xingtimer = QtCore.QTimer()
        self.xingtimer.timeout.connect(self.xing_timer_update)
        self.autotimer = QtCore.QTimer()
        self.autotimer.start(20000)
        self.autotimer.timeout.connect(self.autotimer_update)
        self.lbltime = QtGui.QLabel(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.statusBar().addPermanentWidget(self.lbltime)

    def init_api(self):
        self.XASession_observer = XingXASessionUpdate(proxy(self.status_xi))
        self.XASession = px.XASession()
        self.XASession.Attach(self.XASession_observer)
        self.cpcybos = CpCybosNULL()

    def init_feedcode(self):
        self._FeedCodeList = FeedCodeList()
        self._FeedCodeList.read_code_list()

    def init_zmq(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://127.0.0.1:%d" % self.port)

    def init_zmqsender(self):
        self.ZMQFuturesExpectSender_xing = ZMQTickSender_New(self.socket, 'xing', 'E', 'futures')
        self.ZMQOptionsExpectSender_xing = ZMQTickSender_New(self.socket, 'xing', 'E', 'options')
        self.obs = ConsoleObserver()

    def init_taq_feederlist(self):
        self.FutureTAQFeederDict = dict()
        self.OptionTAQFeederDict = dict()
        self.EquityTAQFeederLst = list()

    # ======= init futures =======

    def initFC0(self):
        newitemtrade_new = px.XAReal_FC0(datatype='dictionary')
        zmqsender = ZMQTickSender_New(self.socket, 'xing', 'T', 'futures')
        newitemtrade_new.Attach(zmqsender)
        self.FutureTAQFeederDict['FC0'] = newitemtrade_new

    def initFH0(self):
        newitemtrade_new = px.XAReal_FH0(datatype='dictionary')
        zmqsender = ZMQTickSender_New(self.socket, 'xing', 'Q', 'futures')
        newitemtrade_new.Attach(zmqsender)
        self.FutureTAQFeederDict['FH0'] = newitemtrade_new

    def initNC0(self):
        newitemtrade_new = px.XAReal_NC0(datatype='dictionary')
        zmqsender = ZMQTickSender_New(self.socket, 'xing', 'T', 'futures')
        newitemtrade_new.Attach(zmqsender)
        self.FutureTAQFeederDict['NC0'] = newitemtrade_new

    def initNH0(self):
        newitemtrade_new = px.XAReal_NH0(datatype='dictionary')
        zmqsender = ZMQTickSender_New(self.socket, 'xing', 'Q', 'futures')
        newitemtrade_new.Attach(zmqsender)
        self.FutureTAQFeederDict['NH0'] = newitemtrade_new

    def initEC0_MINI(self):
        newitemtrade_new = px.XAReal_EC0(DataType='dictionary')
        zmqsender = ZMQTickSender_New(self.socket, 'xing', 'T', 'futures')
        newitemtrade_new.Attach(zmqsender)
        self.OptionTAQFeederDict['EC0_MINI'] = newitemtrade_new

    def initEH0_MINI(self):
        newitemquote_new = px.XAReal_EH0(DataType='dictionary')
        zmqsender = ZMQTickSender_New(self.socket, 'xing', 'Q', 'futures')
        newitemquote_new.Attach(zmqsender)
        self.OptionTAQFeederDict['EH0_MINI'] = newitemquote_new

    def initYFC(self):
        newitemfuture_aution_new = px.XAReal_YFC(DataType='dictionary')
        newitemfuture_aution_new.Attach(self.ZMQFuturesExpectSender_xing)
        self.FutureTAQFeederDict['YFC'] = newitemfuture_aution_new

    # ======= init options =======

    def initOptionCur(self):
        newitem_trade = pc.OptionCurOnly()
        self.OptionTAQFeederDict['OptionCur'] = newitem_trade

    def initOptionJpBid(self):
        newitemquote = pc.OptionJpBid()
        # newitemquote.Attach(self.ZMQOptionsQuoteSender)
        self.OptionTAQFeederDict['OptionJpBid'] = newitemquote

    def initOC0(self):
        newitemtrade_new = px.XAReal_OC0(DataType='dictionary')
        zmqsender = ZMQTickSender_New(self.socket, 'xing', 'T', 'options')
        newitemtrade_new.Attach(zmqsender)
        self.OptionTAQFeederDict['OC0_New'] = newitemtrade_new
            
    def initOH0(self):
        newitemquote_new = px.XAReal_OH0(DataType='dictionary')
        zmqsender = ZMQTickSender_New(self.socket, 'xing', 'Q', 'options')
        newitemquote_new.Attach(zmqsender)
        self.OptionTAQFeederDict['OH0_New'] = newitemquote_new
            
    def initEC0(self):
        newitemtrade_new = px.XAReal_EC0(DataType='dictionary')
        zmqsender = ZMQTickSender_New(self.socket, 'xing', 'T', 'options')
        newitemtrade_new.Attach(zmqsender)
        self.OptionTAQFeederDict['EC0_New'] = newitemtrade_new

    def initEH0(self):
        newitemquote_new = px.XAReal_EH0(DataType='dictionary')
        zmqsender = ZMQTickSender_New(self.socket, 'xing', 'Q', 'options')
        newitemquote_new.Attach(zmqsender)
        self.OptionTAQFeederDict['EH0_New'] = newitemquote_new
            
    def initYOC(self):
        newitemoption_aution_new = px.XAReal_YOC(DataType='dictionary')        
        newitemoption_aution_new.Attach(self.ZMQOptionsExpectSender_xing)
        self.OptionTAQFeederDict['YOC'] = newitemoption_aution_new

    def initFOExpect_Future(self):
        newitemoption_futures_aution = pc.FOExpectCur()
        zmq_sender = ZMQTickSender_New(self.socket, 'cybos', 'E', 'futures')
        newitemoption_futures_aution.Attach(zmq_sender)
        self.FutureTAQFeederDict['FutureExpect'] = newitemoption_futures_aution

    def initFOExpect_Option(self):
        newitemoption_options_aution = pc.FOExpectCur()
        zmq_sender = ZMQTickSender_New(self.socket, 'cybos', 'E', 'options')
        newitemoption_options_aution.Attach(zmq_sender)
        self.OptionTAQFeederDict['OptionExpect'] = newitemoption_options_aution

    # ======= regist futures =======

    def regist_FeedItem_FutureJpBid(self, shortcd):
        newitemquote = pc.FutureJpBid(shortcd[:-3])
        # newitemquote.Attach(self.ZMQFuturesQuoteSender)
        # newitemquote.Subscribe()
        # self.FutureTAQFeederLst.append(newitemquote)

    def regist_FeedItem_FC0(self, shortcd):
        self.FutureTAQFeederDict['FC0'].SetFieldData('InBlock', 'futcode', shortcd)
        self.FutureTAQFeederDict['FC0'].AdviseRealData()

    def regist_FeedItem_FH0(self, shortcd):
        self.FutureTAQFeederDict['FH0'].SetFieldData('InBlock', 'futcode', shortcd)
        self.FutureTAQFeederDict['FH0'].AdviseRealData()

    def regist_FeedItem_CMECurr(self, shortcd):
        newitemquote = pc.CmeCurr(shortcd[:-3])
        # newitemquote.Attach(self.ZMQFuturesQuoteSender)
        # newitemquote.Subscribe()
        # self.FutureTAQFeederLst.append(newitemquote)

    def regist_FeedItem_NC0(self, shortcd):
        self.FutureTAQFeederDict['NC0'].SetFieldData('InBlock', 'futcode', shortcd)
        self.FutureTAQFeederDict['NC0'].AdviseRealData()

    def regist_FeedItem_NH0(self, shortcd):
        self.FutureTAQFeederDict['NH0'].SetFieldData('InBlock', 'futcode', shortcd)
        self.FutureTAQFeederDict['NH0'].AdviseRealData()

    def regist_FeedItem_YFC(self, shortcd):
        self.FutureTAQFeederDict['YFC'].SetFieldData('InBlock', 'futcode', shortcd)
        self.FutureTAQFeederDict['YFC'].AdviseRealData()

    # ======= regist options =======
    def regist_FeedItem_OptionCur(self, shortcd):
        self.OptionTAQFeederDict['OptionCur'].Subscribe('0', shortcd)

    def regist_FeedItem_OptionJpBid(self, shortcd):
        self.OptionTAQFeederDict['OptionJpBid'].Subscribe('0', shortcd)

    def regist_FeedItem_OC0(self, shortcd):
        self.OptionTAQFeederDict['OC0_New'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['OC0_New'].AdviseRealData()

    def regist_FeedItem_OH0(self, shortcd):
        self.OptionTAQFeederDict['OH0_New'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['OH0_New'].AdviseRealData()

    def regist_FeedItem_EC0(self, shortcd):
        if shortcd[:3] == '105':
            self.OptionTAQFeederDict['EC0_MINI'].SetFieldData('InBlock', 'optcode', shortcd)
            self.OptionTAQFeederDict['EC0_MINI'].AdviseRealData()
        else:
            self.OptionTAQFeederDict['EC0_New'].SetFieldData('InBlock', 'optcode', shortcd)
            self.OptionTAQFeederDict['EC0_New'].AdviseRealData()

    def regist_FeedItem_EH0(self, shortcd):
        if shortcd[:3] == '105':
            self.OptionTAQFeederDict['EH0_MINI'].SetFieldData('InBlock', 'optcode', shortcd)
            self.OptionTAQFeederDict['EH0_MINI'].AdviseRealData()
        else:
            self.OptionTAQFeederDict['EH0_New'].SetFieldData('InBlock', 'optcode', shortcd)
            self.OptionTAQFeederDict['EH0_New'].AdviseRealData()
        
    def regist_FeedItem_YOC(self, shortcd):
        self.OptionTAQFeederDict['YOC'].SetFieldData('InBlock', 'optcode', shortcd)
        self.OptionTAQFeederDict['YOC'].AdviseRealData()

    def registerFeedItem_FOExpect(self, shortcd):
        if shortcd[:3] in ['101', '105']:
            self.FutureTAQFeederDict['FutureExpect'].SetInputValue(0, shortcd[:-3])
            self.FutureTAQFeederDict['FutureExpect'].SetInputValue(1, 'F1')
            self.FutureTAQFeederDict['FutureExpect'].SetInputValue(2, shortcd[3:-3])
            self.FutureTAQFeederDict['FutureExpect'].Subscribe()
        elif shortcd[:3] == '201' or shortcd[:3] == '301':
            self.OptionTAQFeederDict['OptionExpect'].SetInputValue(0, shortcd)
            self.OptionTAQFeederDict['OptionExpect'].SetInputValue(1, 'O1')
            self.OptionTAQFeederDict['OptionExpect'].SetInputValue(2, shortcd[3:-3])
            self.OptionTAQFeederDict['OptionExpect'].Subscribe()

    # ======= regist stock =======

    def registerFeedItem_StockJpBid(self, shortcd):
        newitemquote = pc.StockJpBid('A' + shortcd)
        # newitemquote.Attach(self.ZMQEquityQuoteSender)
        # newitemquote.Subscribe()
        # self.EquityTAQFeederLst.append(newitemquote)

    def registerFeedItem_S3_(self, shortcd):
        newitemtrade = px.XAReal_S3_(shortcd, 'list')
        # newitemtrade.Attach(self.ZMQEquityTradeSender)
        # newitemtrade.AdviseRealData()
        # self.EquityTAQFeederLst.append(newitemtrade)

    def registerFeedItem_YS3(self, shortcd):
        newitem_aution = px.XAReal_YS3(shortcd, 'list')
        # newitem_aution.Attach(self.ZMQEquityExpectSender)
        # newitem_aution.AdviseRealData()
        # self.EquityTAQFeederLst.append(newitem_aution)

    def registerFeedItem_I5_(self, shortcd):
        NewItemNAV = px.XAReal_I5_(shortcd, 'list')
        # NewItemNAV.Attach(self.ZMQETFNAVSender)
        # NewItemNAV.AdviseRealData()
        # self.EquityTAQFeederLst.append(NewItemNAV)

    def registerFeedItem_ExpectIndexS(self, shortcd):
        newitem_index_expect = pc.ExpectIndexS(shortcd)
        # newitem_index_expect.Attach(self.ZMQIndexExpectSender)
        # newitem_index_expect.Subscribe()
        # self.EquityTAQFeederLst.append(newitem_index_expect)

    def slot_ToggleFeed(self, boolToggle):
        if boolToggle:
            # self.slot_RequestPrevClosePrice()
            pythoncom.CoInitialize()
            self.init_feedcode()
            self.init_zmqsender()
            self.init_taq_feederlist()
            logger.info('set feed code & zmq')
        else:
            logger.info('toggle off')
            logger.info('tick count: %d' % ZMQTickSender_New.count)
            ZMQTickSender_New.count = 0
            return

        nowlocaltime = time.localtime()
        if nowlocaltime.tm_hour >= 7 and nowlocaltime.tm_hour < 17:
            self.exchange_code = 'KRX'
        else:
            self.exchange_code = 'EUREX'

        if self.XASession.IsConnected() and boolToggle:
            logger.info('regist feed data @ xing')
            if nowlocaltime.tm_hour >= 7 and nowlocaltime.tm_hour < 17:
                self.initFC0()
                self.initFH0()
                self.initYFC()
                for shortcd in self._FeedCodeList.future_shortcd_list:
                    self.regist_FeedItem_FC0(shortcd)
                    self.regist_FeedItem_FH0(shortcd)
                    self.regist_FeedItem_YFC(shortcd)
            else:
                self.initNC0()
                self.initNH0()
                self.initEC0_MINI()
                self.initEH0_MINI()
                for shortcd in self._FeedCodeList.future_shortcd_list:
                    self.regist_FeedItem_NC0(shortcd)
                    self.regist_FeedItem_NH0(shortcd)
                    if shortcd[:3] == '105':
                        self.regist_FeedItem_EC0(shortcd)
                        self.regist_FeedItem_EH0(shortcd)

            if nowlocaltime.tm_hour >= 7 and nowlocaltime.tm_hour < 17:
                self.initOC0()
                self.initOH0()
                self.initYOC()
                for shortcd in self._FeedCodeList.option_shortcd_list:
                    self.regist_FeedItem_OC0(shortcd)
                    self.regist_FeedItem_OH0(shortcd)
                    self.regist_FeedItem_YOC(shortcd)
            else:
                self.initEC0()
                self.initEH0()
                for shortcd in self._FeedCodeList.option_shortcd_list:
                    self.regist_FeedItem_EC0(shortcd)
                    self.regist_FeedItem_EH0(shortcd)

            for shortcd in self._FeedCodeList.equity_shortcd_list:
                self.registerFeedItem_S3_(shortcd)
                self.registerFeedItem_YS3(shortcd)
                self.registerFeedItem_I5_(shortcd)

        if self.cpcybos.IsConnect() and boolToggle:
            logger.info('regist feed data @ cybos')
            if nowlocaltime.tm_hour >= 7 and nowlocaltime.tm_hour < 17:
                self.initFOExpect_Future()
                for shortcd in self._FeedCodeList.future_shortcd_list:
                    self.regist_FeedItem_FutureJpBid(shortcd)
                    self.registerFeedItem_FOExpect(shortcd)
            else:
                for shortcd in self._FeedCodeList.future_shortcd_list:
                    self.regist_FeedItem_CMECurr(shortcd)

            if nowlocaltime.tm_hour >= 7 and nowlocaltime.tm_hour < 17:
                self.initOptionCur()
                self.initOptionJpBid()
                self.initFOExpect_Option()
                for shortcd in self._FeedCodeList.option_shortcd_list:
                    self.regist_FeedItem_OptionJpBid(shortcd)
                    self.registerFeedItem_FOExpect(shortcd)

            # for shortcd in self._FeedCodeList.equity_shortcd_list:
            #     self.registerFeedItem_StockJpBid(shortcd)
            #
            # for shortcd in self._FeedCodeList.index_shortcd_list:
            #     self.registerFeedItem_ExpectIndexS(shortcd)

        if boolToggle:
            logger.info('start pumping msg')
            pythoncom.PumpMessages()
        pass

    def slot_request_prev_close(self):
        if self.cpcybos.IsConnect():
            filep = open(self.filename, 'w+')
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

    def slot_StartXingDlg(self, row, column):
        if row == 1 and column == 2:
            # print("Row %d and Column %d was doblueclicked" % (row,column))
            local_login_form = LoginForm(XASession=proxy(self.XASession))
            local_login_form.show()
            local_login_form.exec_()
            self.xingtimer.start(1000)
            
    def auto_start_xing(self, auto_config):
        server = 'hts.ebestsec.co.kr'
        port = 20001
        servertype = 0
        showcerterror = 1
        user = str(auto_config['id'])
        password = str(auto_config['pwd'].decode('hex'))
        certpw = str(auto_config['cetpwd'].decode('hex'))
        servertype = int(auto_config['servertype'])
        if servertype == 1:
            server = 'demo.ebestsec.co.kr'
        elif servertype == 0:
            server = 'hts.ebestsec.co.kr'
        
        self.XASession.ConnectServer(server, port)
        # print 'connect server'
        ret = self.XASession.Login(user, password, certpw, servertype, showcerterror)
                
        px.XASessionEvents.session = proxy(self.XASession)
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

    def ctimer_update(self):
        now_time = time.localtime()
        self.lbltime.setText(time.strftime("%Y-%m-%d %H:%M:%S", now_time))

    def cybos_timer_update(self):
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

    def xing_timer_update(self):
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

    def autotimer_update(self):
        now_time = time.localtime()
        close_hour = 6
        close_minute = 5
        re_toggle_hour = 17
        re_toggle_minute = 5
        if now_time.tm_hour == close_hour and now_time.tm_min == close_minute and self.set_auto:
            logger.info("auto trigger-off")
            self.slot_ToggleFeed(False)
            if self.cpcybos.IsConnect():
                self.cpcybos.PlusDisconnect()
            self.close()
        elif now_time.tm_hour == re_toggle_hour and now_time.tm_min == re_toggle_minute and self.set_auto:
            if self.exchange_code == 'KRX':
                logger.info('auto toggle feed from KRX to EUREX')
                self.slot_ToggleFeed(False)
                self.slot_ToggleFeed(True)


class XingXASessionUpdate():
    def __init__(self, status_xi=None):
        self.status_xi = status_xi

    def Update(self, subject):
        msg = ''
        for item in subject.data:
            msg = msg + ' ' + item
        if msg[:5] == ' 0000':
            self.status_xi.setText('connect:' + msg[:5])
        pass


class CpCybosNULL():
    def IsConnect(self):
        return False


if __name__ == '__main__':
    import sys
    # import ctypes
    # myappid = 'zerofeeder'
    # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    if myform.set_auto:
        logger.info('set_auto: True')
        myform.ui.actionFeed.setChecked(True)
        myform.slot_ToggleFeed(True)
    app.exec_()
