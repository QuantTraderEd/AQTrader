# -*- coding: utf-8 -*-

from cybos_source import Source


class FutureJpBid(Source):
    """
    subscribe kospi200 index futures (mini) quote
    """
    def __init__(self, code=None, datatype='list'):
        super(FutureJpBid, self).__init__('CpSysDib.FutureJpBid.1')
        self.type = 'TAQ'
        self.datatype = datatype
        if self.datatype == 'list':
            self.data = []
        elif self.datatype == 'dict':
            self.data = {}
        else:
            self.data = None
        if code: self.SetInputValue('0',code)
        pass

    def OnSignal(self):
        if self.datatype == 'list':
            self.data = []
            for i in xrange(37): self.data.append(self.com.GetHeaderValue(i))
            self.Notify()
        elif self.datatype == 'dict':
            self.data = {}
            for i in xrange(1, 6):
                self.data['Ask%d' % i] = self.com.GetHeaderValue(2 + i - 1)
                self.data['Bid%d' % i] = self.com.GetHeaderValue(19 + i - 1)
                self.data['AskQty%d' % i] = self.com.GetHeaderValue(7 + i - 1)
                self.data['BidQty%d' % i] = self.com.GetHeaderValue(24 + i - 1)
                self.data['AskCnt%d' % i] = self.com.GetHeaderValue(13 + i - 1)
                self.data['BidCnt%d' % i] = self.com.GetHeaderValue(30 + i - 1)

            self.data['TotalAskQty'] = self.com.GetHeaderValue(12)
            self.data['TotalBidQty'] = self.com.GetHeaderValue(29)
            self.data['TotalAskCnt'] = self.com.GetHeaderValue(18)
            self.data['TotalBidCnt'] = self.com.GetHeaderValue(35)
            self.data['ShortCD'] = self.com.GetHeaderValue(0)
            self.Notify()
        pass