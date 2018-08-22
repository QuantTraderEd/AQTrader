# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 20:00:04 2013

@author: Administrator
"""

from xing_source import SourceQuery

class XAQuery_t9944(SourceQuery):
    """
    kospi200 options code master query
    """
    def __init__(self):
        super(XAQuery_t9944,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\t9944.res")
        pass
    def OnSignal(self):
        self.data = []
        num = self.GetBlockCount('T9944OutBlock')
        for i in range(num):
            optioncode = {}
            optioncode['hname'] = self.GetFieldData('T9944OutBlock','hname',i)
            optioncode['shcode'] = self.GetFieldData('T9944OutBlock','shcode',i)
            optioncode['expcode'] = self.GetFieldData('T9944OutBlock','expcode',i)
            self.data.append(optioncode)
        self.Notify()
        pass