# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 21:34:42 2017

@author: assa
"""
from xing_source import SourceQuery

class XAQuery_CCEAT00300(SourceQuery):
    """
    kospi200 CME futures cancel order
    """
    def __init__(self):
        super(XAQuery_CCEAT00300,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\CCEAT00300.res")
        self.autotrader_id = "0"
        pass
    
    def OnSignal(self):
        self.data = {}
        self.data['blsSystemError'] = self.RecvMsg[0]
        self.data['szMessageCode'] = self.RecvMsg[1]
        self.data['szMessage'] = self.RecvMsg[2]
        
        self.data['RecCnt'] = self.GetFieldData('CCEAT00300OutBlock1','RecCnt',0)
        self.data['OrdMktCode'] = self.GetFieldData('CCEAT00300OutBlock1','OrdMktCode',0)
        self.data['AcntNo'] = self.GetFieldData('CCEAT00300OutBlock1','AcntNo',0)
        self.data['Pwd'] = self.GetFieldData('CCEAT00300OutBlock1','Pwd',0)
        self.data['FnoIsuNo'] = self.GetFieldData('CCEAT00300OutBlock1','FnoIsuNo',0)
        self.data['FnoOrdPtnCode'] = self.GetFieldData('CCEAT00300OutBlock1','FnoOrdPtnCode',0)
        self.data['OrgOrdNo'] = self.GetFieldData('CCEAT00300OutBlock1','OrgOrdNo',0)
        self.data['CancQty'] = self.GetFieldData('CCEAT00300OutBlock1','CancQty',0)
        self.data['CommdaCode'] = self.GetFieldData('CCEAT00300OutBlock1','CommdaCode',0)
        self.data['DscusBnsCmpltTime'] = self.GetFieldData('CCEAT00300OutBlock1','DscusBnsCmpltTime',0)
        self.data['GrpId'] = self.GetFieldData('CCEAT00300OutBlock1','GrpId',0)
        self.data['OrdSeqno'] = self.GetFieldData('CCEAT00300OutBlock1','OrdSeqno',0)
        self.data['PtfNo'] = self.GetFieldData('CCEAT00300OutBlock1','PtfNo',0)
        self.data['BskNo'] = self.GetFieldData('CCEAT00300OutBlock1','BskNo',0)
        self.data['TrchNo'] = self.GetFieldData('CCEAT00300OutBlock1','TrchNo',0)
        self.data['ItemNo'] = self.GetFieldData('CCEAT00300OutBlock1','ItemNo',0)
        self.data['MgempNo'] = self.GetFieldData('CCEAT00300OutBlock1','MgempNo',0)
        self.data['FundId'] = self.GetFieldData('CCEAT00300OutBlock1','FundId',0)
        self.data['FundOrgOrdNo'] = self.GetFieldData('CCEAT00300OutBlock1','FundOrgOrdNo',0)
        self.data['FundOrdNo'] = self.GetFieldData('CCEAT00300OutBlock1','FundOrdNo',0)
        
        self.data['RecCnt'] = self.GetFieldData('CCEAT00300OutBlock2','RecCnt',0)
        self.data['OrdNo'] = self.GetFieldData('CCEAT00300OutBlock2','OrdNo',0)
        self.data['BrnNm'] = self.GetFieldData('CCEAT00300OutBlock2','BrnNm',0)
        self.data['AcntNm'] = self.GetFieldData('CCEAT00300OutBlock2','AcntNm',0)
        self.data['IsuNm'] = self.GetFieldData('CCEAT00300OutBlock2','IsuNm',0)
        self.data['OrdAbleAmt'] = self.GetFieldData('CCEAT00300OutBlock2','OrdAbleAmt',0)
        self.data['MnyOrdAbleAmt'] = self.GetFieldData('CCEAT00300OutBlock2','MnyOrdAbleAmt',0)
        self.data['OrdMgn'] = self.GetFieldData('CCEAT00300OutBlock2','OrdMgn',0)
        self.data['MnyOrdMgn'] = self.GetFieldData('CCEAT00300OutBlock2','MnyOrdMgn',0)
        self.data['OrdAbleQty'] = self.GetFieldData('CCEAT00300OutBlock2','OrdAbleQty',0)
        self.Notify()
        pass