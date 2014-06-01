# -*- coding: utf-8 -*-
"""
Created on Thu Dec 05 16:48:02 2013

@author: Administrator
"""

from cybos_source import Source

class StockUniCur(Source):
    """ subscribe stock after market tick """
    def __init__(self, code=None):
        super(StockUniCur, self).__init__('CpSysDib.StockUniCur.1')
        self.type = 'TAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(22): self.data.append(self.com.GetHeaderValue(i))
        self.Notify()
        pass