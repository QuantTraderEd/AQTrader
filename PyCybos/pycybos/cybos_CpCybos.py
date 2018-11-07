# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 16:41:44 2013

@author: Administrator
"""

from cybos_source import Source


class CpCybos(Source):

    def __init__(self):
        super(CpCybos, self).__init__('CpUtil.CpCybos.1')
        pass

    def IsConnect(self):
        return self.com.IsConnect

    def ServerType(self):
        """
        @return: 0-연결끊김, 1-cybosplus, 2-HTS 보통서버(cybosplus 서버제외)
        """
        return self.com.ServerType

    def GetLimitRemainCount(self, limitType):
        """
        :param limitType:
            LT_NONTRADE_REQUEST = 1 # 주문관련 RQ 요청
            LT_SUBSCRIBE        = 2 # 시세관련 RQ 요청
            LT_TRADE_REQUEST    = 0 # 시세관련 SB
        :return: remain count
        """
        return self.com.GetLimitRemainCount(limitType)

    def PlusDisconnect(self):
        """
        Cybos PLUS Termination Signal
        """
        return self.com.PlusDisconnect()

    def OnDisConnect(self):
        return True
