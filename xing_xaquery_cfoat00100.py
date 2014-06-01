# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 20:10:38 2013

@author: Administrator
"""
from xing_source import SourceQuery

class XAQuery_CFOAT00100(SourceQuery):
    """
    kospi200 futures & options normal order
    """
    def __init__(self):
        super(XAQuery_CFOAT00100,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\CFOAT00100.res")
        pass
    def OnSignal(self):                
        self.data = {}
        self.data['blsSystemError'] = self.RecvMsg[0]
        self.data['szMessageCode'] = self.RecvMsg[1]
        self.data['szMessage'] = self.RecvMsg[2]
        
        self.data['RecCnt1'] = self.GetFieldData('CFOAT00100OutBlock1','RecCnt',0)
        self.data['OrdMktCode'] = self.GetFieldData('CFOAT00100OutBlock1','OrdMktCode',0)
        self.data['AcntNo'] = self.GetFieldData('CFOAT00100OutBlock1','AcntNo',0)
        self.data['Pwd'] = self.GetFieldData('CFOAT00100OutBlock1','Pwd',0)
        self.data['FnoIsuNo'] = self.GetFieldData('CFOAT00100OutBlock1','FnoIsuNo',0)
        self.data['BnsTpCode'] = self.GetFieldData('CFOAT00100OutBlock1','BnsTpCode',0)
        self.data['FnoOrdPtnCode'] = self.GetFieldData('CFOAT00100OutBlock1','FnoOrdPtnCode',0)
        self.data['FnoOrdprcPtnCode'] = self.GetFieldData('CFOAT00100OutBlock1','FnoOrdprcPtnCode',0)
        self.data['FnoTrdPtnCode'] = self.GetFieldData('CFOAT00100OutBlock1','FnoTrdPtnCode',0)
        self.data['OrdPrc'] = self.GetFieldData('CFOAT00100OutBlock1','OrdPrc',0)
        self.data['OrdQty'] = self.GetFieldData('CFOAT00100OutBlock1','OrdQty',0)
        self.data['CommdaCode'] = self.GetFieldData('CFOAT00100OutBlock1','CommdaCode',0)
        self.data['DscusBnsCmpltTime'] = self.GetFieldData('CFOAT00100OutBlock1','DscusBnsCmpltTime',0)
        self.data['GrpId'] = self.GetFieldData('CFOAT00100OutBlock1','GrpId',0)
        self.data['OrdSeqno'] = self.GetFieldData('CFOAT00100OutBlock1','OrdSeqno',0)
        self.data['PtflNo'] = self.GetFieldData('CFOAT00100OutBlock1','PtflNo',0)
        self.data['BskNo'] = self.GetFieldData('CFOAT00100OutBlock1','BskNo',0)
        self.data['TrchNo'] = self.GetFieldData('CFOAT00100OutBlock1','TrchNo',0)
        self.data['ItemNo'] = self.GetFieldData('CFOAT00100OutBlock1','ItemNo',0)
        self.data['OpDrtnNo'] = self.GetFieldData('CFOAT00100OutBlock1','OpDrtnNo',0)
        self.data['MgempNo'] = self.GetFieldData('CFOAT00100OutBlock1','MgempNo',0)
        self.data['FundId'] = self.GetFieldData('CFOAT00100OutBlock1','FundId',0)
        self.data['FundOrdNo'] = self.GetFieldData('CFOAT00100OutBlock1','FundOrdNo',0)
        
        self.data['RecCnt2'] = self.GetFieldData('CFOAT00100OutBlock2','RecCnt',0)
        self.data['OrdNo'] = self.GetFieldData('CFOAT00100OutBlock2','OrdNo',0)
        self.data['BrnNm'] = self.GetFieldData('CFOAT00100OutBlock2','BrnNm',0)
        self.data['AcntNm'] = self.GetFieldData('CFOAT00100OutBlock2','AcntNm',0)
        self.data['IsuNm'] = self.GetFieldData('CFOAT00100OutBlock2','IsuNm',0)
        self.data['OrdAbleAmt'] = self.GetFieldData('CFOAT00100OutBlock2','OrdAbleAmt',0)
        self.data['MnyOrdAbleAmt'] = self.GetFieldData('CFOAT00100OutBlock2','MnyOrdAbleAmt',0)
        self.data['OrdMgm'] = self.GetFieldData('CFOAT00100OutBlock2','OrdMgm',0)
        self.data['MnyOrdMgn'] = self.GetFieldData('CFOAT00100OutBlock2','MnyOrdMgn',0)
        self.data['OrdAbleQty'] = self.GetFieldData('CFOAT00100OutBlock2','OrdAbleQty',0)
        self.Notify()
        pass