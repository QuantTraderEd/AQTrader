# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 16:48:41 2013

@author: Administrator
"""

from cybos_source import SourceNoEvent

class CpOptionCode(SourceNoEvent):
    OPTION_CODE     = 0
    OPTION_NAME     = 1
    OPTION_TYPE     = 2
    OPTION_MONTH    = 3
    OPTION_STRIKE   = 4
    def __init__(self):
        super(CpOptionCode, self).__init__('CpUtil.CpOptionCode.1')
        pass
    def CodeToName(self, code):
        return self.com.CodeToName(code)
    def GetCount(self):
        return self.com.GetCount()
    def GetData(self, type_, index):
        return self.com.GetData(type_, index) 