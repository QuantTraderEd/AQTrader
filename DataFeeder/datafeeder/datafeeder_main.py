# -*- coding: utf-8 -*-

from __future__ import print_function

import time
import zmq
import logging
import pythoncom

from weakref import proxy
from logging.handlers import RotatingFileHandler

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QAxContainer

import pyxing as px
import pycybos as pc
import pykiwoom as pk
from commutil.FeedCodeList import FeedCodeList
from datafeeder_ui import Ui_MainWindow
from commutil.xinglogindlg.xinglogindlg_main import LoginForm  # FIXME: package path issue
from ZMQTickSender import ZMQTickSender_New

logger = logging.getLogger('DataFeeder')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('DataFeeder.log')
fh = RotatingFileHandler('DataFeeder.log', maxBytes=104857, backupCount=3)
fh.setLevel(logging.INFO)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)


class XingXASessionUpdate:
    def __init__(self, status_xi=None):
        self.status_xi = status_xi

    def update(self, subject):
        msg = ''
        for item in subject.data:
            msg = msg + ' ' + item
        if msg[:5] == ' 0000':
            self.status_xi.setText('connect:' + msg[:5])
        pass


class CpCybosNULL:
    def IsConnect(self):
        return False


class ConsoleObserver:
    def Update(self, subject):
        for i in xrange(len(subject.data)):
            print(subject.data[i],)
        print()


class MainForm(QtGui.QMainWindow):

    def __init__(self):
        super(MainForm, self).__init__()
        self.port = 5501  # Real: 5501, RealTest 5502, BackTest 5503
        self.set_auto = False
        # self.auto_config = self.set_auto_config()

        self.init_ui()
        self.init_timer()
        self.init_api()
        self.init_feedcode()
        self.init_taq_feederlist()
        self.init_zmq()

        self.exchange_code = 'KRX'

        # if self.set_auto:
        #     self.slot_CheckCybosStarter(0, 2)
        #     self.auto_start_xing(self.auto_config)

    def init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QtGui.qApp.setStyle('Cleanlooks')
        self.login_cybos = QtGui.QTableWidgetItem("login_cybos")
        self.login_xing = QtGui.QTableWidgetItem("login_xing")
        self.login_kiwoom = QtGui.QTableWidgetItem("login_kiwoom")
        self.status_cy = QtGui.QTableWidgetItem("ready")
        self.status_xi = QtGui.QTableWidgetItem("ready")
        self.status_ki = QtGui.QTableWidgetItem("ready")
        self.ui.tableWidget.setItem(0, 2, self.login_cybos)
        self.ui.tableWidget.setItem(1, 2, self.login_xing)
        self.ui.tableWidget.setItem(2, 2, self.login_kiwoom)
        self.ui.tableWidget.setItem(0, 1, self.status_cy)
        self.ui.tableWidget.setItem(1, 1, self.status_xi)
        self.ui.tableWidget.setItem(2, 1, self.status_ki)
        self.ui.tableWidget.cellDoubleClicked.connect(self.cell_was_dobuleclicked)
        self.ui.actionFeed.triggered.connect(self.slot_togglefeed)
        pass

    def init_timer(self):
        self.ctimer = QtCore.QTimer()
        self.ctimer.start(1000)
        self.ctimer.timeout.connect(self.ctimer_update)
        self.cybostimer = QtCore.QTimer()
        self.cybostimer.timeout.connect(self.cybos_timer_update)
        self.xingtimer = QtCore.QTimer()
        self.xingtimer.timeout.connect(self.xing_timer_update)
        self.kiwoomtimer = QtCore.QTimer()
        self.kiwoomtimer.timeout.connect(self.kiwoom_timer_update)
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
        self.kiwoom_session = pk.KiwoomSession()
        self.ocx = QAxContainer.QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.on_event_connect)
        self.ocx.OnReceiveMsg.connect(self.on_receive_msg)

    def init_feedcode(self):
        self.feedcode_list = FeedCodeList()
        self.feedcode_list.read_code_list()

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

    def on_event_connect(self, errcode):
        print("ErrCode: %d" % errcode)
        pass

    def on_receive_msg(self, scrno, rqname, trcode, msg):
        print(scrno, rqname, trcode, msg)
        pass

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

    def init_kiwoom_futures_tradetick(self):
        real_futurestradetick = pk.KiwoomFuturesTradeTick(kiwoom_session=self.kiwoom_session)
        zmqsender = ZMQTickSender_New(self.socket, 'kiwoom', 'T', 'futures')
        real_futurestradetick.attach(zmqsender)
        self.FutureTAQFeederDict['real_futurestradetick'] = real_futurestradetick

    def init_kiwoom_futures_quotetick(self):
        real_futuresquotetick = pk.KiwoomFuturesQuoteTick(kiwoom_session=self.kiwoom_session)
        zmqsender = ZMQTickSender_New(self.socket, 'kiwoom', 'Q', 'futures')
        real_futuresquotetick.attach(zmqsender)
        self.FutureTAQFeederDict['real_futuresquotetick'] = real_futuresquotetick

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

    def regist_feeditem_kiwoom_futurestradetick(self, shortcd):
        screen_no = u"0001"
        code_list = shortcd
        fid_list = u"9001;20;10;15;13;195"
        opt_type = u"1"
        self.FutureTAQFeederDict['real_futurestradetick'].set_real_reg(screen_no, code_list, fid_list, opt_type)

    def regist_feeditem_kiwoom_futuresquotetick(self, shortcd):
        screen_no = u"0002"
        code_list = shortcd
        fid_list = u"9001;20;10;15;13;195"  # quote 항목에 맞게 수정 필
        opt_type = u"1"
        self.FutureTAQFeederDict['real_futuresquotetick'].set_real_reg(screen_no, code_list, fid_list, opt_type)

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

    def regist_FeedItem_FOExpect(self, shortcd):
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

    def kiwoom_timer_update(self):
        if self.kiwoom_session.get_connect_state() != 0:
            if self.status_ki.text() == 'connect':
                self.status_ki.setText('connect.')
            elif self.status_ki.text() == 'connect.':
                self.status_ki.setText('connect..')
            elif self.status_ki.text() == 'connect..':
                self.status_ki.setText('connect...')
            elif self.status_ki.text() == 'connect...':
                self.status_ki.setText('connect')
        else:
            self.status_ki.setText('disconnect')

    def autotimer_update(self):
        now_time = time.localtime()
        close_trigger = False
        close_hour = 6
        close_minute = 5
        re_toggle_hour = 17
        re_toggle_minute = 5
        if now_time.tm_hour == close_hour and now_time.tm_min == close_minute and self.set_auto:
            if self.cpcybos.IsConnect():
                self.cpcybos.PlusDisconnect()
            close_trigger = True
        elif now_time.tm_hour == re_toggle_hour and now_time.tm_min == re_toggle_minute and self.set_auto:
            if self.exchange_code == 'KRX':
                logger.info('auto toggle feed from KRX to EUREX')
                self.slot_ToggleFeed(False)
                self.slot_ToggleFeed(True)

        if close_trigger:
            logger.info("close trigger")
            self.slot_ToggleFeed(False)
            self.close()

    def cell_was_dobuleclicked(self, row, column):
        if row == 0 and column == 2:
            self.check_cybosplus()
        elif row == 1 and column == 2:
            self.start_xinglogindlg()
        elif row == 2 and column == 2:
            self.start_kiwoomlogin()

    def start_xinglogindlg(self):
        local_login_form = LoginForm(XASession=proxy(self.XASession))
        local_login_form.show()
        local_login_form.exec_()
        self.xingtimer.start(1000)

    def auto_start_xinglogin(self, auto_config):
        server = 'hts.ebestsec.co.kr'
        port = 20001
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

    def check_cybosplus(self):
        self.cpcybos = pc.CpCybos()
        if self.cpcybos.IsConnect():
            self.status_cy.setText('connect')
        else:
            self.status_cy.setText('disconnect')
        self.cybostimer.start(1000)

    def start_kiwoomlogin(self):
        self.kiwoom_session.comm_connect()
        if self.kiwoom_session.get_connect_state() != 0:
            self.status_ki.setText('connect')
        else:
            self.status_ki.setText('disconnect')
        self.kiwoomtimer.start(1000)

    def slot_togglefeed(self, bool_toggle):
        if bool_toggle:
            # self.slot_RequestPrevClosePrice()
            pythoncom.CoInitialize()
            self.init_feedcode()
            self.init_zmqsender()
            self.init_taq_feederlist()
            logger.info('toggle on')
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

        if self.XASession.IsConnected() and bool_toggle:
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

        if self.cpcybos.IsConnect() and bool_toggle:
            logger.info('regist feed data @ cybos')
            if nowlocaltime.tm_hour >= 7 and nowlocaltime.tm_hour < 17:
                self.initFOExpect_Future()
                for shortcd in self.feedcode_list.future_shortcd_list:
                    self.regist_FeedItem_FutureJpBid(shortcd)
                    self.regist_FeedItem_FOExpect(shortcd)
            else:
                for shortcd in self.feedcode_list.future_shortcd_list:
                    self.regist_FeedItem_CMECurr(shortcd)

            if nowlocaltime.tm_hour >= 7 and nowlocaltime.tm_hour < 17:
                self.initOptionCur()
                self.initOptionJpBid()
                self.initFOExpect_Option()
                for shortcd in self.feedcode_list.option_shortcd_list:
                    self.regist_FeedItem_OptionJpBid(shortcd)
                    self.regist_FeedItem_FOExpect(shortcd)

        if self.kiwoom_session.get_connect_state() != 0 and bool_toggle:
            logger.info('regist feed data @ kiwoom')
            if nowlocaltime.tm_hour >= 7 and nowlocaltime.tm_hour < 17:
                self.init_kiwoom_futures_tradetick()
                self.init_kiwoom_futures_quotetick()
                for shortcd in self.feedcode_list.future_shortcd_list:
                    self.regist_feeditem_kiwoom_futurestradetick(shortcd)
                    self.regist_feeditem_kiwoom_futuresquotetick(shortcd)

        if bool_toggle:
            logger.info('start pumping msg')
            pythoncom.PumpWaitingMessages()
        pass


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    app.exec_()
