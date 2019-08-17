# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

from ..pykiwoom.kiwoom_source import KiwoomSession
from ..pykiwoom.kiwoom_tr_opt50001 import KiwoomOPT50001


class TestClass(object):
    app = QtGui.QApplication(sys.argv)
    kiwoom_session = KiwoomSession()
    opt50001 = KiwoomOPT50001()

    def test_login(self):
        ret = self.kiwoom_session.comm_connect()

        assert self.kiwoom_session.get_connect_state() != 0

    def test_tr_opt50001(self):
        id_key = u"종목코드"
        value = u'101P9000'
        rqname = u"선옵현재가정보요청 "
        trcode = "opt50001"
        self.opt50001.set_input_value(id_key, value)
        self.opt50001.comm_rq_data(rqname, trcode, 0, "0001")
        data = self.opt50001.data
        print(data)
        assert isinstance(data, list)
        assert len(data) == 14
