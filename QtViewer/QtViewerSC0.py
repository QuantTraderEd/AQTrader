# -*- coding: utf-8 -*-
"""
Created on Fri Jul 04 22:23:56 2014

@author: assa
"""

from PyQt4 import QtCore
from datetime import datetime

class QtViewerSC0(QtCore.QObject):
    receive = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(QtViewerSC0,self).__init__(parent)
        self.dbname = None
        self.flag = True
        
    def Update(self, subject):
        #print '-' * 20                    
        if type(subject.data).__name__ == 'dict':     
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]
            ordno = subject.data['ordno']                    
        self.flag = False