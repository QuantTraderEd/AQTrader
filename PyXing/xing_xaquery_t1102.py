# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 19:43:26 2013

@author: Administrator
"""

from xing_source import SourceQuery

class XAQuery_t1102(SourceQuery):
    """
    kospi stock now quote & state query
    """    
    def __init__(self):
        super(XAQuery_t1102,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\t1102.res")
        pass
    def OnSignal(self):
        self.data = {}
        self.data['hname'] = self.GetFieldData('T1102OutBlock','hname',0)
        self.data['price'] = self.GetFieldData('T1102OutBlock','price',0)
        self.data['sign'] = self.GetFieldData('T1102OutBlock','sign',0)
        self.data['change'] = self.GetFieldData('T1102OutBlock','change',0)
        self.data['diff'] = self.GetFieldData('T1102OutBlock','diff',0)
        self.data['volume'] = self.GetFieldData('T1102OutBlock','volume',0)
        self.data['recprice'] = self.GetFieldData('T1102OutBlock','reprice',0)
        self.data['avg'] = self.GetFieldData('T1102OutBlock','avg',0)
        self.data['uplmtprice'] = self.GetFieldData('T1102OutBlock','uplmtprice',0)
        self.data['dnlmtprice'] = self.GetFieldData('T1102OutBlock','dnlmtprice',0)
        self.data['jnilvolume'] = self.GetFieldData('T1102OutBlock','jnilvolume',0)
        self.data['volumediff'] = self.GetFieldData('T1102OutBlock','volumediff',0)
        self.data['open'] = self.GetFieldData('T1102OutBlock','open',0)
        self.data['opentime'] = self.GetFieldData('T1102OutBlock','opentime',0)
        self.data['high'] = self.GetFieldData('T1102OutBlock','high',0)
        self.data['hightime'] = self.GetFieldData('T1102OutBlock','hightime',0)
        self.data['low'] = self.GetFieldData('T1102OutBlock','low',0)
        self.data['lowtime'] = self.GetFieldData('T1102OutBlock','lowtime',0)
        self.data['high52w'] = self.GetFieldData('T1102OutBlock','high52w',0)
        self.data['high52wdate'] = self.GetFieldData('T1102OutBlock','high52wdate',0)
        self.data['low52w'] = self.GetFieldData('T1102OutBlock','low52w',0)
        self.data['low52wdate'] = self.GetFieldData('T1102OutBlock','low52wdate',0)
        self.data['exhratio'] = self.GetFieldData('T1102OutBlock','exhratio',0)
        self.data['per'] = self.GetFieldData('T1102OutBlock','per',0)
        self.data['pbrx'] = self.GetFieldData('T1102OutBlock','pbrx',0)
        self.data['listing'] = self.GetFieldData('T1102OutBlock','listing',0)
        self.data['jkrate'] = self.GetFieldData('T1102OutBlock','jkrate',0)
        self.data['memedan'] = self.GetFieldData('T1102OutBlock','memedan',0)
        self.data['offernocd1'] = self.GetFieldData('T1102OutBlock','offernocd1',0)
        self.data['bidnocd1'] = self.GetFieldData('T1102OutBlock','bidnocd1',0)
        self.data['offerno1'] = self.GetFieldData('T1102OutBlock','offerno1',0)
        self.data['bidno1'] = self.GetFieldData('T1102OutBlock','bidno1',0)
        self.data['offernocd2'] = self.GetFieldData('T1102OutBlock','offernocd2',0)
        self.data['bidnocd2'] = self.GetFieldData('T1102OutBlock','bidnocd2',0)
        self.data['offerno2'] = self.GetFieldData('T1102OutBlock','offerno2',0)
        self.data['bidno2'] = self.GetFieldData('T1102OutBlock','bidno2',0)
        
        # continue
        
        self.Notify()
        pass