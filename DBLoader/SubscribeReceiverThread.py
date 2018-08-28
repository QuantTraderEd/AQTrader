# -*- coding: utf-8 -*-


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
        self.subType = subtype

    def run(self):
        self.mt_stop = False
        self.mt_pause = False
        port = '5503'
        if self.subType == 'Real':
            port = '5501'
        if self.subType == 'RealTest':
            port = '5503'
        elif self.subType == 'BackTest':
            port = '5502'
        else:
            raise AssertionError()
            return
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:%s" % port)
        self.socket.setsockopt(zmq.SUBSCRIBE, "")

        while True:
            self.mutex.lock()
            if self.mt_stop: break
            self.mutex.unlock()

            if self.subType == 'BackTest':
                msg_dict = self.socket.recv_pyobj()
                self.onReceiveData(msg_dict)
            elif self.subType == 'Real':
                msg_dict = self.socket.recv_pyobj()
                self.onReceiveData(msg_dict)
        pass

    def stop(self):
        self.mt_stop = True
        pass

    def onReceiveData(self, msg_dict):
        pass
