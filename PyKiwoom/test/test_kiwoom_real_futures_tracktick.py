# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

from ..pykiwoom.kiwoom_source import KiwoomSession
from ..pykiwoom.kiwoom_real_futures_tradetick import KiwoomFuturesTradeTick


class TestClass(object):
    app = QtGui.QApplication(sys.argv)
    kiwoom_session = KiwoomSession()
    real_futurestradetick = KiwoomFuturesTradeTick(kiwoom_session=kiwoom_session)

    def test_login(self):
        ret = self.kiwoom_session.comm_connect()
        assert self.kiwoom_session.get_connect_state() != 0

    def test_futurestradetick(self):
        futures_list = self.kiwoom_session.get_futures_list()
        assert futures_list[0][:3] == u'101'
        print(futures_list)

        assert self.real_futurestradetick.kiwoom_session.get_connect_state() != 0

        screen_no = u"0005"
        code_list = futures_list[0]
        fid_list = u"9001;20;10;15;13"
        opt_type = u"0"
        self.real_futurestradetick.set_real_reg(screen_no, code_list, fid_list, opt_type)

