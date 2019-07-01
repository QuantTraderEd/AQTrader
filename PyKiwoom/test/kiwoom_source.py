# -*- coding: utf-8 -*-

from __future__ import print_function

from weakref import proxy
from PyQt4 import QtCore
from PyQt4 import QAxContainer


class Kiwoom(object):
    def __init__(self):
        self.ocx = QAxContainer.QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.on_event_connect)
        self.ocx.OnReceiveTrData.connect(self.on_receive_tr_data)
        # self.ocx.OnReceiveChejanData.connect(self.on_receive_chejan_data)
        # self.ocx.OnReceiveRealData.connect(self.on_receive_real_data)
        self.ocx.OnReceiveMsg.connect(self.on_receive_msg)
        # self.ocx.OnReceiveConditionVer.connect(self.on_receive_condition_ver)
        # self.ocx.OnReceiveTrCondition.connect(self.on_receive_tr_condition)
        # self.ocx.OnReceiveRealCondition.connect(self.on_receive_real_condition)
        self.ocx.parent = proxy(self)
        self.observers = []
        self.data = None
        self.event = None

    # observer routine
    def attach(self, obs):
        if not (obs in self.observers):
            self.observers.append(obs)

    def detach(self, obs):
        try:
            self.observers.remove(obs)
        except ValueError:
            pass

    def get_futures_list(self):
        data = self.ocx.dynamicCall("GetFutureList()")
        data = unicode(data.toPyObject())
        data = data.split(u";")
        return data

    def get_month_list(self):
        data = self.ocx.dynamicCall("GetMonthList()")
        data = unicode(data.toPyObject())
        data = data.split(u";")
        return data

    def on_event_connect(self, errcode):
        print("ErrCode: %d" % errcode)
        pass

    def notify(self):
        for obs in self.observers:
            obs.update(proxy(self))

    def on_signal(self, trcode, rqname):
        raise NotImplementedError

    def set_input_value(self, id, value):
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, prevnext, scrno):
        ret = self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", rqname,
                                   trcode,
                                   prevnext,
                                   scrno)
        self.event = QtCore.QEventLoop()
        self.event.exec_()
        return ret

    def on_receive_msg(self, scrno, rqname, trcode, msg):
        print(scrno, rqname, trcode, msg)

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
        print(unicode(trcode), unicode(rqname))
        self.on_signal(trcode, rqname)
