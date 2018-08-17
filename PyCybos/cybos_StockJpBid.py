# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 16:05:06 2013

@author: Administrator
"""

from cybos_source import Source

class StockJpBid(Source):
    """ subscribe index futures quote  """
    def __init__(self, code = None):
        super(StockJpBid, self).__init__('Dscbo1.StockJpBid.1')
        self.type = 'BAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(69): self.data.append(self.com.GetHeaderValue(i))
        self.Notify()
        pass
    pass