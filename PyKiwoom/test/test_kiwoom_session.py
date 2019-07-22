# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

from ..pykiwoom.kiwoom_source import KiwoomSession


class TestClass(object):
    app = QtGui.QApplication(sys.argv)
    kiwoom_session = KiwoomSession()

    def test_login(self):
        ret = self.kiwoom_session.comm_connect()

        assert self.kiwoom_session.get_connect_state() != 0

