# -*- coding: utf-8 -*-

import zmq
from PyQt4 import QtCore


def cybos_convertor(strprice, floating):
    value = round(float(strprice), floating)
    strformat = '%.' + str(floating) + 'f'
    strValue = strformat % value
    return (strValue)


class OptionViewerThread(QtCore.QThread):
    receiveData = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None, port=5503):
        QtCore.QThread.__init__(self, parent)
        self.msg = ''
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()
        self.port = port

    def run(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:%s" % self.port)
        self.socket.setsockopt(zmq.SUBSCRIBE, "")
        
        while True:
            msg_dict = self.socket.recv_pyobj()
            self.receiveData.emit(msg_dict)
            self.onReceiveData(msg_dict)

            self.mutex.lock()
            if self.mt_stop: break
            self.mutex.unlock()
        pass

    def stop(self):
        self.mt_stop = True

    def onReceiveData(self, msg_dict):
        pass
