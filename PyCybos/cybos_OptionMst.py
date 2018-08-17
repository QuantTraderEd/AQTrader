# -*- coding: utf-8 -*-
"""
Created on Sat May 31 02:19:23 2014

@author: assa
"""

from cybos_source import Source

class OptionMst(Source):
    """ request future current state """
    def __init__(self, code = None):
        super(OptionMst, self).__init__('Dscbo1.OptionMst.1')
        self.type = 'TAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(119): self.data.append(self.com.GetHeaderValue(i))
        #for debug
        self.Notify()
        pass