# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 13:09:47 2013

@author: Administrator
"""

from cybos_source import Source

class OptionJpBid(Source):
    """ subscribe index option quote """
    def __init__(self, code = None):
        super(OptionJpBid, self).__init__('CpSysDib.OptionJpBid.1')
        self.type = 'TAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(37): self.data.append(self.com.GetHeaderValue(i))
        self.Notify()
    pass