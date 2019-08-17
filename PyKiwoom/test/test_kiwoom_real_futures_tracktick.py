# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

from ..pykiwoom.kiwoom_source import KiwoomSession
from ..pykiwoom.kiwoom_real_futures_tradetick import KiwoomFuturesTradeTick


class TestThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()

        self.real_futures_tradetick = None

    def run(self):
        self.mt_stop = False
        self.mt_pause = False

        if not isinstance(self.real_futures_tradetick, KiwoomFuturesTradeTick):
            return

        futures_list = self.real_futures_tradetick.kiwoom_session.get_futures_list()

        screen_no = u"0005"
        code_list = futures_list[0]
        fid_list = u"9001;20;10;15;13"
        opt_type = u"0"
        self.real_futures_tradetick.set_real_reg(screen_no, code_list, fid_list, opt_type)
        self.real_futures_tradetick.receiveData.connect(self.onReceiveData)
        self.real_futures_tradetick.event = QtCore.QEventLoop()
        self.real_futures_tradetick.event.exec_()

    def onReceiveData(self, data_dict):
        print(data_dict)
        self.terminate()
        pass


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

    def test_tickdata_thread(self):
        test_thread = TestThread()
        test_timer = QtCore.QTimer()
        test_timer.timeout.connect(test_thread.terminate)
        test_timer.setSingleShot(True)
        test_timer.start(5000)
        test_thread.real_futures_tradetick = self.real_futurestradetick
        test_thread.start()
        assert test_thread.isRunning()
        test_thread.wait()
        assert len(test_thread.real_futures_tradetick.data) > 0


