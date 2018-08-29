# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 10:27:17 2014

@author: assa
"""

import zmq
from PyQt4 import QtCore

def cybos_convertor(strprice, floating):
    value = round(float(strprice), floating)
    strformat = '%.' + str(floating) + 'f'
    strValue = strformat%value
    return (strValue)
    
class OptionViewerThread(QtCore.QThread):
    receiveData = QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)
        self.msg = ''
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()        
        
        
    def run(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:5500")
        self.socket.setsockopt(zmq.SUBSCRIBE,"")  
        
        while True:
            msg = self.socket.recv()
            self.receiveData.emit(msg)
            self.onReceiveData(msg)

            self.mutex.lock()
            if self.mt_stop: break
            self.mutex.unlock()
        pass

    def stop(self):
        self.mt_stop = True

    def onReceiveData(self,msg):
        pass
