# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("KiwoomLoginTest")
        self.setGeometry(300, 300, 300, 150)
        
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        
        button1 = QPushButton("Login", self)
        button1.move(20, 20)
        button1.clicked.connect(self.button1_clicked)
        
        button2 = QPushButton("check state", self)
        button2.move(20, 70)
        button2.clicked.connect(self.button2_clicked)
        
    def button1_clicked(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")
        
    def button2_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()