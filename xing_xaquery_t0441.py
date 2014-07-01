# -*- coding: utf-8 -*-
"""
Created on Tue Jul 01 11:12:18 2014

@author: assa
"""

from xing_source import SourceQuery

class XAQuery_t0441(SourceQuery):
    """
    kospi futures&options now open position query
    """    
    def __init__(self):
        super(XAQuery_t0441,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\t0441.res")
        self.cts_expcode_key = ''
        pass
    
    def OnSignal(self):
        self.data = []
        data = {}
        data['tdtsunik'] = self.GetFieldData('T0441OutBlock','tdtsunik',0)
        data['cts_expcode'] = self.GetFieldData('T0441OutBlock','cts_expcode',0)
        data['cts_medocd'] = self.GetFieldData('T0441OutBlock','cts_medocd',0)
        data['tappamt'] = self.GetFieldData('T0441OutBlock','tappamt',0)
        data['tsunik'] = self.GetFieldData('T0441OutBlock','tsunik',0)
        
        self.cts_expcode_key = data['cts_expcode']
        self.data.append(data)
        
        nCount = self.GetBlockCount('T0441OutBlock1')                
        for i in xrange(nCount):        
            data = {}
            data['expcode'] = self.GetFieldData('T0441OutBlock1','expcode',i)
            data['medosu'] = self.GetFieldData('T0441OutBlock1','medosu',i)
            data['jqty'] = self.GetFieldData('T0441OutBlock1','jqty',i)
            data['cqty'] = self.GetFieldData('T0441OutBlock1','cqty',i)
            data['pamt'] = self.GetFieldData('T0441OutBlock1','pamt',i)
            data['mamt'] = self.GetFieldData('T0441OutBlock1','mamt',i)
            data['medocd'] = self.GetFieldData('T0441OutBlock1','medocd',i)
            data['dtsunik'] = self.GetFieldData('T0441OutBlock1','dtsunik',i)
            data['sysprocseq'] = self.GetFieldData('T0441OutBlock1','sysprocseq',i)
            data['price'] = self.GetFieldData('T0441OutBlock1','price',i)
            data['appamt'] = self.GetFieldData('T0441OutBlock1','appamt',i)
            data['dtsunik1'] = self.GetFieldData('T0441OutBlock1','dtsunik1',i)
            data['sunikrt'] = self.GetFieldData('T0441OutBlock1','sunikrt',i)
            self.data.append(data)
            
        self.Notify()
        pass
            
            
            
        
        
        
