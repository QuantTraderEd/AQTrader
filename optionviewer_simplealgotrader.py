# -*- coding: utf-8 -*-
"""
Created on Thu Sep 04 08:09:15 2014

@author: assa
"""
import time
import random
import zmq
from PyQt4 import QtCore, QtGui

class SimpleAlgoTrader(QtGui.QWidget):
    def __init__(self,parent = None, widget = None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initVar()
        
        
    def initUI(self):
        self.button = QtGui.QPushButton('Start', self)
        self.button.clicked.connect(self.onStart)
        self.button.move(100, 50)
        self.setWindowTitle('SpAgTder')
        self.resize(200, 120)
        pass
    
    def initVar(self):
        self.counter = 0
        
    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:6000")
        pass
    
    def initTimer(self):
        self.XTimer = QtCore.QTimer()
        self.XTimer.timeout.connect(self.onXTimerUpdate)
    
    def onStart(self):        
        self.XTimer.start(3222)
        print 'XTimer Start'
        pass
    
    def onXTimerUpdate(self):        
        nowtime = time.localtime()
        if nowtime.tm_hour == 14 and nowtime.tm_min > 39 and nowtime.tm_min < 42 and self.counter < 10:            
            #time.sleep(random.randint(0,2000) * 0.001)            
            buysell = True 
            shcode = '201J9262'
            price = 1.90
            qty = 1
            msg = str(buysell) + ',' + str(shcode) + ',' + str(price) + ',' + str(qty)            
            if type(self.socket).__name__ == 'Socket':
                print msg
                self.socket.send(msg)
                msg_in = self.socket.recv()        
                print msg_in
                            
            buysell = True
            shcode = '301J9262'
            price = 1.90
            qty = 1
            msg = str(buysell) + ',' + str(shcode) + ',' + str(price) + ',' + str(qty)            
            if type(self.socket).__name__ == 'Socket':
                print msg
                self.socket.send(msg)
                msg_in = self.socket.recv()        
                print msg_in      
                self.counter+=1                      
                
        pass
    
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = SimpleAlgoTrader()
    wdg.initZMQ()
    wdg.initTimer()
    wdg.show()    
    sys.exit(app.exec_())
