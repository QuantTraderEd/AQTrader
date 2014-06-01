# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 20:09:01 2013

@author: Administrator
"""

from xing_source import SourceReal

class XAReal_OC0(SourceReal):
    """
    kospi200 options trade tick real time receive
    """
    def __init__(self,shcode=None,DataType='dictionary'):
        super(XAReal_OC0,self).__init__("XA_DataSet.XAReal")
        self.LoadFromResFile("Res\\OC0.res")
        self.shcode = shcode
        self.DataType = DataType        
        pass
    def OnSignal(self):
        if self.DataType == 'dictionary':
            self.data = {}
            self.data['chetime'] = self.GetFieldData('OutBlock','chetime')      
            self.data['sign'] = self.GetFieldData('OutBlock','sign')            
            self.data['change'] = self.GetFieldData('OutBlock','change')
            self.data['drate'] = self.GetFieldData('OutBlock','drate')
            self.data['price'] = self.GetFieldData('OutBlock','price')
            self.data['open'] = self.GetFieldData('OutBlock','open')
            self.data['high'] = self.GetFieldData('OutBlock','high')
            self.data['low'] = self.GetFieldData('OutBlock','low')
            self.data['cgubun'] = self.GetFieldData('OutBlock','cgubun')
            self.data['cvolume'] = self.GetFieldData('OutBlock','cvolume')
            self.data['volume'] = self.GetFieldData('OutBlock','volume')
            self.data['value'] = self.GetFieldData('OutBlock','value')
            self.data['mdvolume'] = self.GetFieldData('OutBlock','mdvolume')
            self.data['mdchecnt'] = self.GetFieldData('OutBlock','mdchecnt')
            self.data['msvolume'] = self.GetFieldData('OutBlock','msvolume')
            self.data['mschent'] = self.GetFieldData('OutBlock','mschent')
            self.data['cpower'] = self.GetFieldData('OutBlock','cpower')
            self.data['offerho1'] = self.GetFieldData('OutBlock','offerho1')
            self.data['bidho1'] = self.GetFieldData('OutBlock','bidho1')
            self.data['openyak'] = self.GetFieldData('OutBlock','openyak')        
            self.data['eqva'] = self.GetFieldData('OutBlock','eqva')
            self.data['theoryprice'] = self.GetFieldData('OutBlock','theoryprice')
            self.data['impv'] = self.GetFieldData('OutBlock','impv')        
            self.data['openyakcha'] = self.GetFieldData('OutBlock','openyakcha')
            self.data['timevalue'] = self.GetFieldData('OutBlock','timevalue')
            self.data['jgubun'] = self.GetFieldData('OutBlock','jgubun')
            self.data['jnilvolume'] = self.GetFieldData('OutBlock','jnilvolume')
            self.data['optcode'] = self.GetFieldData('OutBlock','optcode')
            self.Notify()
        elif self.DataType == 'list':
            self.data = []
            self.data.append(self.GetFieldData('OutBlock','chetime'))
            self.data.append(self.GetFieldData('OutBlock','sign'))            
            self.data.append(self.GetFieldData('OutBlock','change'))
            self.data.append(self.GetFieldData('OutBlock','drate'))
            self.data.append(self.GetFieldData('OutBlock','price'))
            self.data.append(self.GetFieldData('OutBlock','open'))
            self.data.append(self.GetFieldData('OutBlock','high'))
            self.data.append(self.GetFieldData('OutBlock','low'))
            self.data.append(self.GetFieldData('OutBlock','cgubun'))
            self.data.append(self.GetFieldData('OutBlock','cvolume'))
            self.data.append(self.GetFieldData('OutBlock','volume'))
            self.data.append(self.GetFieldData('OutBlock','value'))
            self.data.append(self.GetFieldData('OutBlock','mdvolume'))
            self.data.append(self.GetFieldData('OutBlock','mdchecnt'))
            self.data.append(self.GetFieldData('OutBlock','msvolume'))
            self.data.append(self.GetFieldData('OutBlock','mschent'))
            self.data.append(self.GetFieldData('OutBlock','cpower'))
            self.data.append(self.GetFieldData('OutBlock','offerho1'))
            self.data.append(self.GetFieldData('OutBlock','bidho1'))
            self.data.append(self.GetFieldData('OutBlock','openyak'))        
            self.data.append(self.GetFieldData('OutBlock','eqva'))
            self.data.append(self.GetFieldData('OutBlock','theoryprice'))
            self.data.append(self.GetFieldData('OutBlock','impv'))        
            self.data.append(self.GetFieldData('OutBlock','openyakcha'))
            self.data.append(self.GetFieldData('OutBlock','timevalue'))
            self.data.append(self.GetFieldData('OutBlock','jgubun'))
            self.data.append(self.GetFieldData('OutBlock','jnilvolume'))
            self.data.append(self.GetFieldData('OutBlock','optcode'))
            self.Notify()
        pass