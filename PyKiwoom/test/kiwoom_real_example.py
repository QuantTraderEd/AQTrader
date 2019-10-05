# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import zmq
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QAxContainer


class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("KiwoomLoginTest")
        self.setGeometry(300, 300, 300, 150)
        
        self.ocx = QAxContainer.QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.on_event_connect)
        self.ocx.OnReceiveTrData.connect(self.on_receive_tr_data)
        self.ocx.OnReceiveChejanData.connect(self.on_receive_chejan_data)
        self.ocx.OnReceiveRealData.connect(self.on_receive_real_data)
        self.ocx.OnReceiveMsg.connect(self.on_receive_msg)
        self.ocx.OnReceiveConditionVer.connect(self.on_receive_condition_ver)
        self.ocx.OnReceiveTrCondition.connect(self.on_receive_tr_condition)
        self.ocx.OnReceiveRealCondition.connect(self.on_receive_real_condition)

        button1 = QtGui.QPushButton("Login", self)
        button1.move(20, 20)
        button1.clicked.connect(self.button1_clicked)
        
        button2 = QtGui.QPushButton("check state", self)
        button2.move(20, 70)
        button2.clicked.connect(self.button2_clicked)
        
    def button1_clicked(self):
        ret = self.ocx.dynamicCall("CommConnect()")
        
    def button2_clicked(self):
        if self.ocx.dynamicCall("GetConnectState()") == 0:
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
            print (itemname_lst[i] , unicode(data.toPyObject()).strip())

        pass
    
    def on_receive_chejan_data(self):
        pass

    def on_receive_real_data(self, shortcd, realtype, realdata):
        print(unicode(realtype), unicode(shortcd))
        if realtype == u"선물시세":
            for i in self.fidlist:
                data = self.ocx.dynamicCall("GetCommRealData(QString, int)", shortcd, i)
                print(self.fid_name_dict[i], unicode(data.toPyObject()).strip(), )
                self.data[self.fid_name_dict[i]] = unicode(data.toPyObject()).strip()
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

        futures_list = self.get_futures_list()
        print(futures_list[:3])

        id_key = u"종목코드"
        value = futures_list[0]
        rqname = u"선옵현재가정보요청 "
        trcode = "opt50001"
        self.set_input_value(id_key, value)
        self.comm_rq_data(rqname, trcode, 0, "0001")

        screen_no = u"0002"
        code_list = futures_list[0]
        fid_list = u"20;10;15;13;27;28"
        self.fid_name_dict = dict()
        self.fid_name_dict[20] = u"Timestamp"
        self.fid_name_dict[10] = u"LastPrice"
        self.fid_name_dict[15] = u"LastQty"
        self.fid_name_dict[13] = u"Volume"
        self.fid_name_dict[195] = u'OpenInterest'
        self.fid_name_dict[27] = u"Ask1"
        self.fid_name_dict[28] = u"Bid1"
        self.fidlist = self.fid_name_dict.keys()
        opt_type = u"0"
        ret = self.set_real_reg(screen_no, code_list, fid_list, opt_type)
        print(ret.toPyObject())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
