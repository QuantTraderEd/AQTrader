# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 15:00:36 2015

@author: assa
"""

import zmq
from PyQt4 import QtCore


class SubscribeThread(QtCore.QThread):
    def __init__(self, parent=None, subtype='BackTest'):
        QtCore.QThread.__init__(self,parent)
        self.msg = ''
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()
        self.SubType = subtype
        pass

    def run(self):
        self.mt_stop = False
        self.mt_pause = False
        port = '5501'
        if self.SubType == 'Real':
            port = '5500'
        else:
            assert False
            return
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:%s" % port)
        self.socket.setsockopt(zmq.SUBSCRIBE,"")

        while True:
            if self.SubType == 'BackTest':
                row = self.socket.recv_pyobj()
                self.onReceiveData(row)
            elif self.SubType == 'Real':
                msg = self.socket.recv()
                self.onReceiveData(msg)

            self.mutex.lock()
            if self.mt_stop: break
            self.mutex.unlock()
        pass

    def stop(self):
        self.mt_stop = True
        pass

    def onReceiveData(self,row):
        pass