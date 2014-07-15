# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 23:32:11 2014

@author: assa
"""

import sys
from PyQt4 import QtCore, QtGui
from ui_executewidget import Ui_Form


class ExcuteWidget(QtGui.QWidget):
    def __init__(self,parent = None, widget = None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # adjust the margins or you will get an invisible, uninterended border
        self.ui.horizontalLayout.setContentsMargins(0,0,0,0)

        # need to set the layout
        self.adjustSize()
        
        # tag this widget as a popup
        self.setWindowFlags(QtCore.Qt.Popup)
        
        # calculate the bottom right point from the parents rectangle
        point = widget.rect().bottomRight()
        
        # map that point as a global position
        global_point = widget.mapToGlobal(point)
        
        # by default, a widget will be placed from its top-left corner, so
        # we need to move it to the left based on the widgets width
        self.move(global_point - QtCore.QPoint(self.width(), 0))
        
class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.button = QtGui.QPushButton('Hit this button to show a popup', self)
        self.button.clicked.connect(self.handleOpenDialog)
        self.button.move(250, 50)
        self.resize(600, 200)
        
    def handleOpenDialog(self):
        self.popup = ExcuteWidget(self, self.button)
        self.popup.show()
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
        

