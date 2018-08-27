# -*- coding: utf-8 -*-

import logging
import zmq
from PyQt4 import QtCore, QtGui
from ui_orderwidget import Ui_Form


class OptionViewerOrderWidget(QtGui.QWidget):
    def __init__(self, parent=None, widget=None):
        QtGui.QWidget.__init__(self,parent)
        self.initVar()
        self.initUI(widget)
        self.logger = logging.getLogger('ZeroOptionViewer.OrderWidget')
        self.logger.info('Init OrderWidget')

    def initVar(self):
        self.synthfutures_dict = {}
        self.socket = None
        
    def initUI(self,widget=None):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.onToggled()

        self.ui.horizontalLayout.setContentsMargins(0,0,0,0)
        self.resize(220, 40)
        
        self.setWindowFlags(QtCore.Qt.Popup)
        self.initMove(widget)
                
        self.ui.pushButtonSend.clicked.connect(self.onSend)
        self.ui.radioButtonBuy.toggled.connect(self.onToggled)
        pass
    
    def initMove(self, widget):
        if widget is not None:
            point = widget.rect().bottomRight()
            global_point = widget.mapToGlobal(point)
            self.move(global_point - QtCore.QPoint(self.width(), 0))
        pass

    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.RCVTIMEO, 2000)
        # self.order_port = 6000  # real port
        self.order_port = 6001  # demo port
        self.socket.connect("tcp://127.0.0.1:%d" % self.order_port)
        pass

    def initOrder(self, shortcd='', price=0, qty=0, buysell=''):
        if isinstance(buysell, str):
            if buysell == 'B':
                self.ui.radioButtonBuy.setChecked(True)
                self.ui.radioButtonSell.setChecked(False)
            elif buysell == 'S':
                self.ui.radioButtonBuy.setChecked(False)
                self.ui.radioButtonSell.setChecked(True)
        elif isinstance(buysell, bool):
            self.ui.radioButtonBuy.setChecked(buysell)
            self.ui.radioButtonSell.setChecked(not buysell)
        else:
            return
        self.ui.lineEditShortCode.setText(shortcd)
        self.ui.doubleSpinBoxPrice.setValue(price)
        self.ui.spinBoxQty.setValue(qty)
        self.onToggled()
        pass
    
    def initSynthOrder(self, buysell=True, price=0, callShCode='', callPrice=0, putShCode='', putPrice=0, qty=0):
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
        shortcd = str(self.ui.lineEditShortCode.text())
        price = self.ui.doubleSpinBoxPrice.value()
        qty = self.ui.spinBoxQty.value()
        if shortcd[:3] in ['201', '301']:
            msg_dict = {}
            msg_dict['ShortCD'] =  shortcd
            msg_dict['OrderPrice'] = price
            msg_dict['OrderQty'] = qty
            msg_dict['BuySell'] = buysell
            msg_dict['NewAmendCancel'] = 'N'
            msg_dict['OrderType'] = 2  # market = 1 limit = 2
            msg_dict['TimeInForce'] = 'GFD'
            if type(self.socket).__name__ == 'Socket':
                self.logger.info('Send Order->'+str(msg_dict))
                self.socket.send_pyobj(msg_dict)
                msg_dict_in = self.socket.recv_pyobj()
                self.logger.info('Recv Msg->'+msg_dict_in['MsgCode'])
        # elif shcode[:4] == 'SNTH':
        #     for key in self.synthfutures_dict.iterkeys():
        #         price = self.synthfutures_dict[key]
        #         if key[:3] == '301': bs = not buysell
        #         elif key[:3] == '201': bs = buysell
        #         msg = str(bs) + ',' + str(key) + ',' + str(price) + ',' + str(qty)
        #         print msg
        #         if type(self.socket).__name__ == 'Socket':
        #             self.socket.send(msg)
        #             msg_in = self.socket.recv()
        #             print msg_in
            
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
            self.button.resize(300,60)
            self.button.move(100, 20)
            self.resize(500, 100)
            
        def handleOpenDialog(self):
            self.popup = OptionViewerOrderWidget(self, self.button)
            self.popup.initZMQ()
            self.popup.ui.doubleSpinBoxPrice.setMaximum(300)
            self.popup.show()
            self.popup.initOrder('101LA000',250,1,'B')
            # self.popup.initOrder('301LA215',0.01,1,'B')

    app = QtGui.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

