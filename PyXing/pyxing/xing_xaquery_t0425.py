# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:23:05 2013

@author: Administrator
"""

from xing_source import SourceQuery


class XAQuery_t0425(SourceQuery):
    """
    kospi stock now quote & state query
    """    
    def __init__(self):
        super(XAQuery_t0425,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\t0425.res")
        self.cts_ordno_key = ''
        pass

    def OnSignal(self):
        self.data = []
        data = {}
        data['tqty'] = self.GetFieldData('T0425OutBlock','tqty',0)
        data['tcheqty'] = self.GetFieldData('T0425OutBlock','tcheqty',0)
        data['torderm'] = self.GetFieldData('T0425OutBlock','torderm',0)
        data['cmss'] = self.GetFieldData('T0425OutBlock','cmss',0)
        data['tamt'] = self.GetFieldData('T0425OutBlock','tamt',0)
        data['tmdamt'] = self.GetFieldData('T0425OutBlock','tmdamt',0)
        data['tax'] = self.GetFieldData('T0425OutBlock','tax',0)
        data['cts_ordno'] = self.GetFieldData('T0425OutBlock','cts_ordno',0)    # consecutive view key

        self.cts_ordno_key = data['cts_ordno']
        self.data.append(data)

        nCount = self.GetBlockCount('T0425OutBlock1')                
        for i in xrange(nCount):        
            data = {}
            data['ordno'] = self.GetFieldData('T0425OutBlock1','ordno',i)
            data['expcode'] = self.GetFieldData('T0425OutBlock1','expcode',i)
            data['medosu'] = self.GetFieldData('T0425OutBlock1','medosu',i)
            data['qty'] = self.GetFieldData('T0425OutBlock1','qty',i)
            data['price'] = self.GetFieldData('T0425OutBlock1','price',i)
            data['cheqty'] = self.GetFieldData('T0425OutBlock1','cheqty',i)
            data['cheprice'] = self.GetFieldData('T0425OutBlock1','cheprice',i)
            data['orderem'] = self.GetFieldData('T0425OutBlock1','orderem',i)
            data['cfmqty'] = self.GetFieldData('T0425OutBlock1','cfmqty',i)
            data['status'] = self.GetFieldData('T0425OutBlock1','status',i)
            data['ordgb'] = self.GetFieldData('T0425OutBlock1','ordgb',i)
            data['ordtime'] = self.GetFieldData('T0425OutBlock1','ordtime',i)
            data['ordermtd'] = self.GetFieldData('T0425OutBlock1','ordermtd',i)
            data['sysprocseq'] = self.GetFieldData('T0425OutBlock1','sysprocseq',i)
            data['hogagb'] = self.GetFieldData('T0425OutBlock1','hogagb',i)
            data['price1'] = self.GetFieldData('T0425OutBlock1','price1',i)
            data['orggb'] = self.GetFieldData('T0425OutBlock1','orggb',i)
            data['singb'] = self.GetFieldData('T0425OutBlock1','singb',i)
            data['loandt'] = self.GetFieldData('T0425OutBlock1','loandt',i)            

            self.data.append(data)

        self.Notify()
        pass
