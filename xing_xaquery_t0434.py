# -*- coding: utf-8 -*-
"""
Created on Tue Jul 01 14:27:33 2014

@author: assa
"""

from xing_source import SourceQuery

class XAQuery_t0434(SourceQuery):
    """
    kospi futures&options now quote & state query
    """    
    def __init__(self):
        super(XAQuery_t0434,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\t0434.res")
        self.cts_ordno_key = ''
        pass
    
    def OnSignal(self):
        self.data = []
        data = {}        
        data['cts_ordno'] = self.GetFieldData('T0434OutBlock','cts_ordno',0)    # consecutive view key
        
        
        self.cts_ordno_key = data['cts_ordno']
        self.data.append(data)
        
        nCount = self.GetBlockCount('T0434OutBlock1')                
        for i in xrange(nCount):        
            data = {}
            data['ordno'] = self.GetFieldData('T0434OutBlock1','ordno',i)
            data['orgordno'] = self.GetFieldData('T0434OutBlock1','orgordno',i)
            data['medosu'] = self.GetFieldData('T0434OutBlock1','medosu',i)
            data['ordgb'] = self.GetFieldData('T0434OutBlock1','ordgb',i)
            data['qty'] = self.GetFieldData('T0434OutBlock1','qty',i)
            data['price'] = self.GetFieldData('T0434OutBlock1','price',i)
            data['cheqty'] = self.GetFieldData('T0434OutBlock1','cheqty',i)
            data['cheprice'] = self.GetFieldData('T0434OutBlock1','cheprice',i)
            data['ordrem'] = self.GetFieldData('T0434OutBlock1','ordrem',i)
            data['status'] = self.GetFieldData('T0434OutBlock1','status',i)
            data['ordtime'] = self.GetFieldData('T0434OutBlock1','ordtime',i)
            data['ordermtd'] = self.GetFieldData('T0434OutBlock1','ordermtd',i)
            data['expcode'] = self.GetFieldData('T0434OutBlock1','expcode',i)
            data['rtcode'] = self.GetFieldData('T0434OutBlock1','rtcode',i)
            data['sysprocseq'] = self.GetFieldData('T0434OutBlock1','sysprocseq',i)
            data['hogatype'] = self.GetFieldData('T0434OutBlock1','hogatype',i)
            
            self.data.append(data)
            
            
        self.Notify()
        pass
