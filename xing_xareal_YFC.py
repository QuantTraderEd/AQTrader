# -*- coding: utf-8 -*-

from xing_source import SourceReal

class XAReal_YFC(SourceReal):
    """
    kospi stock expected auction price real time recieve
    """
    def __init__(self,shcode=None,DataType='dictionary'):
        super(XAReal_YFC,self).__init__("XA_DataSet.XAReal")
        self.LoadFromResFile("Res\\YFC.res")
        self.shcode = shcode
        self.DataType = DataType
        if shcode: self.SetFieldData('InBlock','futcode',shcode)        
        pass    
    def OnSignal(self):
        if self.DataType == 'dictionary':
            self.data = {}
            self.data['ychetime'] = self.GetFieldData('OutBlock','ychetime')
            self.data['yeprice'] = self.GetFieldData('OutBlock','yeprice')
            self.data['jnilysign'] = self.GetFieldData('OutBlock','jnilysign')
            self.data['preychange'] = self.GetFieldData('OutBlock','preychange')
            self.data['jnilydrate'] = self.GetFieldData('OutBlock','jnilydrate')
            self.data['optcode'] = self.GetFieldData('OutBlock','futcode')
            self.Notify()
        elif self.DataType == 'list':
            self.data = []
            self.data.append(self.GetFieldData('OutBlock','ychetime'))
            self.data.append(self.GetFieldData('OutBlock','yeprice'))
            self.data.append(self.GetFieldData('OutBlock','jnilysign'))
            self.data.append(self.GetFieldData('OutBlock','preychange'))
            self.data.append(self.GetFieldData('OutBlock','jnilydrate'))
            self.data.append(self.GetFieldData('OutBlock','futcode'))
            self.Notify()

