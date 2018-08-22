# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 22:51:31 2015

@author: assa
"""

from xing_source import SourceQuery

class XAQuery_t2105(SourceQuery):
    """    
    kospi future & option now quote & state query
    """    
    def __init__(self):
        super(XAQuery_t2105,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\t2105.res")
        pass
    def OnSignal(self):
        self.data = {}
        self.data['hname'] = self.GetFieldData('T2105OutBlock','hname',0)
        self.data['price'] = self.GetFieldData('T2105OutBlock','price',0)
        self.data['sign'] = self.GetFieldData('T2105OutBlock','sign',0)
        self.data['change'] = self.GetFieldData('T2105OutBlock','change',0)
        self.data['diff'] = self.GetFieldData('T2105OutBlock','diff',0)
        self.data['volume'] = self.GetFieldData('T2105OutBlock','volume',0)
        self.data['stimeqrt'] = self.GetFieldData('T2105OutBlock','stimeqrt',0)
        self.data['jnilclose'] = self.GetFieldData('T2105OutBlock','jnilclose',0)
        
        self.data['offerho1'] = self.GetFieldData('T2105OutBlock','offerho1',0)
        self.data['bidho1'] = self.GetFieldData('T2105OutBlock','bidho1',0)
        self.data['offerrem1'] = self.GetFieldData('T2105OutBlock','offerrem1',0)
        self.data['bidrem1'] = self.GetFieldData('T2105OutBlock','bidrem1',0)
        self.data['dcnt1'] = self.GetFieldData('T2105OutBlock','dcnt1',0)
        self.data['scnt1'] = self.GetFieldData('T2105OutBlock','scnt1',0)
        
        self.data['offerho2'] = self.GetFieldData('T2105OutBlock','offerho2',0)
        self.data['bidho2'] = self.GetFieldData('T2105OutBlock','bidho2',0)
        self.data['offerrem2'] = self.GetFieldData('T2105OutBlock','offerrem2',0)
        self.data['bidrem2'] = self.GetFieldData('T2105OutBlock','bidrem2',0)
        self.data['dcnt2'] = self.GetFieldData('T2105OutBlock','dcnt2',0)
        self.data['scnt2'] = self.GetFieldData('T2105OutBlock','scnt2',0)
        
        self.data['offerho3'] = self.GetFieldData('T2105OutBlock','offerho3',0)
        self.data['bidho3'] = self.GetFieldData('T2105OutBlock','bidho3',0)
        self.data['offerrem3'] = self.GetFieldData('T2105OutBlock','offerrem3',0)
        self.data['bidrem3'] = self.GetFieldData('T2105OutBlock','bidrem3',0)
        self.data['dcnt3'] = self.GetFieldData('T2105OutBlock','dcnt3',0)
        self.data['scnt3'] = self.GetFieldData('T2105OutBlock','scnt3',0)        
        
        self.data['offerho4'] = self.GetFieldData('T2105OutBlock','offerho4',0)
        self.data['bidho4'] = self.GetFieldData('T2105OutBlock','bidho4',0)
        self.data['offerrem4'] = self.GetFieldData('T2105OutBlock','offerrem4',0)
        self.data['bidrem4'] = self.GetFieldData('T2105OutBlock','bidrem4',0)
        self.data['dcnt4'] = self.GetFieldData('T2105OutBlock','dcnt4',0)
        self.data['scnt4'] = self.GetFieldData('T2105OutBlock','scnt4',0)      
        
        self.data['offerho5'] = self.GetFieldData('T2105OutBlock','offerho5',0)
        self.data['bidho5'] = self.GetFieldData('T2105OutBlock','bidho5',0)
        self.data['offerrem5'] = self.GetFieldData('T2105OutBlock','offerrem5',0)
        self.data['bidrem5'] = self.GetFieldData('T2105OutBlock','bidrem5',0)
        self.data['dcnt5'] = self.GetFieldData('T2105OutBlock','dcnt5',0)
        self.data['scnt5'] = self.GetFieldData('T2105OutBlock','scnt5',0)      
        
        self.data['dvol'] = self.GetFieldData('T2105OutBlock','dvol',0)
        self.data['svol'] = self.GetFieldData('T2105OutBlock','svol',0)
        self.data['toffernum'] = self.GetFieldData('T2105OutBlock','toffernum',0)
        self.data['tbidnum'] = self.GetFieldData('T2105OutBlock','tbidnum',0)
        self.data['time'] = self.GetFieldData('T2105OutBlock','time',0)
        self.data['shcode'] = self.GetFieldData('T2105OutBlock','shcode',0)      
        
        # continue
        
        self.Notify()
        pass