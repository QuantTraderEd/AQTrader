# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:23:05 2013

@author: Administrator
"""

from xing_source import SourceQuery

class XAQuery_t0424(SourceQuery):
    """
    kospi stock now open position query
    """    
    def __init__(self):
        super(XAQuery_t0424,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\t0424.res")
        self.cts_expcode_key = ''
        pass
    
    def OnSignal(self):
        self.data = []
        data = {}
        data['sumamt'] = self.GetFieldData('T0424OutBlock','sumamt',0)
        data['dtsunik'] = self.GetFieldData('T0424OutBlock','dtsunik',0)
        data['sumamt1'] = self.GetFieldData('T0424OutBlock','sumamt1',0)
        data['cts_expcode'] = self.GetFieldData('T0424OutBlock','cts_expcode',0)    # consecutive view key
        data['tappamt'] = self.GetFieldData('T0424OutBlock','tappamt',0)
        data['tdtsunik'] = self.GetFieldData('T0424OutBlock','tdtsunik',0)
        
        self.cts_expcode_key = data['cts_expcode']
        self.data.append(data)
        
        nCount = self.GetBlockCount('T0424OutBlock1')                
        for i in xrange(nCount):        
            data = {}
            data['expcode'] = self.GetFieldData('T0424OutBlock1','expcode',i)
            data['jangb'] = self.GetFieldData('T0424OutBlock1','jangb',i)
            data['janqty'] = self.GetFieldData('T0424OutBlock1','janqty',i)
            data['mdposqt'] = self.GetFieldData('T0424OutBlock1','mdposqt',i)
            data['pamt'] = self.GetFieldData('T0424OutBlock1','pamt',i)
            data['mamt'] = self.GetFieldData('T0424OutBlock1','mamt',i)
            data['sinamt'] = self.GetFieldData('T0424OutBlock1','sinamt',i)
            data['lastdt'] = self.GetFieldData('T0424OutBlock1','lastdt',i)
            data['msat'] = self.GetFieldData('T0424OutBlock1','msat',i)
            data['mpms'] = self.GetFieldData('T0424OutBlock1','mpms',i)
            data['mdat'] = self.GetFieldData('T0424OutBlock1','mdat',i)
            data['mpmd'] = self.GetFieldData('T0424OutBlock1','mpmd',i)
            data['jsat'] = self.GetFieldData('T0424OutBlock1','jsat',i)
            data['jpms'] = self.GetFieldData('T0424OutBlock1','jpms',i)
            data['jdat'] = self.GetFieldData('T0424OutBlock1','jdat',i)
            data['jpmd'] = self.GetFieldData('T0424OutBlock1','jpmd',i)
            data['sysprocseq'] = self.GetFieldData('T0424OutBlock1','sysprocseq',i)
            data['loandt'] = self.GetFieldData('T0424OutBlock1','loandt',i)
            data['hname'] = self.GetFieldData('T0424OutBlock1','hname',i)
            data['marketgb'] = self.GetFieldData('T0424OutBlock1','marketgb',i)
            data['jonggb'] = self.GetFieldData('T0424OutBlock1','jonggb',i)
            data['janrt'] = self.GetFieldData('T0424OutBlock1','janrt',i)
            data['price'] = self.GetFieldData('T0424OutBlock1','price',i)
            data['appamt'] = self.GetFieldData('T0424OutBlock1','appamt',i)
            data['dtsunik'] = self.GetFieldData('T0424OutBlock1','dtsunik',i)
            data['sunikrt'] = self.GetFieldData('T0424OutBlock1','sunikrt',i)
            data['fee'] = self.GetFieldData('T0424OutBlock1','fee',i)
            data['tax'] = self.GetFieldData('T0424OutBlock1','tax',i)
            data['sininter'] = self.GetFieldData('T0424OutBlock1','sininter',i)
            self.data.append(data)
            
            
        self.Notify()
        pass
        
        
        
        