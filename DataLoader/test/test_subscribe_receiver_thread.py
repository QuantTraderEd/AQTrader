# -*- coding: utf-8 -*-

import datetime as dt
from PyQt4 import QtGui
from ..dataloader.SubscribeReceiverThread import SubscribeThread


class TestThread(SubscribeThread):
    def __init__(self, parent=None):
        SubscribeThread.__init__(self, parent)
        self.nowtime = dt.datetime.now()
        self.msg_dict = dict()
        self.msg_dict['TimeStamp'] = self.nowtime

    def onReceiveData(self, msg_dict):
        nowtime = dt.datetime.now()
        shortcd = msg_dict['ShortCD']
        feedsource = msg_dict['FeedSource']
        taq = msg_dict['TAQ']
        securities_type = msg_dict['SecuritiesType']
        print msg_dict['TimeStamp'], nowtime
        print nowtime, msg_dict
        self.msg_dict = msg_dict
        self.nowtime = nowtime
        self.stop()


class TestClass(object):
    test_thread = TestThread()
    test_thread.port = 5501
    test_thread.start()

    def test_thread_running(self):
        assert self.test_thread.isRunning()
        self.test_thread.wait()
        assert self.test_thread.msg_dict['TimeStamp'] == self.test_thread.nowtime