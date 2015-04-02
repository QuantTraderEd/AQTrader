# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:14:13 2015

@author: assa
"""
import pdb
import pandas as pd
from BackTestReceiver_Thread import BackTestReceiverThread
from PyQt4 import QtGui

class BackTestReciever(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initThread()
        
        
    def initUI(self):
        self.button = QtGui.QPushButton('Start', self)
        self.button.clicked.connect(self.onClick)
        self.button.move(70, 40)
        self.setWindowTitle('BackTestReciever')
        self.resize(220, 100)
        pass
    
    def initThread(self):
        self._thread = BackTestReceiverThread()
        self._thread.finished.connect(self.NotifyThreadEnd)
        self._thread.receiveData.connect(self.NotifyMsg)
        pass
    
    
    def onClick(self):
        if not self._thread.isRunning():
            self._thread.start()
            self.button.setText('Stop')
        else:
            self._thread.stop()
            #self._thread.quit()
            #self._thread.terminate()        
            self.button.setText('Start')
        pass
    
    def NotifyThreadEnd(self):
        self.button.setText('Start')
        pass
    
    def NotifyMsg(self,row):        
        pass
            
                
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = BackTestReciever()
    wdg.show()
    sys.exit(app.exec_())
