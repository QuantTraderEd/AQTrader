# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 20:35:15 2013

@author: Administrator
"""

import zmq
from PyQt4 import QtGui, QtCore
from ui_executedlg import Ui_Dialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class ExecuteDlg(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initZMQ()
        
        
        
    def initUI(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)        
        
        self.ui.pushButtonSend.clicked.connect(self.onSend)
        pass
    
    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:6000")
        pass
        
                
        
    def onSend(self):
        buysell = self.ui.pushButtonBuySell.isChecked()
        shname = self.ui.lineEditShortName.text()
        price = self.ui.doubleSpinBoxPrice.value()
        qty = self.ui.spinBoxQty.value()
        msg = str(buysell) + ',' + str(shname) + ',' + str(price) + ',' + str(qty)
        #self.socket.send(msg)
        #msg_in = self.socket.recv()
        print msg
        #print buysell,price,qty
        
if __name__ == "__main__":
    import sys    
    app = QtGui.QApplication(sys.argv)
    mydlg = ExecuteDlg()
    mydlg.ui.doubleSpinBoxPrice.setValue(1.25)
    mydlg.show()
    app.exec_()  
        
