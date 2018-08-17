# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 22:39:07 2013

@author: assa
"""

from xing_source import SourceQuery

class XAQuery_t9943(SourceQuery):
    """
    kospi200 futures code master query
    """
    def __init__(self):
        super(XAQuery_t9943,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\t9943.res")
        pass
    def OnSignal(self):
        self.data = []
        num = self.GetBlockCount('T9943OutBlock')
        for i in range(num):
            futurecode = {}
            futurecode['hname'] = self.GetFieldData('T9943OutBlock','hname',i)
            futurecode['shcode'] = self.GetFieldData('T9943OutBlock','shcode',i)
            futurecode['expcode'] = self.GetFieldData('T9943OutBlock','expcode',i)
            self.data.append(futurecode)
        self.Notify()
        pass