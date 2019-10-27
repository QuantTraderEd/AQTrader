# -*- coding: utf-8 -*-

from __future__ import print_function

import time
import zmq
import logging
import pythoncom

from weakref import proxy

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QAxContainer

import pyxing as px
import pycybos as pc
import pykiwoom as pk
from commutil.FeedCodeList import FeedCodeList
from datafeeder_ui import Ui_MainWindow
from DataFeeder.xinglogindlg.xinglogindlg import LoginForm
from ZMQTickSender import ZMQTickSender_New

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


class XingXASessionUpdate():
    def __init__(self, status_xi=None):
        self.status_xi = status_xi

    def update(self, subject):
        msg = ''
        for item in subject.data:
            msg = msg + ' ' + item
        if msg[:5] == ' 0000':
            self.status_xi.setText('connect:' + msg[:5])
        pass


class CpCybosNULL():
    def IsConnect(self):
        return False


class MainForm(QtGui.QMainWindow):

    def __init__(self):
        super(MainForm, self).__init__()
        # self.port = 5501  # Real: 5501, RealTest 5502, BackTest 5503
        # self.set_auto = False
        # self.auto_config = self.set_auto_config()

        self.init_ui()
        self.init_timer()
        self.init_api()
        # self.init_feedcode()
        # self.init_taq_feederlist()
        # self.init_zmq()
        #
        # self.exchange_code = 'KRX'
        # self.filename = 'prevclose.txt'
        #
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
        #
        # setting = QtCore.QSettings("ZeroFeeder.ini", QtCore.QSettings.IniFormat)
        # value = setting.value("geometry")
        # if value:
        #     self.restoreGeometry(setting.value("geometry").toByteArray())
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

    def on_event_connect(self, errcode):
        print("ErrCode: %d" % errcode)
        pass

    def on_receive_msg(self, scrno, rqname, trcode, msg):
        print(scrno, rqname, trcode, msg)
        pass

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


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    app.exec_()
