# -*- coding: utf-8 -*-
"""
Created on Thu Nov 07 19:13:19 2013

@author: Administrator
"""

from cybos_source import Source

class FOExpectCur(Source):
    """ subscribe futures & options expect price tick """
    def __init__(self):
        super(FOExpectCur, self).__init__('CpSysDib.FOExpectCur.1')            
        self.data = None            
        pass
    def  OnSignal(self):
        self.data = []
        for i in xrange(5): self.data.append(self.com.GetHeaderValue(i))
        # i = 0 data[i] is string (unicode)
        #for debug
        self.Notify()
        pass
