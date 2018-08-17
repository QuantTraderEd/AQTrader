# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 12:17:23 2013

@author: Administrator
"""

from cybos_source import Source

class StockMst2(Source):
    """ 
    request multi stock current state data 
    shcode style A003540,A000060,A000010 MAX 110
    """
    def __init__(self, code = None):
        super(StockMst2, self).__init__('Dscbo1.StockMst2.1')
        self.type = 'TAQ'
        self.data = None
        self.count = 0
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        self.count = self.com.GetHeaderValue(0)        
        for i in xrange(int(self.count)):
            for j in xrange(30): 
                self.data.append(self.com.GetDataValue(j,i))
                #for debug
        self.Notify()
        pass