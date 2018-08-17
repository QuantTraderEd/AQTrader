# -*- coding: utf-8 -*-
"""
Created on Mon Nov 04 19:30:45 2013

@author: Administrator
"""

from xing_source import SourceReal

class XAReal_YS3(SourceReal):
    """
    kospi stock expected auction price real time recieve
    """
    def __init__(self,shcode=None,DataType='dictionary'):
        super(XAReal_YS3,self).__init__("XA_DataSet.XAReal")
        self.LoadFromResFile("Res\\YS3.res")
        self.shcode = shcode
        self.DataType = DataType
        if shcode: self.SetFieldData('InBlock','shcode',shcode)        
        pass    
    def OnSignal(self):
        if self.DataType == 'dictionary':
            self.data = {}
            self.data['hotime'] = self.GetFieldData('OutBlock','hotime')        
            self.data['yeprice'] = self.GetFieldData('OutBlock','yeprice')
            self.data['yevolume'] = self.GetFieldData('OutBlock','yevolume')
            self.data['jnilysign'] = self.GetFieldData('OutBlock','jnilysign')
            self.data['preychange'] = self.GetFieldData('OutBlock','preychange')
            self.data['jnilydrate'] = self.GetFieldData('OutBlock','jnilydrate')
            self.data['yofferho0'] = self.GetFieldData('OutBlock','yofferho0')
            self.data['ybidho0'] = self.GetFieldData('OutBlock','ybidho0')
            self.data['yofferrem0'] = self.GetFieldData('OutBlock','yofferrem0')
            self.data['ybidrem0'] = self.GetFieldData('OutBlock','ybidrem0')
            self.data['shcode'] = self.GetFieldData('OutBlock','shcode')
            self.Notify()
        elif self.DataType == 'list':
            self.data = []
            self.data.append(self.GetFieldData('OutBlock','hotime'))
            self.data.append(self.GetFieldData('OutBlock','yeprice'))
            self.data.append(self.GetFieldData('OutBlock','yevolume'))
            self.data.append(self.GetFieldData('OutBlock','jnilysign'))
            self.data.append(self.GetFieldData('OutBlock','preychange'))
            self.data.append(self.GetFieldData('OutBlock','jnilydrate'))
            self.data.append(self.GetFieldData('OutBlock','yofferho0'))
            self.data.append(self.GetFieldData('OutBlock','ybidho0'))
            self.data.append(self.GetFieldData('OutBlock','yofferrem0'))
            self.data.append(self.GetFieldData('OutBlock','ybidrem0'))
            self.data.append(self.GetFieldData('OutBlock','shcode'))
            self.Notify()