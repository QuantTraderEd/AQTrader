# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 15:57:54 2013

@author: Administrator
"""

from cybos_source import Source

class StockCur(Source):
    """ subscribe stock trade tick """
    def __init__(self, code = None):
        super(StockCur, self).__init__('Dscbo1.StockCur.1')
        self.type = 'TAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(29): self.data.append(self.com.GetHeaderValue(i))
        #for debug
        self.Notify()
        pass