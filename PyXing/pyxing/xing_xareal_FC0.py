# -*- coding: utf-8 -*-

from xing_source import SourceReal


class XAReal_FC0(SourceReal):
    """
    kospi200 futures trade tick real time receive
    """
    def __init__(self, shcode=None, datatype='dictionary'):
        super(XAReal_FC0, self).__init__("XA_DataSet.XAReal")
        self.LoadFromResFile("Res\\FC0.res")
        self.shcode = shcode
        self.datatype = datatype
        if shcode: self.SetFieldData('InBlock', 'futcode', shcode)
        pass

    def OnSignal(self):
        if self.datatype == 'dictionary':
            self.data = dict()
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
            self.data['mschecnt'] = self.GetFieldData('OutBlock','mschecnt')
            self.data['cpower'] = self.GetFieldData('OutBlock','cpower')
            self.data['offerho1'] = self.GetFieldData('OutBlock','offerho1')
            self.data['bidho1'] = self.GetFieldData('OutBlock','bidho1')
            self.data['openyak'] = self.GetFieldData('OutBlock','openyak')
            self.data['k200jisu'] = self.GetFieldData('OutBlock','k200jisu')
            self.data['theoryprice'] = self.GetFieldData('OutBlock','theoryprice')
            self.data['kasis'] = self.GetFieldData('OutBlock','kasis')
            self.data['sbasis'] = self.GetFieldData('OutBlock','sbasis')
            self.data['ibasis'] = self.GetFieldData('OutBlock','ibasis')
            self.data['openyakcha'] = self.GetFieldData('OutBlock','openyakcha')
            self.data['jgubun'] = self.GetFieldData('OutBlock','jgubun')
            self.data['jnilvolume'] = self.GetFieldData('OutBlock','jnilvolume')
            self.data['futcode'] = self.GetFieldData('OutBlock','futcode')
            #===============================================================
            self.data['LastPrice'] = self.GetFieldData('OutBlock', 'price')
            self.data['LastQty'] = self.GetFieldData('OutBlock', 'cvolume')
            self.data['BuySell'] = self.GetFieldData('OutBlock','cgubun')
            self.data['Ask1'] = self.GetFieldData('OutBlock','offerho1')
            self.data['Bid1'] = self.GetFieldData('OutBlock','bidho1')
            self.data['ShortCD'] = self.GetFieldData('OutBlock','futcode') 
            self.Notify()
        elif self.datatype == 'list':
            self.data = list()
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
            self.data.append(self.GetFieldData('OutBlock','mschecnt'))
            self.data.append(self.GetFieldData('OutBlock','cpower'))
            self.data.append(self.GetFieldData('OutBlock','offerho1'))
            self.data.append(self.GetFieldData('OutBlock','bidho1'))
            self.data.append(self.GetFieldData('OutBlock','openyak'))
            self.data.append(self.GetFieldData('OutBlock','k200jisu'))
            self.data.append(self.GetFieldData('OutBlock','theoryprice'))
            self.data.append(self.GetFieldData('OutBlock','kasis'))
            self.data.append(self.GetFieldData('OutBlock','sbasis'))
            self.data.append(self.GetFieldData('OutBlock','ibasis'))
            self.data.append(self.GetFieldData('OutBlock','openyakcha'))
            self.data.append(self.GetFieldData('OutBlock','jgubun'))
            self.data.append(self.GetFieldData('OutBlock','jnilvolume'))
            self.data.append(self.GetFieldData('OutBlock','futcode'))
            self.Notify()
        pass