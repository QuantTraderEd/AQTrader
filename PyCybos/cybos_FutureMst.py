# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 13:16:33 2013

@author: Administrator
"""

from cybos_source import Source

class FutureMst(Source):
    """ request future current state """
    def __init__(self, code = None):
        super(FutureMst, self).__init__('Dscbo1.FutureMst.1')
        self.type = 'TAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(116): self.data.append(self.com.GetHeaderValue(i))
        #for debug
        self.Notify()
        pass