# -*- coding: utf-8 -*-

from xing_source import SourceReal


class XAReal_I5_(SourceReal):
    """
    kospi200 ETF NAV
    """
    def __init__(self,shcode=None,DataType='dictionary'):
        super(XAReal_I5_,self).__init__("XA_DataSet.XAReal")
        self.LoadFromResFile("Res\\I5_.res")
        self.shcode = shcode
        self.DataType = DataType 
        pass

    def OnSignal(self):
        if self.DataType == 'dictionary':
            self.data = {}
            self.data['time'] = self.GetFieldData('OutBlock','time')
            self.data['price'] = self.GetFieldData('OutBlock','price')
            self.data['sign'] = self.GetFieldData('OutBlock','sign')            
            self.data['change'] = self.GetFieldData('OutBlock','change')
            self.data['volume'] = self.GetFieldData('OutBlock','volume')
            self.data['navdiff'] = self.GetFieldData('OutBlock','navdiff')
            self.data['nav'] = self.GetFieldData('OutBlock','nav')
            self.data['navchange'] = self.GetFieldData('OutBlock','navchange')
            self.data['crate'] = self.GetFieldData('OutBlock','crate')
            self.data['grate'] = self.GetFieldData('OutBlock','grate')
            self.data['jisu'] = self.GetFieldData('OutBlock','jisu')
            self.data['jichange'] = self.GetFieldData('OutBlock','jichange')
            self.data['jirate'] = self.GetFieldData('OutBlock','jirate')
            self.data['shcode'] = self.GetFieldData('OutBlock','shcode')
            self.Notify()
        elif self.DataType == 'list':
            self.data = []
            self.data.append(self.GetFieldData('OutBlock','time'))
            self.data.append(self.GetFieldData('OutBlock','price'))
            self.data.append(self.GetFieldData('OutBlock','sign'))            
            self.data.append(self.GetFieldData('OutBlock','change'))
            self.data.append(self.GetFieldData('OutBlock','volume'))
            self.data.append(self.GetFieldData('OutBlock','navdiff'))
            self.data.append(self.GetFieldData('OutBlock','nav'))
            self.data.append(self.GetFieldData('OutBlock','navchange'))
            self.data.append(self.GetFieldData('OutBlock','crate'))
            self.data.append(self.GetFieldData('OutBlock','grate'))
            self.data.append(self.GetFieldData('OutBlock','jisu'))
            self.data.append(self.GetFieldData('OutBlock','jichange'))
            self.data.append(self.GetFieldData('OutBlock','jirate'))
            self.data.append(self.GetFieldData('OutBlock','shcode'))
            self.Notify()
        pass
