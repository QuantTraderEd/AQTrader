# -*- coding: utf-8 -*-

import logging
import pprint
import datetime as dt

from logging.handlers import RotatingFileHandler
from ..dataloader.SubscribeReceiverThread import SubscribeThread

logger = logging.getLogger('dataload.test')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('dataload.log')
fh = RotatingFileHandler('dataload.log', maxBytes=104857, backupCount=3)
fh.setLevel(logging.INFO)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s '
                              '%(filename)s %(funcName)s() %(lineno)d:\t\t'                              
                              '%(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)


class TestThread(SubscribeThread):
    def __init__(self, parent=None):
        SubscribeThread.__init__(self, parent)
        self.now_dt = dt.datetime.now()
        self.msg_dict = dict()
        self.msg_dict['TimeStamp'] = self.now_dt

    def onReceiveData(self, msg_dict):
        now_dt = dt.datetime.now()
        shortcd = msg_dict['ShortCD']
        feedsource = msg_dict['FeedSource']
        taq = msg_dict['TAQ']
        securities_type = msg_dict['SecuritiesType']
        logger.info('msg_dict[TimeStamp]: %s, now_dt: %s' % (msg_dict['TimeStamp'], now_dt))
        msg = pprint.pformat(msg_dict)
        logger.info('msg_dict->\n%s' % msg)
        self.msg_dict = msg_dict
        self.nowtime = now_dt
        self.stop()


class TestClass(object):
    test_thread = TestThread()
    test_thread.port = 5501
    test_thread.start()

    def test_thread_running(self):
        assert self.test_thread.isRunning()
        self.test_thread.wait()
        assert 'OpenInterest' in self.test_thread.msg_dict
        assert self.test_thread.msg_dict['FeedSource'] == 'kiwoom'
        assert self.test_thread.msg_dict['TimeStamp'] == self.test_thread.nowtime