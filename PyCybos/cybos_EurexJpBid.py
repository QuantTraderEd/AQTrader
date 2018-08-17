# -*- coding: utf-8 -*-
"""
Created on Sat May 31 14:14:25 2014

@author: assa
"""

from cybos_source import Source

class EurexJpBid(Source):
    """ subscribe index option quote """
    def __init__(self, code = None):
        super(EurexJpBid, self).__init__('CpSysDib.EurexJpbid.1')
        self.type = 'TAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(14): self.data.append(self.com.GetHeaderValue(i))
        self.Notify()
    pass