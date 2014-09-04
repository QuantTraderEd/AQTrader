# -*- coding: utf-8 -*-
"""
Created on Thu Sep 04 08:09:15 2014

@author: assa
"""
import time
import zmq
from PyQt4 import QtCore, QtGui

class SimpleAlgoTrader(QtGui.QWidget):
    def __init__(self,parent = None, widget = None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initVar()
        
        
    def initUI(self):
        self.button = QtGui.QPushButton('Start', self)
        self.button.clicked.connect(self.onClick)
        self.button.move(60, 50)
        self.setWindowTitle('SpAgTder')
        self.resize(200, 120)
        pass
    
    def initVar(self):
        self.counter = 0
        self.entry_counter1 = 0
        self.entry_counter2 = 0
        
    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:6000")
        pass
    
    def initTimer(self):
        self.XTimer = QtCore.QTimer()
        self.XTimer.timeout.connect(self.onXTimerUpdate)
    
    def onClick(self):
        if not self.XTimer.isActive():
            self.XTimer.start(3222)
            self.button.setText('Stop')
        else:
            self.XTimer.stop()
            self.button.setText('Start')
        pass
    
    def onXTimerUpdate(self):        
        nowtime = time.localtime()
        if nowtime.tm_hour == 9 and nowtime.tm_min > 23 and nowtime.tm_min < 26 and self.entryc_counter1 < 5:
            buysell = False
            shcode = '201J9262'
            price = 0.40
            qty = 1     
            
            self.sendOrder(buysell,shcode,price,qty)            
                            
            buysell = False
            shcode = '301J9262'
            price = 0.40
            qty = 1
            
            if self.sendOrder(buysell,shcode,price,qty):            
                self.entry_counter+=1
                
        elif nowtime.tm_hour == 11 and nowtime.tm_min > 23 and nowtime.tm_min < 26 and self.entryc_counter2 < 5:
            buysell = False
            shcode = '201J9262'
            price = 0.40
            qty = 1     
            
            self.sendOrder(buysell,shcode,price,qty)            
                            
            buysell = False
            shcode = '301J9262'
            price = 0.40
            qty = 1
            
            if self.sendOrder(buysell,shcode,price,qty):            
                self.entry_counter2+=1
                
        elif nowtime.tm_hour == 14 and nowtime.tm_min > 39 and nowtime.tm_min < 42 and self.counter < 10:            
            #time.sleep(random.randint(0,2000) * 0.001)            
            buysell = True 
            shcode = '201J9262'
            price = 1.90
            qty = 1
            
            self.sendOrder(buysell,shcode,price,qty)            
                            
            buysell = True
            shcode = '301J9262'
            price = 1.90
            qty = 1
            
            if self.sendOrder(buysell,shcode,price,qty):
                self.counter+=1
                
        pass
    
    def sendOrder(self,buysell,shcode,price,qty):
        if type(self.socket).__name__ == 'Socket':
            msg = str(buysell) + ',' + str(shcode) + ',' + str(price) + ',' + str(qty)            
            print msg
            self.socket.send(msg)
            msg_in = self.socket.recv()        
            print msg_in
            return True
        else:
            print 'not define socket..'
            return False
        pass
    
    
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = SimpleAlgoTrader()
    wdg.initZMQ()
    wdg.initTimer()
    wdg.show()    
    sys.exit(app.exec_())
