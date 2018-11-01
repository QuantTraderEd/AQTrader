# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 20:08:18 2013

@author: Administrator
"""

from xing_source import SourceReal

class XAReal_FH0(SourceReal):
    """
    kospi200 futures quote tick real time receive
    """
    def __init__(self,shcode=None,DataType='dictionary'):
        super(XAReal_FH0,self).__init__("XA_DataSet.XAReal")
        self.LoadFromResFile("Res\\FH0.res")
        self.shcode = shcode
        self.DataType = DataType  
        if shcode: self.SetFieldData('InBlock','futcode',shcode)
        pass
    def OnSignal(self):
        if self.DataType == 'dictionary':
            self.data = {}
            self.data['hotime'] = self.GetFieldData('OutBlock','hotime')
            self.data['offerho1'] = self.GetFieldData('OutBlock','offerho1')
            self.data['bidho1'] = self.GetFieldData('OutBlock','bidho1')
            self.data['offerrem1'] = self.GetFieldData('OutBlock','offerrem1')
            self.data['bidrem1'] = self.GetFieldData('OutBlock','bidrem1')
            self.data['offercnt1'] = self.GetFieldData('OutBlock','offercnt1')
            self.data['bidcnt1'] = self.GetFieldData('OutBlock','bidcnt1')
            self.data['offerho2'] = self.GetFieldData('OutBlock','offerho2')
            self.data['bidho2'] = self.GetFieldData('OutBlock','bidho2')
            self.data['offerrem2'] = self.GetFieldData('OutBlock','offerrem2')
            self.data['bidrem2'] = self.GetFieldData('OutBlock','bidrem2')
            self.data['offercnt2'] = self.GetFieldData('OutBlock','offercnt2')
            self.data['bidcnt2'] = self.GetFieldData('OutBlock','bidcnt2')
            self.data['offerho3'] = self.GetFieldData('OutBlock','offerho3')
            self.data['bidho3'] = self.GetFieldData('OutBlock','bidho3')
            self.data['offerrem3'] = self.GetFieldData('OutBlock','offerrem3')
            self.data['bidrem3'] = self.GetFieldData('OutBlock','bidrem3')
            self.data['offercnt3'] = self.GetFieldData('OutBlock','offercnt3')
            self.data['bidcnt3'] = self.GetFieldData('OutBlock','bidcnt3')
            self.data['offerho4'] = self.GetFieldData('OutBlock','offerho4')
            self.data['bidho4'] = self.GetFieldData('OutBlock','bidho4')
            self.data['offerrem4'] = self.GetFieldData('OutBlock','offerrem4')
            self.data['bidrem4'] = self.GetFieldData('OutBlock','bidrem4')
            self.data['offercnt4'] = self.GetFieldData('OutBlock','offercnt4')
            self.data['bidcnt4'] = self.GetFieldData('OutBlock','bidcnt4')
            self.data['offerho5'] = self.GetFieldData('OutBlock','offerho5')
            self.data['bidho5'] = self.GetFieldData('OutBlock','bidho5')
            self.data['offerrem5'] = self.GetFieldData('OutBlock','offerrem5')
            self.data['bidrem5'] = self.GetFieldData('OutBlock','bidrem5')
            self.data['offercnt5'] = self.GetFieldData('OutBlock','offercnt5')
            self.data['bidcnt5'] = self.GetFieldData('OutBlock','bidcnt5')       
            self.data['totofferrem'] = self.GetFieldData('OutBlock','totofferrem')
            self.data['totbidrem'] = self.GetFieldData('OutBlock','totbidrem')
            self.data['totoffercnt'] = self.GetFieldData('OutBlock','totoffercnt')
            self.data['totbidcnt'] = self.GetFieldData('OutBlock','totbidcnt')
            self.data['futcode'] = self.GetFieldData('OutBlock','futcode')
            self.data['danhochk'] = self.GetFieldData('OutBlock','danhochk')
            self.data['alloc_gubun'] = self.GetFieldData('OutBlock','alloc_gubun')
            #==================================================================
            for i in xrange(1,6):
                self.data['Ask%d'%i] = self.GetFieldData('OutBlock','offerho%d'%i)
                self.data['Bid%d'%i] = self.GetFieldData('OutBlock','bidho%d'%i)
                self.data['AskQty%d'%i] = self.GetFieldData('OutBlock','offerrem%d'%i)
                self.data['BidQty%d'%i] = self.GetFieldData('OutBlock','bidrem%d'%i)
                self.data['AskCnt%d'%i] = self.GetFieldData('OutBlock','offercnt%d'%i)
                self.data['BidCnt%d'%i] = self.GetFieldData('OutBlock','bidcnt%d'%i)
                
            self.data['TotalAskQty'] = self.GetFieldData('OutBlock','totofferrem')
            self.data['TotalBidQty'] = self.GetFieldData('OutBlock','totbidrem')
            self.data['TotalAskCnt'] = self.GetFieldData('OutBlock','totoffercnt')
            self.data['TotalBidCnt'] = self.GetFieldData('OutBlock','totbidcnt')
            self.data['ShortCD'] = self.GetFieldData('OutBlock','futcode')
            self.Notify()
        elif self.DataType == 'list':
            self.data = []
            self.data.append(self.GetFieldData('OutBlock','hotime'))
            self.data.append(self.GetFieldData('OutBlock','offerho1'))
            self.data.append(self.GetFieldData('OutBlock','bidho1'))
            self.data.append(self.GetFieldData('OutBlock','offerrem1'))
            self.data.append(self.GetFieldData('OutBlock','bidrem1'))
            self.data.append(self.GetFieldData('OutBlock','offercnt1'))
            self.data.append(self.GetFieldData('OutBlock','bidcnt1'))
            self.data.append(self.GetFieldData('OutBlock','offerho2'))
            self.data.append(self.GetFieldData('OutBlock','bidho2'))
            self.data.append(self.GetFieldData('OutBlock','offerrem2'))
            self.data.append(self.GetFieldData('OutBlock','bidrem2'))
            self.data.append(self.GetFieldData('OutBlock','offercnt2'))
            self.data.append(self.GetFieldData('OutBlock','bidcnt2'))
            self.data.append(self.GetFieldData('OutBlock','offerho3'))
            self.data.append(self.GetFieldData('OutBlock','bidho3'))
            self.data.append(self.GetFieldData('OutBlock','offerrem3'))
            self.data.append(self.GetFieldData('OutBlock','bidrem3'))
            self.data.append(self.GetFieldData('OutBlock','offercnt3'))
            self.data.append(self.GetFieldData('OutBlock','bidcnt3'))
            self.data.append(self.GetFieldData('OutBlock','offerho4'))
            self.data.append(self.GetFieldData('OutBlock','bidho4'))
            self.data.append(self.GetFieldData('OutBlock','offerrem4'))
            self.data.append(self.GetFieldData('OutBlock','bidrem4'))
            self.data.append(self.GetFieldData('OutBlock','offercnt4'))
            self.data.append(self.GetFieldData('OutBlock','bidcnt4'))
            self.data.append(self.GetFieldData('OutBlock','offerho5'))
            self.data.append(self.GetFieldData('OutBlock','bidho5'))
            self.data.append(self.GetFieldData('OutBlock','offerrem5'))
            self.data.append(self.GetFieldData('OutBlock','bidrem5'))
            self.data.append(self.GetFieldData('OutBlock','offercnt5'))
            self.data.append(self.GetFieldData('OutBlock','bidcnt5'))       
            self.data.append(self.GetFieldData('OutBlock','totofferrem'))
            self.data.append(self.GetFieldData('OutBlock','totbidrem'))
            self.data.append(self.GetFieldData('OutBlock','totoffercnt'))
            self.data.append(self.GetFieldData('OutBlock','totbidcnt'))
            self.data.append(self.GetFieldData('OutBlock','futcode'))
            self.data.append(self.GetFieldData('OutBlock','danhochk'))
            self.data.append(self.GetFieldData('OutBlock','alloc_gubun'))
            self.Notify()
        pass