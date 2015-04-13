# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 15:14:13 2015

@author: assa
"""
import pdb
import pandas as pd
from BackTestReceiver_Thread import BackTestReceiverThread
from OptionViewerPlot import OptionViewerPlotDlg
from PyQt4 import QtGui

class BackTestReciever(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initThread()
        
        
    def initUI(self):
        self.button = QtGui.QPushButton('Start', self)
        self.buttonPlot = QtGui.QPushButton('Plot', self)
        self.button.clicked.connect(self.onClick)
        self.buttonPlot.clicked.connect(self.onPlotClick)
        self.button.move(80, 30)
        self.buttonPlot.move(80, 60)
        self.setWindowTitle('BackTestReciever')
        self.resize(240, 110)
        
        self._OptionVeiwerPlotDlg = OptionViewerPlotDlg()
        pass
    
    def initThread(self):
        self._thread = BackTestReceiverThread()
        self._thread.finished.connect(self.NotifyThreadEnd)
        self._thread.updateImVol.connect(self.NotifyUpdateImVol)
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
    
    def onPlotClick(self):
        if not self._OptionVeiwerPlotDlg.isVisible():
            self._OptionVeiwerPlotDlg.show()
            #self._OptionVeiwerPlotDlg.exec_()
            
        pass
    
    def NotifyThreadEnd(self):
        self.button.setText('Start')
        pass
    
    def NotifyMsg(self,row):        
        pass
    
    
    def NotifyUpdateImVol(self,df_imvol):
        print 'receive df_imvol'
        xdata = df_imvol['Strike']
        data = df_imvol['ImVol']
        self._OptionVeiwerPlotDlg.plot(xdata, data)
        pass
            
                
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = BackTestReciever()
    wdg.show()
    sys.exit(app.exec_())
