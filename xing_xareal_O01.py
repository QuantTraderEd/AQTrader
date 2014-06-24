# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 09:59:21 2014

@author: assa
"""

from xing_source import SourceReal

class XAReal_O01(SourceReal):
    """
    kospi200 futures&options normal order ack real time receive
    """       
    def __init__(self,shcode=None,DataType='dictionary'):
        super(XAReal_O01,self).__init__("XA_DataSet.XAReal")
        self.LoadFromResFile("Res\\O01.res")
        self.shcode = shcode
        self.DataType = DataType 
        pass
    def OnSignal(self):
        if self.DataType == 'dictionary':
            self.data = {}
            self.data['lineseq'] = self.GetFieldData('OutBlock','lineseq')
            self.data['accno'] = self.GetFieldData('OutBlock','accno')
            self.data['user'] = self.GetFieldData('OutBlock','user')
            self.data['len'] = self.GetFieldData('OutBlock','len')
            self.data['gubun'] = self.GetFieldData('OutBlock','gubun')
            self.data['compress'] = self.GetFieldData('OutBlock','compress')
            self.data['encrypt'] = self.GetFieldData('OutBlock','encrypt')
            self.data['offset'] = self.GetFieldData('OutBlock','offset')
            self.data['trcode'] = self.GetFieldData('OutBlock','trcode')                    
            self.data['compid'] = self.GetFieldData('OutBlock','compid')      
            self.data['userid'] = self.GetFieldData('OutBlock','userid')      
            self.data['media'] = self.GetFieldData('OutBlock','media')      
            self.data['ifid'] = self.GetFieldData('OutBlock','ifid')      
            self.data['seq'] = self.GetFieldData('OutBlock','seq')      
            self.data['trid'] = self.GetFieldData('OutBlock','trid')      
            self.data['pubip'] = self.GetFieldData('OutBlock','pubip')      
            self.data['prvip'] = self.GetFieldData('OutBlock','prvip')      
            self.data['pcbpno'] = self.GetFieldData('OutBlock','pcbpno')      
            self.data['bpno'] = self.GetFieldData('OutBlock','bpno')      
            self.data['termno'] = self.GetFieldData('OutBlock','termno')      
            self.data['lang'] = self.GetFieldData('OutBlock','lang')      
            self.data['proctm'] = self.GetFieldData('OutBlock','proctm')      
            self.data['msgcode'] = self.GetFieldData('OutBlock','msgcode')      
            self.data['outgu'] = self.GetFieldData('OutBlock','outgu')      
            self.data['compreq'] = self.GetFieldData('OutBlock','compreq')      
            self.data['funckey'] = self.GetFieldData('OutBlock','funckey')      
            self.data['reqcnt'] = self.GetFieldData('OutBlock','reqcnt')      
            self.data['filler'] = self.GetFieldData('OutBlock','filler')      
            self.data['cont'] = self.GetFieldData('OutBlock','cont')      
            self.data['contkey'] = self.GetFieldData('OutBlock','contkey')      
            self.data['varlen'] = self.GetFieldData('OutBlock','varlen')      
            self.data['varhdlen'] = self.GetFieldData('OutBlock','varhdlen')      
            self.data['varmsglen'] = self.GetFieldData('OutBlock','varmsglen')      
            self.data['trsrc'] = self.GetFieldData('OutBlock','trsrc')      
            self.data['eventid'] = self.GetFieldData('OutBlock','eventid')      
            self.data['ifinfo'] = self.GetFieldData('OutBlock','ifinfo')      
            self.data['filler1'] = self.GetFieldData('OutBlock','filler1')      
            self.data['trcode1'] = self.GetFieldData('OutBlock','trcode1')    
            self.data['firmno'] = self.GetFieldData('OutBlock','firmno')    
            self.data['acntno'] = self.GetFieldData('OutBlock','acntno')    
            self.data['acntno1'] = self.GetFieldData('OutBlock','acntno1')    
            self.data['acntnm'] = self.GetFieldData('OutBlock','acntnm')    
            self.data['brnno'] = self.GetFieldData('OutBlock','brnno')    
            self.data['ordmktcode'] = self.GetFieldData('OutBlock','ordmktcode')    
            self.data['ordno1'] = self.GetFieldData('OutBlock','ordno1')    
            self.data['ordno'] = self.GetFieldData('OutBlock','ordno')    
            self.data['orgordno'] = self.GetFieldData('OutBlock','orgordno')    
            self.data['prntordno'] = self.GetFieldData('OutBlock','prntordno')    
            self.data['prntordno1'] = self.GetFieldData('OutBlock','prntordno1')    
            self.data['isuno'] = self.GetFieldData('OutBlock','isuno')    
            self.data['fnolsuno'] = self.GetFieldData('OutBlock','fnolsuno')    
            self.data['fnolsunm'] = self.GetFieldData('OutBlock','fnolsunm')    
            self.data['pdgrpcode'] = self.GetFieldData('OutBlock','pdgrpcode')    
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
            self.Notify()
        pass
