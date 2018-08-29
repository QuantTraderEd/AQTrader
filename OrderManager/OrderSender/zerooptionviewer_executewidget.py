# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 23:32:11 2014

@author: assa
"""
import zmq
import logging
from PyQt4 import QtCore, QtGui
from ui_executewidget import Ui_Form


logger = logging.getLogger('SendOrder')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('SendOrder.log')
#fh = logging.Handlers.RotatingFileHandler('SendOrder.log',maxBytes=104857,backupCount=3)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)


class OptionViewerSendOrderWidget(QtGui.QWidget):
    def __init__(self,parent = None, widget = None):
        QtGui.QWidget.__init__(self,parent)
        self.initVar()
        self.initUI(widget)        
        
        
    def initVar(self):
        self.synthfutures_dict = {}
        self.socket = None
        
    def initUI(self,widget=None):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.onToggled()

        self.ui.horizontalLayout.setContentsMargins(0,0,0,0)
        self.resize(220,40)
        
        self.setWindowFlags(QtCore.Qt.Popup)
        self.initMove(widget)
                
        self.ui.pushButtonSend.clicked.connect(self.onSend)
        self.ui.radioButtonBuy.toggled.connect(self.onToggled)
        pass
    
    def initMove(self,widget):
        if widget != None:
            point = widget.rect().bottomRight()
            global_point = widget.mapToGlobal(point)
            self.move(global_point - QtCore.QPoint(self.width(), 0))
        pass
        
    
    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO,2000)
        self.socket.connect("tcp://127.0.0.1:6004")
        pass
    
    def initOrder(self,shortcd='',price=0,qty=0,buysell=' '):
        if buysell == 'B':    
            self.ui.radioButtonBuy.setChecked(True)
            self.ui.radioButtonSell.setChecked(False)
        elif buysell == 'S':
            self.ui.radioButtonBuy.setChecked(False)
            self.ui.radioButtonSell.setChecked(True)
        else:
            return
        self.ui.lineEditShortCode.setText(shortcd)
        self.ui.doubleSpinBoxPrice.setValue(price)
        self.ui.spinBoxQty.setValue(qty)
        self.onToggled()
        pass
    
    def initSynthOrder(self,buysell=True,price=0,callShCode='',callPrice=0,putShCode='',putPrice=0,qty=0):        
        self.ui.radioButtonBuy.setChecked(buysell)
        self.ui.radioButtonSell.setChecked(not buysell)
        self.ui.lineEditShortCode.setText('SNTH'+callShCode[-5:])
        self.ui.doubleSpinBoxPrice.setValue(price)
        self.ui.spinBoxQty.setValue(qty)
        self.onToggled()
        self.synthfutures_dict = {}
        self.synthfutures_dict[callShCode] = callPrice
        self.synthfutures_dict[putShCode] = putPrice
        pass
        
        
    def onSend(self):
        if self.ui.radioButtonBuy.isChecked():
            buysell = 'B'
        else:
            buysell = 'S'
        shortcd = self.ui.lineEditShortCode.text()
        price = self.ui.doubleSpinBoxPrice.value()
        qty = self.ui.spinBoxQty.value()
        if shortcd[:3] in ['101','201','301','105']:
            msg_dict = {}
            msg_dict['ShortCD'] =  shortcd
            msg_dict['OrderPrice'] = price
            msg_dict['OrderQty'] = qty
            msg_dict['BuySell'] = buysell
            msg_dict['NewAmendCancel'] = 'N'
            msg_dict['OrderType'] = 2 # market = 1 limit = 2
            msg_dict['TimeInForce'] = 'GFD'
            logger.info(str(msg_dict))
            if type(self.socket).__name__ == 'Socket':
                logger.info('Send Order')
                self.socket.send_pyobj(msg_dict)
                msg_in = self.socket.recv()     
                logger.info('Recv Msg')
        elif shortcd[:4] == 'SNTH':
            for key in self.synthfutures_dict.iterkeys():
                price = self.synthfutures_dict[key]
                if key[:3] == '301': bs = not buysell
                elif key[:3] == '201': bs = buysell
                msg = str(bs) + ',' + str(key) + ',' + str(price) + ',' + str(qty)
                print msg
                if type(self.socket).__name__ == 'Socket':
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
            self.setWindowTitle('OrderSender')
            self.button = QtGui.QPushButton('Hit this button to show a popup', self)
            self.button.clicked.connect(self.handleOpenDialog)
            self.button.resize(300,60)
            self.button.move(100, 20)
            self.resize(500, 100)
            
        def handleOpenDialog(self):
            self.popup = OptionViewerSendOrderWidget(self, self.button)
            self.popup.initZMQ()
            self.popup.ui.doubleSpinBoxPrice.setMaximum(300)
            self.popup.show()   
            # self.popup.initOrder('105L9000',250,1,'B')
            self.popup.initOrder('301LA215',0.01,1,'B')            
        
    app = QtGui.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
        

