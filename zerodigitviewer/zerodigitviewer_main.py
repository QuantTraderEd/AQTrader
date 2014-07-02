# -*- coding: utf-8 -*-
"""
Created on Wed Jul 02 22:20:29 2014

@author: assa
"""
import sys
from PyQt4 import QtGui, QtCore
from ui_zerodigitviewer import Ui_Form

class ZeroDigitViewer(QtGui.QWidget):
    def __init__(self,parent=None):
        super(ZeroDigitViewer,self).__init__()
        self.initUI()
        
    def initUI(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
if __name__ == '__main__':    
    app = QtGui.QApplication(sys.argv)
    myform = ZeroDigitViewer()
    myform.show()
    app.exec_()
    