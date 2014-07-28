# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 23:32:11 2014

@author: assa
"""
import zmq
from PyQt4 import QtCore, QtGui
from ui_executewidget import Ui_Form


class OptionViewerExecuteWidget(QtGui.QWidget):
    def __init__(self,parent = None, widget = None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI(widget)
        self.initZMQ()
        
        
    def initUI(self,widget=None):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.onToggled()

        self.ui.horizontalLayout.setContentsMargins(0,0,0,0)
        self.resize(220,40)
        
        self.setWindowFlags(QtCore.Qt.Popup)
        
        point = widget.rect().bottomRight()
        
        global_point = widget.mapToGlobal(point)
        self.move(global_point - QtCore.QPoint(self.width(), 0))
        
        self.ui.pushButtonSend.clicked.connect(self.onSend)
        self.ui.radioButtonBuy.toggled.connect(self.onToggled)
        pass
    
    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:6000")
        pass
    
    def initOrder(self,buysell=True,shcode='',price=0,qty=0):
        self.ui.radioButtonBuy.setChecked(buysell)
        self.ui.radioButtonSell.setChecked(not buysell)
        self.ui.lineEditShortCode.setText(shcode)
        self.ui.doubleSpinBoxPrice.setValue(price)
        self.ui.spinBoxQty.setValue(qty)
        self.onToggled()
        pass
        
    def onSend(self):
        buysell = self.ui.radioButtonBuy.isChecked()
        shcode = self.ui.lineEditShortCode.text()
        price = self.ui.doubleSpinBoxPrice.value()
        qty = self.ui.spinBoxQty.value()
        msg = str(buysell) + ',' + str(shcode) + ',' + str(price) + ',' + str(qty)
        print msg
        self.socket.send(msg)
        msg_in = self.socket.recv()        
        print msg_in
        self.close()
        
    def onToggled(self):
        buysell = self.ui.radioButtonBuy.isChecked()
        if buysell:
            self.ui.pushButtonSend.setText('Buy')
            self.ui.pushButtonSend.setStyleSheet("background-color: blue; color: yellow;")
        elif not buysell:
            self.ui.pushButtonSend.setText('Sell')
            self.ui.pushButtonSend.setStyleSheet("background-color: red")

        
if __name__ == '__main__':
    import sys
    class Window(QtGui.QWidget):
        def __init__(self):
            QtGui.QWidget.__init__(self)
            self.button = QtGui.QPushButton('Hit this button to show a popup', self)
            self.button.clicked.connect(self.handleOpenDialog)
            self.button.move(250, 50)
            self.resize(600, 200)
            
        def handleOpenDialog(self):
            self.popup = OptionViewerExecuteWidget(self, self.button)
            self.popup.show()    
            self.popup.initOrder(False,'201J8260',0.60,1)
        
    app = QtGui.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
        

