# -*- coding: utf-8 -*-

from cybos_source import Source


class OptionCurOnly(Source):
    """
    subscribe kospi200 option (mini) trade tick
    """
    def __init__(self, code=None, datatype='list'):
        super(OptionCurOnly, self).__init__('CpSysDib.OptionCurOnly.1')
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
            for i in xrange(29): self.data.append(self.com.GetHeaderValue(i))
            self.Notify()
        if self.datatype == 'dict':
            self.data = {}
            self.data['LastPrice'] = self.com.GetHeaderValue(2)
            self.data['LastQty'] = 0
            self.data['Volume'] = self.com.GetHeaderValue(7)
            self.data['BuySell'] = self.com.GetHeaderValue(21)
            self.data['Ask1'] = self.com.GetHeaderValue(17)
            self.data['Bid1'] = self.com.GetHeaderValue(18)
            self.data['AskQty1'] = self.com.GetHeaderValue(19)
            self.data['BidQty1'] = self.com.GetHeaderValue(20)
            self.data['ShortCD'] = self.com.GetHeaderValue(0)
            self.Notify()
        pass
