# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 12:05:48 2013

@author: Administrator
"""

from cybos_source import Source

class StockMst(Source):
    """ request stock current state data """
    def __init__(self, code = None):
        super(StockMst, self).__init__('Dscbo1.StockMst.1')
        self.type = 'TAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(71): self.data.append(self.com.GetHeaderValue(i))
        #for debug
        self.Notify()
        pass