# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import zmq
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QAxContainer
# from kiwoom_tr_opt50001 import KiwoomOPT50001
from PyKiwoom.pykiwoom.kiwoom_source import KiwoomSession
from PyKiwoom.pykiwoom.kiwoom_real_futures_tradetick import KiwoomFuturesTradeTick
from PyKiwoom.pykiwoom.kiwoom_real_options_tradetick import KiwoomOptionsTradeTick
from DataFeeder.ZMQTickSender import ZMQTickSender_New


class ConsoleObserver:
    def update(self,subject):
        print("===== console observer ====")
        for key in subject.data:
            print(key, subject.data[key],)
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
        self.ocx.OnReceiveTrData.connect(self.on_receive_tr_data)
        self.ocx.OnReceiveChejanData.connect(self.on_receive_chejan_data)
        self.ocx.OnReceiveRealData.connect(self.on_receive_real_data)
        self.ocx.OnReceiveMsg.connect(self.on_receive_msg)
        self.ocx.OnReceiveConditionVer.connect(self.on_receive_condition_ver)
        self.ocx.OnReceiveTrCondition.connect(self.on_receive_tr_condition)
        self.ocx.OnReceiveRealCondition.connect(self.on_receive_real_condition)
        # self.opt50001 = KiwoomOPT50001()
        self.kiwoom_session = KiwoomSession()
        self.real_futures_tradetick = KiwoomFuturesTradeTick(kiwoom_session=self.kiwoom_session)
        self.real_options_tradetick = KiwoomOptionsTradeTick(kiwoom_session=self.kiwoom_session)

        console_obs = ConsoleObserver()
        self.real_futures_tradetick.attach(console_obs)
        self.real_options_tradetick.attach(console_obs)

        self.ZMQFuturesTradeSender = ZMQTickSender_New(self.socket, 'kiwoom', 'T', 'futures')
        self.ZMQOptionsTradeSender = ZMQTickSender_New(self.socket, 'kiwoom', 'T', 'options')
        self.real_futures_tradetick.attach(self.ZMQFuturesTradeSender)
        self.real_options_tradetick.attach(self.ZMQOptionsTradeSender)

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
    
    def on_receive_tr_data(self, scrno, rqname, trcode, recordname, prevnext, 
                           datalength, errorcode, message, splm_msg):
        """
        scrno: 화면번호
        rqname: 사용자구분명 (TR 요청명)
        trcode: TR code
        recordname: record 이름
        prevnext: 연속조회유뮤
        datalength: 1.0.0.1 버전 이후 사용하지 않음.
        errorcode: 1.0.0.1 버전 이후 사용하지 않음.
        message: 1.0.0.1 버전 이후 사용하지 않음.
        splm_msg: 1.0.0.1 버전 이후 사용하지 않음.
        """
        print (unicode(trcode), unicode(rqname))
        # data = self.ocx.getCommData(trcode, rqname, 0, u"현재가")
        itemname_lst = [u"종목명", u"체결시간", u"현재가", u"체결량", u"누적거래량"]
        for i in xrange(len(itemname_lst)):
            data = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", trcode,
                                                                                   rqname,
                                                                                   0,
                                                                                   itemname_lst[i])
            print (unicode(data.toPyObject()).strip())

        pass
    
    def on_receive_chejan_data(self):
        pass
    
    def on_receive_real_data(self):
        pass
    
    def on_receive_msg(self, scrno, rqname, trcode, msg):
        print (scrno, rqname, trcode, msg)
        pass
    
    def on_receive_condition_ver(self):
        pass
    
    def on_receive_tr_condition(self):
        pass
    
    def on_receive_real_condition(self):
        pass

    def set_input_value(self, id, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, prevnext, scrno):
        ret = self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", rqname,
                                                                                 trcode,
                                                                                 prevnext,
                                                                                 scrno)
        return ret

    def get_futures_list(self):
        data = self.ocx.dynamicCall("GetFutureList()")
        data = unicode(data.toPyObject())
        data = data.split(u";")
        return data
        
    def test(self):
        id_key = u"종목코드"
        value = u'101P9000'
        rqname = u"선옵현재가정보요청 "
        trcode = "opt50001"

        futures_list = self.kiwoom_session.get_futures_list()
        print(futures_list[:3])

        # id_key = u"종목코드"
        # value = futures_list[0]
        # rqname = u"선옵현재가정보요청 "
        # trcode = "opt50001"
        # self.set_input_value(id_key, value)
        # self.comm_rq_data(rqname, trcode, 0, "0001")

        # value = u'101PC000'
        # self.opt50001.set_input_value(id_key, value)
        # self.opt50001.comm_rq_data(rqname, trcode, 0, "0001")
        # data = self.opt50001.data
        # print(data)

        # ret = self.real_futures_trade_tick.ocx.dynamicCall("GetConnectState()")
        # print("conn:", ret.toPyObject())

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


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
