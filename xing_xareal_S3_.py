# -*- coding: utf-8 -*-


from xing_source import SourceReal

class XAReal_S3_(SourceReal):
    """
    kospi200 stock trade real time receive
    """       
    def __init__(self,shcode=None,DataType='dictionary'):
        super(XAReal_S3_,self).__init__("XA_DataSet.XAReal")
        self.LoadFromResFile("Res\\S3_.res")
        self.shcode = shcode
        self.DataType = DataType     
        if shcode: self.SetFieldData('InBlock','shcode',shcode)
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
            self.data['w_avrg'] = self.GetFieldData('OutBlock','w_avrg')
            self.data['offerho'] = self.GetFieldData('OutBlock','offerho')
            self.data['bidho'] = self.GetFieldData('OutBlock','bidho')
            self.data['status'] = self.GetFieldData('OutBlock','status')
            self.data['jnilvolume'] = self.GetFieldData('OutBlock','jnilvolume')
            self.data['shcode'] = self.GetFieldData('OutBlock','shcode')
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
            self.data.append(self.GetFieldData('OutBlock','w_avrg'))
            self.data.append(self.GetFieldData('OutBlock','offerho'))
            self.data.append(self.GetFieldData('OutBlock','bidho'))
            self.data.append(self.GetFieldData('OutBlock','status'))
            self.data.append(self.GetFieldData('OutBlock','jnilvolume'))
            self.data.append(self.GetFieldData('OutBlock','shcode'))
            self.Notify()
        pass
