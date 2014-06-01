# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 13:08:56 2013

@author: Administrator
"""

from cybos_source import Source

class FutureJpBid(Source):
    """ subscribe index futures quote  """
    def __init__(self, code = None):
        super(FutureJpBid, self).__init__('CpSysDib.FutureJpBid.1')
        self.type = 'BAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(36): self.data.append(self.com.GetHeaderValue(i))
        self.Notify()
        pass
    pass