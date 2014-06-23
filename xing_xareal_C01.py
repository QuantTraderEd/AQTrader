# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 21:09:43 2014

@author: assa
"""

from xing_source import SourceReal

class XAReal_C01(SourceReal):
    """
    kospi200 stock normal order ack real time receive
    """       
    def __init__(self,shcode=None,DataType='dictionary'):
        super(XAReal_C01,self).__init__("XA_DataSet.XAReal")
        self.LoadFromResFile("Res\\C01.res")
        self.shcode = shcode
        self.DataType = DataType 
        pass
    def OnSignal(self):
        if self.DataType == 'dictionary':
            self.data = {}
            self.data['lineseq'] = self.GetFieldData('OutBlock','lineseq')
            self.data['accno'] = self.GetFieldData('OutBlock','accno')
            self.data['user'] = self.GetFieldData('OutBlock','user')
            self.data['seq'] = self.GetFieldData('OutBlock','seq')
            self.data['trcode'] = self.GetFieldData('OutBlock','trcode')
            self.data['typecode'] = self.GetFieldData('OutBlock','typecode')
            self.data['memberno'] = self.GetFieldData('OutBlock','memberno')
            self.data['bpno'] = self.GetFieldData('OutBlock','bpno')
            self.data['ordno'] = self.GetFieldData('OutBlock','ordno')
            self.data['orgordno'] = self.GetFieldData('OutBlock','orgordno')
            self.data['expcode'] = self.GetFieldData('OutBlock','expcode')
            self.data['yakseq'] = self.GetFieldData('OutBlock','yakseq')
            self.data['cheprice'] = self.GetFieldData('OutBlock','cheprice')
            self.data['chevol'] = self.GetFieldData('OutBlock','chevol')
            self.Notify()
        elif self.DataType == 'list':
            self.data = []
            self.data.append(self.GetFieldData('OutBlock','lineseq'))
            self.data.append(self.GetFieldData('OutBlock','accno'))
            self.data.append(self.GetFieldData('OutBlock','user'))
            
            self.Notify()
        pass
