# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 12:10:35 2013

@author: Administrator
"""

from cybos_source import Source

class StockMstM(Source):
    """ 
    request multi stock current state data 
    shcode style A003540A000060A000010 MAX 110
    """
    def __init__(self, code = None):
        super(StockMstM, self).__init__('Dscbo1.StockMstM.1')
        self.type = 'TAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        count = self.com.GetHeaderValue(0)
        for i in xrange(count):
            for j in xrange(12): 
                self.data.append(self.com.GetDataValue(j,i))
                #for debug
        self.Notify()
        pass