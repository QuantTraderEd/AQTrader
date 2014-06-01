# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 13:01:00 2013

@author: Administrator
"""

from cybos_source import Source

class FutureCurOnly(Source):
    """ subscribe index futures trade tick """
    def __init__(self, code = None):
        super(FutureCurOnly, self).__init__('Dscbo1.FutureCurOnly.1')
        self.type = 'TAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(31): self.data.append(self.com.GetHeaderValue(i))
        #for debug
        self.Notify()
        pass