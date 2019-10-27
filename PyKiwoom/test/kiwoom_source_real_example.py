# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import zmq
from PyQt4 import QtGui
from PyQt4 import QAxContainer
from PyKiwoom.pykiwoom.kiwoom_source import KiwoomSession
from PyKiwoom.pykiwoom.kiwoom_real_futures_tradetick import KiwoomFuturesTradeTick
from PyKiwoom.pykiwoom.kiwoom_real_options_tradetick import KiwoomOptionsTradeTick
from PyKiwoom.pykiwoom.kiwoom_real_futures_quotetick import KiwoomFuturesQuoteTick
from PyKiwoom.pykiwoom.kiwoom_real_options_quotetick import KiwoomOptionsQuoteTick
from DataFeeder.datafeeder.ZMQTickSender import ZMQTickSender_New


class ConsoleObserver:
    def update(self, subject):
        print("===== console observer ====")
        for key in subject.data:
            print(key, subject.data[key], )
        print()


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("KiwoomLoginTest")
        self.setGeometry(300, 300, 300, 150)

        self.port = 5501
        self.init_zmq()

        self.ocx = QAxContainer.QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.on_event_connect)
        self.ocx.OnReceiveMsg.connect(self.on_receive_msg)

        self.kiwoom_session = KiwoomSession()
        self.real_futures_tradetick = KiwoomFuturesTradeTick(kiwoom_session=self.kiwoom_session)
        self.real_options_tradetick = KiwoomOptionsTradeTick(kiwoom_session=self.kiwoom_session)
        self.real_futures_quotetick = KiwoomFuturesQuoteTick(kiwoom_session=self.kiwoom_session)
        self.real_options_quotetick = KiwoomOptionsQuoteTick(kiwoom_session=self.kiwoom_session)

        console_obs = ConsoleObserver()
        self.real_futures_tradetick.attach(console_obs)
        self.real_options_tradetick.attach(console_obs)
        self.real_futures_quotetick.attach(console_obs)
        self.real_options_quotetick.attach(console_obs)

        self.ZMQFuturesTradeSender = ZMQTickSender_New(self.socket, 'kiwoom', 'T', 'futures')
        self.ZMQOptionsTradeSender = ZMQTickSender_New(self.socket, 'kiwoom', 'T', 'options')
        self.ZMQFuturesQuoteSender = ZMQTickSender_New(self.socket, 'kiwoom', 'Q', 'futures')
        self.ZMQOptionsQuoteSender = ZMQTickSender_New(self.socket, 'kiwoom', 'Q', 'options')

        self.real_futures_tradetick.attach(self.ZMQFuturesTradeSender)
        self.real_options_tradetick.attach(self.ZMQOptionsTradeSender)
        self.real_futures_quotetick.attach(self.ZMQFuturesQuoteSender)
        self.real_options_quotetick.attach(self.ZMQOptionsQuoteSender)

        button1 = QtGui.QPushButton("Login", self)
        button1.move(20, 20)
        button1.clicked.connect(self.button1_clicked)

        button2 = QtGui.QPushButton("check state", self)
        button2.move(20, 70)
        button2.clicked.connect(self.button2_clicked)

    def init_zmq(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://127.0.0.1:%d" % self.port)
        # logger.info('zmq port: %d' % self.port)

    def button1_clicked(self):
        # ret = self.ocx.dynamicCall("CommConnect()")
        # self.real_futures_trade_tick.ocx.dynamicCall("CommConnect()")
        self.kiwoom_session.comm_connect()

    def button2_clicked(self):
        # if self.ocx.dynamicCall("GetConnectState()") == 0:
        if self.kiwoom_session.get_connect_state() == 0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")
            self.test()

    def on_event_connect(self, errcode):
        print("ErrCode: %d" % errcode)
        pass

    def on_receive_msg(self, scrno, rqname, trcode, msg):
        print(scrno, rqname, trcode, msg)
        pass

    def test(self):

        futures_list = self.kiwoom_session.get_futures_list()
        print(futures_list[:3])

        screen_no = u"0002"
        code_list = futures_list[0]
        fid_list = u"20;10;15;13;27;28"
        opt_type = u"0"
        ret = self.real_futures_tradetick.set_real_reg(screen_no, code_list, fid_list, opt_type)
        print(ret.toPyObject())

        screen_no = u"0003"
        code_list = u"201PA277"
        fid_list = u"20;10;15;13;27;28"
        opt_type = u"1"
        ret = self.real_options_tradetick.set_real_reg(screen_no, code_list, fid_list, opt_type)
        print(ret.toPyObject())

        screen_no = u"0004"
        code_list = futures_list[0]
        fid_list = u"21;41;61;101;51;71;111;42;62;102;52;72;112;"
        fid_list = fid_list + u"43;63;103;53;73;113;44;64;104;54;74;114;"
        fid_list = fid_list + u"45;65;105;55;75;115;"
        fid_list = fid_list + u"121;123;125;127"
        opt_type = u"1"
        ret = self.real_futures_quotetick.set_real_reg(screen_no, code_list, fid_list, opt_type)
        print(ret.toPyObject())

        screen_no = u"0005"
        code_list = u"201PA267"
        fid_list = u"21;41;61;101;51;71;111;42;62;102;52;72;112;"
        fid_list = fid_list + u"43;63;103;53;73;113;44;64;104;54;74;114;"
        fid_list = fid_list + u"45;65;105;55;75;115;"
        fid_list = fid_list + u"121;123;125;127"
        opt_type = u"1"
        ret = self.real_options_quotetick.set_real_reg(screen_no, code_list, fid_list, opt_type)
        print(ret.toPyObject())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
