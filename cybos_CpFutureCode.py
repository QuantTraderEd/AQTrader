# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 16:47:10 2013

@author: Administrator
"""

from cybos_source import SourceNoEvent

class CpFutureCode(SourceNoEvent):
    FUTURE_CODE     = 0
    FUTURE_NAME     = 1
    def __init__(self):
        super(CpFutureCode, self).__init__('CpUtil.CpFutureCode.1')
        pass
    def CodeToName(self,code):
        return self.com.CodeToName(code)
    def GetCount(self):
        return self.com.GetCount()
    def GetData(self,type_,index):
        return self.com.GetData(type_,index)
    pass