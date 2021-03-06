# -*- coding: utf-8 -*-
"""
Created on Fri Jul 05 10:41:54 2013

@author: Administrator
"""
from xing_source import SourceQuery

class XAQuery_CEXAT11200(SourceQuery):
    """
    kospi200 eurex option cancel order 
    """
    def __init__(self):
        super(XAQuery_CEXAT11200,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\CEXAT11200.res")
        pass
    def OnSignal(self):
        self.data = {}
        self.data['blsSystemError'] = self.RecvMsg[0]
        self.data['szMessageCode'] = self.RecvMsg[1]
        self.data['szMessage'] = self.RecvMsg[2]
        
        self.data['RecCnt1'] = self.GetFieldData('CEXAT11200OutBlock1','RecCnt',0)
        self.data['OrgOrdNo'] = self.GetFieldData('CEXAT11200OutBlock1','OrgOrdNo',0)
        self.data['AcntNo'] = self.GetFieldData('CEXAT11200OutBlock1','AcntNo',0)
        self.data['Pwd'] = self.GetFieldData('CEXAT11200OutBlock1','Pwd',0)
        self.data['FnoIsuNo'] = self.GetFieldData('CEXAT11200OutBlock1','FnoIsuNo',0)
        self.data['BnsTpCode'] = self.GetFieldData('CEXAT11200OutBlock1','BnsTpCode',0)
        self.data['ErxPrcCndiTpCode'] = self.GetFieldData('CEXAT11200OutBlock1','ErxPrcCndiTpCode',0)
        self.data['OrdPrc'] = self.GetFieldData('CEXAT11200OutBlock1','OrdPrc',0)
        self.data['MdfyQty'] = self.GetFieldData('CEXAT11200OutBlock1','MdfyQty',0)
        self.data['OrdCndiPrc'] = self.GetFieldData('CEXAT11200OutBlock1','OrdCndiPrc',0)
        self.data['CommdaCode'] = self.GetFieldData('CEXAT11200OutBlock1','CommdaCode',0)
        
        
        self.data['RecCnt2'] = self.GetFieldData('CEXAT11200OutBlock2','RecCnt',0)
        self.data['OrdNo'] = self.GetFieldData('CEXAT11200OutBlock2','OrdNo',0)
        self.data['BrnNm'] = self.GetFieldData('CEXAT11200OutBlock2','BrnNm',0)
        self.data['AcntNm'] = self.GetFieldData('CEXAT11200OutBlock2','AcntNm',0)
        self.data['IsuNm'] = self.GetFieldData('CEXAT11200OutBlock2','IsuNm',0)
        self.data['OrdAbleAmt'] = self.GetFieldData('CEXAT11200OutBlock2','OrdAbleAmt',0)
        self.data['MnyOrdAbleAmt'] = self.GetFieldData('CEXAT11200OutBlock2','MnyOrdAbleAmt',0)
        self.data['OrdMgn'] = self.GetFieldData('CEXAT11200OutBlock2','OrdMgn',0)
        self.data['MnyOrdMgn'] = self.GetFieldData('CEXAT11200OutBlock2','MnyOrdMgn',0)
        self.data['OrdAbleQty'] = self.GetFieldData('CEXAT11200OutBlock2','OrdAbleQty',0)
        self.Notify()
        pass
