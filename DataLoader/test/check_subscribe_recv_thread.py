# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime as dt
from PyQt4 import QtGui
from DataLoader.dataloader.SubscribeReceiverThread import SubscribeThread


class TestThread(SubscribeThread):
    def __init__(self, parent=None, port=5502):
        SubscribeThread.__init__(self, parent, port=port)
        self.nowtime = dt.datetime.now()
        self.msg_dict = dict()
        self.msg_dict['TimeStamp'] = self.nowtime

    def onReceiveData(self, msg_dict):
        nowtime = dt.datetime.now()
        shortcd = msg_dict['ShortCD']
        feedsource = msg_dict['FeedSource']
        taq = msg_dict['TAQ']
        securities_type = msg_dict['SecuritiesType']
        # print msg_dict['TimeStamp'], nowtime
        # if securities_type == 'options':
        # if shortcd[:3] == '105':
        print(nowtime, msg_dict['TimeStamp'], shortcd, securities_type, taq, end=' ')
        if taq == 'T':
            print(msg_dict['Ask1'], msg_dict['Bid1'], msg_dict['LastPrice'], msg_dict['LastQty'], end=' ')
        elif taq == 'Q':
            print(msg_dict['AskQty1'], msg_dict['Ask1'], msg_dict['Bid1'], msg_dict['BidQty1'], end=' ')
        print('dt:', (nowtime - msg_dict['TimeStamp']))
        self.msg_dict = msg_dict
        self.nowtime = nowtime


def main():
    test_thread = TestThread(port=5501)
    test_thread.start()
    test_thread.wait()


if __name__ == "__main__":
    main()
