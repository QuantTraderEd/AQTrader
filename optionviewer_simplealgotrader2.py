# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 09:01:06 2014

@author: assa
"""

import time
import zmq
from PyQt4 import QtCore, QtGui
from zerooptionviewer_thread import OptionViewerThread
from FeedCodeList import FeedCodeList


class SimpleAlgoTrader(QtGui.QWidget):
    def __init__(self,parent = None, widget = None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initVar()
        self.initFeedCode()
        self.initStrikeList()        
        self.initThread()
        pass
        
    def initUI(self):
        self.button = QtGui.QPushButton('Start', self)
        self.button.clicked.connect(self.onClick)
        self.button.move(60, 50)
        self.setWindowTitle('SpAgTder')
        self.resize(200, 120)
        pass
    
    def initVar(self):
        self.counter = 0
        self.counter1 = 0
        self.callShCode = '201JA267'
        self.putShCode = '301JA255'
        self.entry_counter1 = 0
        self.entry_counter2 = 0
        pass
        
    def initFeedCode(self):
        self._FeedCodeList = FeedCodeList()
        self._FeedCodeList.ReadCodeListFile()
        pass
        
    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:6000")
        pass
    
    def initThread(self):
        self.mythread = OptionViewerThread(None)
        self.mythread.receiveData[str].connect(self.onReceiveData)
        pass
    
    def initTimer(self):
        self.XTimer = QtCore.QTimer()
        self.XTimer.timeout.connect(self.onXTimerUpdate)
        pass
        
    def initStrikeList(self):
        shcodelist = self._FeedCodeList.optionshcodelst
        self.strikelst = list(set([shcode[-3:] for shcode in shcodelist]))
        self.strikelst.sort()
        self.strikelst.reverse()
        pass
    
    def onClick(self):        
        if not self.mythread.isRunning() and not self.XTimer.isActive():                        
            self.mythread.start()
            self.XTimer.start(3222)
            self.button.setText('Stop')
        else:
            self.mythread.terminate()
            self.XTimer.stop()
            self.button.setText('Start')
        pass
    
    def onReceiveData(self,msg):
        print msg
        pass
    
    def onXTimerUpdate(self):        
        nowtime = time.localtime()
        print nowtime
        pass
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = SimpleAlgoTrader()
    wdg.initZMQ()
    wdg.initTimer()
    wdg.show()    
    sys.exit(app.exec_())
        
