# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 13:02:06 2013

@author: Administrator
"""

from cybos_source import Source

class OptionCurOnly(Source):
    """ subscribe option trade tick """
    def __init__(self, code = None):
        super(OptionCurOnly, self).__init__('CpSysDib.OptionCurOnly.1')
        self.type = 'TAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(22): self.data.append(self.com.GetHeaderValue(i))
        # for debug
        self.Notify()
        pass