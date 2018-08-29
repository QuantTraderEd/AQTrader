# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 21:09:43 2014

@author: assa
"""

from xing_source import SourceReal


class XAReal_C01(SourceReal):
    """
    kospi200 futures&options order exec real time receive
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
            self.data['ordgb'] = self.GetFieldData('OutBlock','ordgb')
            self.data['chedate'] = self.GetFieldData('OutBlock','chedate')
            self.data['chetime'] = self.GetFieldData('OutBlock','chetime')
            self.data['spdprc1'] = self.GetFieldData('OutBlock','spdprc1')
            self.data['spdprc2'] = self.GetFieldData('OutBlock','spdprc2')
            self.data['dosugb'] = self.GetFieldData('OutBlock','dosugb')
            self.data['accno1'] = self.GetFieldData('OutBlock','accno1')
            self.data['sihogagb'] = self.GetFieldData('OutBlock','sihogagb')
            self.data['jakino'] = self.GetFieldData('OutBlock','jakino')
            self.data['daeyong'] = self.GetFieldData('OutBlock','daeyong')
            self.data['mem_filler'] = self.GetFieldData('OutBlock','mem_filler')
            self.data['mem_accno'] = self.GetFieldData('OutBlock','mem_accno')
            self.data['mem_filler1'] = self.GetFieldData('OutBlock','mem_filler1')
            self.data['filler1'] = self.GetFieldData('OutBlock','filler')            
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
            self.data.append(self.GetFieldData('OutBlock','yakseq'))
            self.data.append(self.GetFieldData('OutBlock','cheprice'))
            self.data.append(self.GetFieldData('OutBlock','chevol'))
            self.data.append(self.GetFieldData('OutBlock','ordgb'))
            self.data.append(self.GetFieldData('OutBlock','chedate'))
            self.data.append(self.GetFieldData('OutBlock','chetime'))
            self.data.append(self.GetFieldData('OutBlock','spdprc1'))
            self.data.append(self.GetFieldData('OutBlock','spdprc2'))
            self.data.append(self.GetFieldData('OutBlock','dosugb'))
            self.data.append(self.GetFieldData('OutBlock','accno1'))
            self.data.append(self.GetFieldData('OutBlock','sihogagb'))  
            self.data.append(self.GetFieldData('OutBlock','jakino'))
            self.data.append(self.GetFieldData('OutBlock','daeyong'))
            self.data.append(self.GetFieldData('OutBlock','mem_filler'))  
            self.data.append(self.GetFieldData('OutBlock','mem_accno'))
            self.data.append(self.GetFieldData('OutBlock','mem_filler1'))
            self.data.append(self.GetFieldData('OutBlock','filler'))
            self.Notify()
        pass
