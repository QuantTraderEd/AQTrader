# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 19:47:13 2013

@author: Administrator
"""

from cybos_source import Source

class CmeCurr(Source):
    """ subscribe index cme futures trade tick """
    def __init__(self, code = None):
        super(CmeCurr, self).__init__('CpSysDib.CmeCurr.1')
        self.type = 'TAQ'
        self.data = None
        if code: self.SetInputValue('0',code)
        pass
    def OnSignal(self):
        self.data = []
        for i in xrange(47): self.data.append(self.com.GetHeaderValue(i))
        #for debug
        self.Notify()
        pass