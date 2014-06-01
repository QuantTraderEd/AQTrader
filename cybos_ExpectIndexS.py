# -*- coding: utf-8 -*-
"""
Created on Fri Nov 01 18:38:30 2013

@author: Administrator
"""

from cybos_source import Source

class ExpectIndexS(Source):
    """ subscribe expect index value at open close auction """
    def __init__(self, code = None):
        super(ExpectIndexS, self).__init__('Dscbo1.ExpectIndexS.1')        
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(7): self.data.append(self.com.GetHeaderValue(i))
        #for debug
        self.Notify()
        pass