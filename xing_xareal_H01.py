# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 21:17:45 2014

@author: assa
"""

from xing_source import SourceReal

class XAReal_H01(SourceReal):
    """
    kospi200 futures&options amend & cancl order ack real time receive
    """       
    def __init__(self,shcode=None,DataType='dictionary'):
        super(XAReal_H01,self).__init__("XA_DataSet.XAReal")
        self.LoadFromResFile("Res\\H01.res")
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
            self.data['dosugb'] = self.GetFieldData('OutBlock','dosugb')
            self.data['mocagb'] = self.GetFieldData('OutBlock','mocagb')
            self.data['accno1'] = self.GetFieldData('OutBlock','accno1')
            self.data['qty2'] = self.GetFieldData('OutBlock','qty2')
            self.data['price'] = self.GetFieldData('OutBlock','price')
            self.data['ordgb'] = self.GetFieldData('OutBlock','ordgb')
            self.data['hogagb'] = self.GetFieldData('OutBlock','hogagb')
            self.data['sihogagb'] = self.GetFieldData('OutBlock','sihogagb')
            self.data['tradid'] = self.GetFieldData('OutBlock','tradid')
            self.data['treacode'] = self.GetFieldData('OutBlock','treacode')
            self.data['askcode'] = self.GetFieldData('OutBlock','askcode')
            self.data['creditcode'] = self.GetFieldData('OutBlock','creditcode')
            self.data['jakigb'] = self.GetFieldData('OutBlock','jakigb')
            self.data['trustnum'] = self.GetFieldData('OutBlock','trustnum')
            self.data['ptgb'] = self.GetFieldData('OutBlock','ptgb')
            self.data['substonum'] = self.GetFieldData('OutBlock','substonum')
            self.data['accgb'] = self.GetFieldData('OutBlock','accgb')
            self.data['accmarggb'] = self.GetFieldData('OutBlock','accmarggb')
            self.data['nationcode'] = self.GetFieldData('OutBlock','nationcode')
            self.data['investgb'] = self.GetFieldData('OutBlock','investgb')
            self.data['forecode'] = self.GetFieldData('OutBlock','forecode')
            self.data['medcode'] = self.GetFieldData('OutBlock','medcode')
            self.data['ordid'] = self.GetFieldData('OutBlock','ordid')
            self.data['orddate'] = self.GetFieldData('OutBlock','orddate')
            self.data['rcvtime'] = self.GetFieldData('OutBlock','rcvtime')
            self.data['mem_filler'] = self.GetFieldData('OutBlock','mem_filler')
            self.data['mem_accno'] = self.GetFieldData('OutBlock','mem_accno')
            self.data['mem_filler1'] = self.GetFieldData('OutBlock','mem_filler1')
            self.data['qty'] = self.GetFieldData('OutBlock','qty')
            self.data['autogb'] = self.GetFieldData('OutBlock','autogb')
            self.data['rejcode'] = self.GetFieldData('OutBlock','rejcode')
            self.data['filler'] = self.GetFieldData('OutBlock','filler')
            self.Notify()
        elif self.DataType == 'list':
            self.data = []
            self.data.append(self.GetFieldData('OutBlock','lineseq'))
            self.data.append(self.GetFieldData('OutBlock','accno'))
            self.data.append(self.GetFieldData('OutBlock','user'))
            self.data.append(self.GetFieldData('OutBlock','seq'))
            self.data.append(self.GetFieldData('OutBlock','trcode'))
            self.data.append(self.GetFieldData('OutBlock','typecode'))
            self.data.append(self.GetFieldData('OutBlock','memberno'))
            self.data.append(self.GetFieldData('OutBlock','bpno'))
            self.data.append(self.GetFieldData('OutBlock','ordno'))
            self.data.append(self.GetFieldData('OutBlock','orgordno'))
            self.data.append(self.GetFieldData('OutBlock','expcode'))
            self.data.append(self.GetFieldData('OutBlock','dosugb'))
            self.data.append(self.GetFieldData('OutBlock','mocagb'))
            self.data.append(self.GetFieldData('OutBlock','accno1'))
            self.data.append(self.GetFieldData('OutBlock','qty2'))
            self.data.append(self.GetFieldData('OutBlock','price'))
            self.data.append(self.GetFieldData('OutBlock','ordgb'))
            self.data.append(self.GetFieldData('OutBlock','hogagb'))
            self.data.append(self.GetFieldData('OutBlock','sihogagb'))
            self.data.append(self.GetFieldData('OutBlock','tradid'))
            self.data.append(self.GetFieldData('OutBlock','treacode'))
            self.data.append(self.GetFieldData('OutBlock','askcode'))
            self.data.append(self.GetFieldData('OutBlock','creditcode'))
            self.data.append(self.GetFieldData('OutBlock','jakigb'))
            self.data.append(self.GetFieldData('OutBlock','trustnum'))
            self.data.append(self.GetFieldData('OutBlock','ptgb'))
            self.data.append(self.GetFieldData('OutBlock','substonum'))
            self.data.append(self.GetFieldData('OutBlock','accgb'))
            self.data.append(self.GetFieldData('OutBlock','accmarggb'))
            self.data.append(self.GetFieldData('OutBlock','nationcode'))
            self.data.append(self.GetFieldData('OutBlock','investgb'))
            self.data.append(self.GetFieldData('OutBlock','forecode'))
            self.data.append(self.GetFieldData('OutBlock','medcode'))
            self.data.append(self.GetFieldData('OutBlock','ordid'))
            self.data.append(self.GetFieldData('OutBlock','orddate'))
            self.data.append(self.GetFieldData('OutBlock','rcvtime'))
            self.data.append(self.GetFieldData('OutBlock','mem_filler'))
            self.data.append(self.GetFieldData('OutBlock','mem_accno'))
            self.data.append(self.GetFieldData('OutBlock','mem_filler1'))
            self.data.append(self.GetFieldData('OutBlock','qty'))
            self.data.append(self.GetFieldData('OutBlock','autogb'))
            self.data.append(self.GetFieldData('OutBlock','rejcode'))
            self.data.append(self.GetFieldData('OutBlock','filler'))
            self.Notify()
        pass