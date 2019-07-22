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


class KiwoomSession(object):
    def __init__(self):
        self.ocx = QAxContainer.QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.on_event_connect)
        # self.ocx.OnReceiveTrData.connect(self.on_receive_tr_data)
        # self.ocx.OnReceiveChejanData.connect(self.on_receive_chejan_data)
        # self.ocx.OnReceiveRealData.connect(self.on_receive_real_data)
        # self.ocx.OnReceiveMsg.connect(self.on_receive_msg)
        # self.ocx.OnReceiveConditionVer.connect(self.on_receive_condition_ver)
        # self.ocx.OnReceiveTrCondition.connect(self.on_receive_tr_condition)
        # self.ocx.OnReceiveRealCondition.connect(self.on_receive_real_condition)
        # self.ocx.parent = proxy(self)
        # self.observers = []
        self.data = None
        self.event = None

    def on_event_connect(self, errcode):
        msg = "ErrCode: %d" % errcode
        print(msg)
        pass

    def comm_connect(self):
        ret = self.ocx.dynamicCall("CommConnect()")
        self.event = QtCore.QEventLoop()
        self.event.exec_()
        return ret


    def get_connect_state(self):
        data = self.ocx.dynamicCall("GetConnectState()")
        data = int(data.toPyObject())
        return data

    def get_login_info(self, tag):
        """
        "ACCOUNT_CNT”–전체계좌개수를반환한다.
        "ACCNO"–전체계좌를반환한다. 계좌별구분은‘;’이다.
        “USER_ID”-사용자ID를반환한다.
        “USER_NAME”–사용자명을반환한다.
        “KEY_BSECGB”–키보드보안해지여부. 0:정상, 1:해지
        “FIREW_SECGB”–방화벽설정여부. 0:미설정, 1:설정, 2:해지
        """
        data = self.ocx.dynamicCall("GetLoginInfo(QString)", tag)
        data = unicode(data.toPyObject())
        if tag == "ACCNO":
            data = data.split(u";")
        return data

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

    def get_actprice_list(self):
        data = self.ocx.dynamicCall("GetActPriceList()")
        data = unicode(data.toPyObject())
        data = data.split(u";")
        return data

    def get_option_code(self):
        data = self.ocx.dynamicCall("GetOptionCode()")
        data = unicode(data.toPyObject())
        data = data.split(u";")
        return data


class KiwoomTR(object):
    def __init__(self):
        self.ocx = QAxContainer.QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        # self.ocx.OnEventConnect.connect(self.on_event_connect)
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


class KiwoomReal(object):
    def __init__(self):
        self.ocx = QAxContainer.QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.on_event_connect)
        # self.ocx.OnReceiveTrData.connect(self.on_receive_tr_data)
        self.ocx.OnReceiveChejanData.connect(self.on_receive_chejan_data)
        self.ocx.OnReceiveRealData.connect(self.on_receive_real_data)
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

    def notify(self):
        for obs in self.observers:
            obs.update(proxy(self))

    def on_signal(self, realtype, shortcd):
        raise NotImplementedError

    def on_event_connect(self, errcode):
        print("ErrCode: %d" % errcode)
        pass

    def on_receive_msg(self, scrno, rqname, trcode, msg):
        print(scrno, rqname, trcode, msg)

    def set_real_reg(self, scrno, cdlist, fidlist, opttype):
        """
        # 실시간 등록을 한다.
        # strScreenNo : 화면번호
        # strCodeList : 종목코드리스트(ex: 039490;005930;…)
        # strFidList : FID번호(ex:9001;10;13;…)
        # 	9001 – 종목코드
        # 	10 - 현재가
        # 	13 - 누적거래량
        # strOptType : 타입(“0”, “1”)
        # 타입 “0”은 항상 마지막에 등록한 종목들만 실시간등록이 됩니다.
        # 타입 “1”은 이전에 실시간 등록한 종목들과 함께 실시간을 받고 싶은 종목을 추가로 등록할 때 사용합니다.
        # ※ 종목, FID는 각각 한번에 실시간 등록 할 수 있는 개수는 100개 입니다.
        """
        ret = self.ocx.dynamicCall("SetRealReg(QString, QString, QString, QString)", scrno,
                                   cdlist,
                                   fidlist,
                                   opttype)
        return ret

    def on_receive_chejan_data(self):
        pass

    def on_receive_real_data(self, shortcd, realtype, realdata):
        print(unicode(realtype), unicode(shortcd))
        self.on_signal(realtype, shortcd)
        # if realtype == u"선물시세":
        #     fidlist = [9001, 20, 10, 15, 13]
        #     fid_name_dict = dict()
        #     fid_name_dict[9001] = u"timestamp"
        #     fid_name_dict[20] = u"last_price"
        #     fid_name_dict[15] = u"last_qty"
        #     fid_name_dict[13] = u"volume"
        #     for i in fidlist:
        #         data = self.ocx.dynamicCall("GetCommRealData(QString, int)", shortcd, i)
        #         print(fid_name_dict[i], unicode(data.toPyObject()).strip())


