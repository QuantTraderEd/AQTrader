# -*- coding: utf-8 -*-
"""
Created on Fri Jul 05 08:23:57 2013

@author: Administrator
"""

from xing_source import SourceReal

class XAReal_EH0(SourceReal):
    """
    kospi200 eurex options quote tick real time receive
    """
    def __init__(self,shcode=None,DataType='dictionary'):
        super(XAReal_EH0,self).__init__("XA_DataSet.XAReal")
        self.LoadFromResFile("Res\\EH0.res")
        self.shcode = shcode
        self.DataType = DataType 
        if shcode: self.SetFieldData('InBlock','optcode',shcode)
        pass
    def OnSignal(self):
        if self.DataType == 'dictionary':
            self.data = {}
            self.data['hotime'] = self.GetFieldData('OutBlock','hotime')
            self.data['hotime1'] = self.GetFieldData('OutBlock','hotime1')
            self.data['offerho1'] = self.GetFieldData('OutBlock','offerho1')
            self.data['bidho1'] = self.GetFieldData('OutBlock','bidho1')
            self.data['offerrem1'] = self.GetFieldData('OutBlock','offerrem1')
            self.data['bidrem1'] = self.GetFieldData('OutBlock','bidrem1')
            self.data['offerho2'] = self.GetFieldData('OutBlock','offerho2')
            self.data['bidho2'] = self.GetFieldData('OutBlock','bidho2')
            self.data['offerrem2'] = self.GetFieldData('OutBlock','offerrem2')
            self.data['bidrem2'] = self.GetFieldData('OutBlock','bidrem2')            
            self.data['offerho3'] = self.GetFieldData('OutBlock','offerho3')
            self.data['bidho3'] = self.GetFieldData('OutBlock','bidho3')
            self.data['offerrem3'] = self.GetFieldData('OutBlock','offerrem3')
            self.data['bidrem3'] = self.GetFieldData('OutBlock','bidrem3')
            self.data['totofferrem'] = self.GetFieldData('OutBlock','totofferrem')
            self.data['totbidrem'] = self.GetFieldData('OutBlock','totbidrem')
            self.data['totoffercnt'] = self.GetFieldData('OutBlock','totoffercnt')
            self.data['totbidcnt'] = self.GetFieldData('OutBlock','totbidcnt')
            self.data['optcode'] = self.GetFieldData('OutBlock','optcode')    
            #==================================================================
            for i in xrange(1,4):
                self.data['Ask%d'%i] = self.GetFieldData('OutBlock','offerho%d'%i)
                self.data['Bid%d'%i] = self.GetFieldData('OutBlock','bidho%d'%i)
                self.data['AskQty%d'%i] = self.GetFieldData('OutBlock','offerrem%d'%i)
                self.data['BidQty%d'%i] = self.GetFieldData('OutBlock','bidrem%d'%i)
                
                
            self.data['TotalAskQty'] = self.GetFieldData('OutBlock','totofferrem')
            self.data['TotalBidQty'] = self.GetFieldData('OutBlock','totbidrem')
            self.data['TotalAskCnt'] = self.GetFieldData('OutBlock','totoffercnt')
            self.data['TotalBidCnt'] = self.GetFieldData('OutBlock','totbidcnt')
            self.data['ShortCD'] = self.GetFieldData('OutBlock','optcode')
            self.data['TAQ'] = 'Q'
            self.Notify()
        elif self.DataType == 'list':
            self.data = []
            self.data.append(self.GetFieldData('OutBlock','hotime'))
            self.data.append(self.GetFieldData('OutBlock','hotime1'))
            self.data.append(self.GetFieldData('OutBlock','offerho1'))
            self.data.append(self.GetFieldData('OutBlock','bidho1'))
            self.data.append(self.GetFieldData('OutBlock','offerrem1'))
            self.data.append(self.GetFieldData('OutBlock','bidrem1'))
            #self.data.append(self.GetFieldData('OutBlock','offercnt1'))
            #self.data.append(self.GetFieldData('OutBlock','bidcnt1'))
            self.data.append(self.GetFieldData('OutBlock','offerho2'))
            self.data.append(self.GetFieldData('OutBlock','bidho2'))
            self.data.append(self.GetFieldData('OutBlock','offerrem2'))
            self.data.append(self.GetFieldData('OutBlock','bidrem2'))
            #self.data.append(self.GetFieldData('OutBlock','offercnt2'))
            #self.data.append(self.GetFieldData('OutBlock','bidcnt2'))
            self.data.append(self.GetFieldData('OutBlock','offerho3'))
            self.data.append(self.GetFieldData('OutBlock','bidho3'))
            self.data.append(self.GetFieldData('OutBlock','offerrem3'))
            self.data.append(self.GetFieldData('OutBlock','bidrem3'))
            #self.data.append(self.GetFieldData('OutBlock','offercnt3'))
            #self.data.append(self.GetFieldData('OutBlock','bidcnt3'))
            #self.data.append(self.GetFieldData('OutBlock','offerho4'))
            #self.data.append(self.GetFieldData('OutBlock','bidho4'))
            #self.data.append(self.GetFieldData('OutBlock','offerrem4'))
            #self.data.append(self.GetFieldData('OutBlock','bidrem4'))
            #self.data.append(self.GetFieldData('OutBlock','offercnt4'))
            #self.data.append(self.GetFieldData('OutBlock','bidcnt4'))
            #self.data.append(self.GetFieldData('OutBlock','offerho5'))
            #self.data.append(self.GetFieldData('OutBlock','bidho5'))
            #self.data.append(self.GetFieldData('OutBlock','offerrem5'))
            #self.data.append(self.GetFieldData('OutBlock','bidrem5'))
            #self.data.append(self.GetFieldData('OutBlock','offercnt5'))
            #self.data.append(self.GetFieldData('OutBlock','bidcnt5'))
            self.data.append(self.GetFieldData('OutBlock','totofferrem'))
            self.data.append(self.GetFieldData('OutBlock','totbidrem'))
            self.data.append(self.GetFieldData('OutBlock','totoffercnt'))
            self.data.append(self.GetFieldData('OutBlock','totbidcnt'))
            self.data.append(self.GetFieldData('OutBlock','optcode'))
            #self.data.append(self.GetFieldData('OutBlock','danhochk'))
            #self.data.append(self.GetFieldData('OutBlock','alloc_gubun'))
            self.Notify()
        pass