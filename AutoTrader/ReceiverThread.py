# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 10:27:17 2014

@author: assa
"""

import zmq
import datetime

from PyQt4 import QtCore

    
class ReceiverThread(QtCore.QThread):
    receiveData = QtCore.pyqtSignal(dict)    
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)
        self.msg = ''
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()       
        self.port = 5501
        
        
    def run(self):
        self.mt_stop = False               
        self.mt_pause = False
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:%d"%self.port)
        self.socket.setsockopt(zmq.SUBSCRIBE,"")           
        
        while True:
            row_dict = self.socket.recv_pyobj()
            self.receiveData.emit(row_dict)
            self.onReceiveData(row_dict)

            self.mutex.lock()
            if self.mt_stop: break
            self.mutex.unlock()
        pass
    
    def stop(self):
        self.mt_stop = True
        pass

    def onReceiveData(self,row_dict): 
        pass
        
