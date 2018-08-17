# -*- coding: utf-8 -*-
"""
Created on Thu Dec 05 17:11:04 2013

@author: Administrator
"""

from cybos_source import Source

class StockUniMst(Source):
    def __init__(self, code=None):
        super(StockUniMst, self).__init__('CpSysDib.StockUniMst.1')
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(139): self.data.append(self.com.GetHeaderValue(i))            
        self.Notify()
        pass
            
    
    