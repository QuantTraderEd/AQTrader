# -*- coding: utf-8 -*-

import time
import zmq
from PyQt4 import QtCore

from DataFeeder.ZMQTickSender import ZMQTickSender_New


class PublishThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.pub_port = 5510
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pause_condition = QtCore.QWaitCondition()
        self.zmq_tick_sender = ZMQTickSender_New()

    def init_zmq(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://127.0.0.1:%d" % self.pub_port)

    def run(self):
        self.init_zmq()

        for i in range(10):
            time.sleep(1)
            self.socket.send_pyobj(i)
            print(i)
            self.mutex.lock()
            if self.mt_stop:
                break
            if self.mt_pause:
                self.mt_pauseCondition.wait(self.mutex)
            self.mutex.unlock()

    def mtf_stop(self):
        self.mt_stop = True

    def mtf_pause(self):
        self.mt_pause = True

    def mtf_resume(self):
        self.mt_pause = False
        self.mt_pause_condition.wakeAll()

    def mtf_reset(self):
        self.mt_stop = False
        self.mt_pause = False
        self.mutex.unlock()
