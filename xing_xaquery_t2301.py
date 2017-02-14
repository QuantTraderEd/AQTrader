# -*- coding: utf-8 -*-

from xing_source import SourceQuery


class XAQuery_t2301(SourceQuery):
    """
    KOSPI200 Options Greeks & etc
    """
    def __init__(self):
        super(XAQuery_t2301, self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\t2301.res")
        self.yyyymm = ''
        self.big_mini_code = 'G'
        pass

    def OnSignal(self):
        self.data = []
        data = {}
        data['histmpv'] = self.GetFieldData('T2301OutBlock', 'histmpv', 0)
        data['jandatecnt'] = self.GetFieldData('T2301OutBlock', 'jandatecnt', 0)
        data['cimpv'] = self.GetFieldData('T2301OutBlock', 'cimpv', 0)
        data['pimpv'] = self.GetFieldData('T2301OutBlock', 'pimpv', 0)
        data['gmprice'] = self.GetFieldData('T2301OutBlock', 'gmprice', 0)
        data['gmsign'] = self.GetFieldData('T2301OutBlock', 'gmsign', 0)
        data['gmchange'] = self.GetFieldData('T2301OutBlock', 'gmchange', 0)
        data['gmdiff'] = self.GetFieldData('T2301OutBlock', 'gmdiff', 0)
        data['gmvolume'] = self.GetFieldData('T2301OutBlock', 'gmvolume', 0)
        data['gmshcode'] = self.GetFieldData('T2301OutBlock', 'gmshcode', 0)

        self.data.append(data)

        count1 = self.GetBlockCount('T2301OutBlock1')
        count2 = self.GetBlockCount('T2301OutBlock2')

        for i in xrange(count1):
            data = {}
            data['actprice'] = self.GetFieldData('T0441OutBlock1', 'actprice', i)
            data['optcode'] = self.GetFieldData('T0441OutBlock1', 'optcode', i)
            data['price'] = self.GetFieldData('T0441OutBlock1', 'price', i)
            data['sign'] = self.GetFieldData('T0441OutBlock1', 'sign', i)
            data['change'] = self.GetFieldData('T0441OutBlock1', 'change', i)
            data['diff'] = self.GetFieldData('T0441OutBlock1', 'diff', i)
            data['volume'] = self.GetFieldData('T0441OutBlock1', 'volume', i)
            data['iv'] = self.GetFieldData('T0441OutBlock1', 'iv', i)
            data['mgjv'] = self.GetFieldData('T0441OutBlock1', 'mgjv', i)
            data['mgjvupdn'] = self.GetFieldData('T0441OutBlock1', 'mgjvupdn', i)
            data['offerho1'] = self.GetFieldData('T0441OutBlock1', 'offerho1', i)
            data['bidho1'] = self.GetFieldData('T0441OutBlock1', 'bidho1', i)
            data['cvolume'] = self.GetFieldData('T0441OutBlock1', 'cvolume', i)
            data['delt'] = self.GetFieldData('T0441OutBlock1', 'delt', i)
            data['gama'] = self.GetFieldData('T0441OutBlock1', 'gama', i)
            data['vega'] = self.GetFieldData('T0441OutBlock1', 'vega', i)
            data['ceta'] = self.GetFieldData('T0441OutBlock1', 'ceta', i)
            data['rhox'] = self.GetFieldData('T0441OutBlock1', 'rhox', i)
            data['theoryprice'] = self.GetFieldData('T0441OutBlock1', 'theoryprice', i)
            data['impv'] = self.GetFieldData('T0441OutBlock1', 'impv', i)
            data['timevl'] = self.GetFieldData('T0441OutBlock1', 'timevl', i)
            data['jvolume'] = self.GetFieldData('T0441OutBlock1', 'jvolume', i)
            data['parpl'] = self.GetFieldData('T0441OutBlock1', 'parpl', i)
            data['jngo'] = self.GetFieldData('T0441OutBlock1', 'jngo', i)
            data['offerrem1'] = self.GetFieldData('T0441OutBlock1', 'offerrem1', i)
            data['bidrem1'] = self.GetFieldData('T0441OutBlock1', 'bidrem1', i)
            data['open'] = self.GetFieldData('T0441OutBlock1', 'open', i)
            data['high'] = self.GetFieldData('T0441OutBlock1', 'high', i)
            data['low'] = self.GetFieldData('T0441OutBlock1', 'low', i)
            data['atmgubun'] = self.GetFieldData('T0441OutBlock1', 'atmgubun', i)
            data['jisuconv'] = self.GetFieldData('T0441OutBlock1', 'jisuconv', i)
            data['value'] = self.GetFieldData('T0441OutBlock1', 'value', i)
            self.data.append(data)

        for i in xrange(count2):
            data = {}
            data['actprice'] = self.GetFieldData('T0441OutBlock2', 'actprice', i)
            data['optcode'] = self.GetFieldData('T0441OutBlock2', 'optcode', i)
            data['price'] = self.GetFieldData('T0441OutBlock2', 'price', i)
            data['sign'] = self.GetFieldData('T0441OutBlock2', 'sign', i)
            data['change'] = self.GetFieldData('T0441OutBlock2', 'change', i)
            data['diff'] = self.GetFieldData('T0441OutBlock2', 'diff', i)
            data['volume'] = self.GetFieldData('T0441OutBlock2', 'volume', i)
            data['iv'] = self.GetFieldData('T0441OutBlock2', 'iv', i)
            data['mgjv'] = self.GetFieldData('T0441OutBlock2', 'mgjv', i)
            data['mgjvupdn'] = self.GetFieldData('T0441OutBlock2', 'mgjvupdn', i)
            data['offerho1'] = self.GetFieldData('T0441OutBlock2', 'offerho1', i)
            data['bidho1'] = self.GetFieldData('T0441OutBlock2', 'bidho1', i)
            data['cvolume'] = self.GetFieldData('T0441OutBlock2', 'cvolume', i)
            data['delt'] = self.GetFieldData('T0441OutBlock2', 'delt', i)
            data['gama'] = self.GetFieldData('T0441OutBlock2', 'gama', i)
            data['vega'] = self.GetFieldData('T0441OutBlock2', 'vega', i)
            data['ceta'] = self.GetFieldData('T0441OutBlock2', 'ceta', i)
            data['rhox'] = self.GetFieldData('T0441OutBlock2', 'rhox', i)
            data['theoryprice'] = self.GetFieldData('T0441OutBlock2', 'theoryprice', i)
            data['impv'] = self.GetFieldData('T0441OutBlock2', 'impv', i)
            data['timevl'] = self.GetFieldData('T0441OutBlock2', 'timevl', i)
            data['jvolume'] = self.GetFieldData('T0441OutBlock2', 'jvolume', i)
            data['parpl'] = self.GetFieldData('T0441OutBlock2', 'parpl', i)
            data['jngo'] = self.GetFieldData('T0441OutBlock2', 'jngo', i)
            data['offerrem1'] = self.GetFieldData('T0441OutBlock2', 'offerrem1', i)
            data['bidrem1'] = self.GetFieldData('T0441OutBlock2', 'bidrem1', i)
            data['open'] = self.GetFieldData('T0441OutBlock2', 'open', i)
            data['high'] = self.GetFieldData('T0441OutBlock2', 'high', i)
            data['low'] = self.GetFieldData('T0441OutBlock2', 'low', i)
            data['atmgubun'] = self.GetFieldData('T0441OutBlock2', 'atmgubun', i)
            data['jisuconv'] = self.GetFieldData('T0441OutBlock2', 'jisuconv', i)
            data['value'] = self.GetFieldData('T0441OutBlock2', 'value', i)
            self.data.append(data)

        self.Notify()
        pass


