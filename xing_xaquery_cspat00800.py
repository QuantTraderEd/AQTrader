# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 17:31:24 2013

@author: Administrator
"""

from xing_source import SourceQuery

class XAQuery_CSPAT00800(SourceQuery):
    """
    kospi200 stock cancel order
    """
    def __init__(self):
        super(XAQuery_CSPAT00800,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\CSPAT00800.res")
        pass
    
    def OnSignal(self):
        self.data = {}
        self.data['blsSystemError'] = self.RecvMsg[0]
        self.data['szMessageCode'] = self.RecvMsg[1]
        self.data['szMessage'] = self.RecvMsg[2]
        
        self.data['RecCnt1'] = self.GetFieldData('CSPAT00800OutBlock1','RecCnt',0)        
        self.data['OrgOrdNo'] = self.GetFieldData('CSPAT00800OutBlock1','OrgOrdNo',0)        
        self.data['AcntNo'] = self.GetFieldData('CSPAT00800OutBlock1','AcntNo',0)        
        self.data['InptPwd'] = self.GetFieldData('CSPAT00800OutBlock1','InptPwd',0)        
        self.data['IsuNo'] = self.GetFieldData('CSPAT00800OutBlock1','IsuNo',0)        
        self.data['OrdQty'] = self.GetFieldData('CSPAT00800OutBlock1','OrdQty',0)        
        self.data['CommdaCode'] = self.GetFieldData('CSPAT00800OutBlock1','CommdaCode',0)        
        self.data['GrpId'] = self.GetFieldData('CSPAT00800OutBlock1','GrpId',0)        
        self.data['StrtgCode'] = self.GetFieldData('CSPAT00800OutBlock1','StrtgCode',0)        
        self.data['OrdSeqNo'] = self.GetFieldData('CSPAT00800OutBlock1','OrdSeqNo',0)     
        self.data['PtflNo'] = self.GetFieldData('CSPAT00800OutBlock1','PtflNo',0)
        self.data['BskNo'] = self.GetFieldData('CSPAT00800OutBlock1','BskNo',0)
        self.data['TrchNo'] = self.GetFieldData('CSPAT00800OutBlock1','TrchNo',0)
        self.data['ItemNo'] = self.GetFieldData('CSPAT00800OutBlock1','ItemNo',0)

        
        self.data['RecCnt2'] = self.GetFieldData('CSPAT00800OutBlock2','RecCnt',0)
        self.data['OrdNo'] = self.GetFieldData('CSPAT00800OutBlock2','OrdNo',0)
        self.data['PrntOrdNo'] = self.GetFieldData('CSPAT00800OutBlock2','PrntOrdNo',0)
        self.data['OrdTime'] = self.GetFieldData('CSPAT00800OutBlock2','OrdTime',0)
        self.data['OrdMktCode'] = self.GetFieldData('CSPAT00800OutBlock2','OrdMktCode',0)
        self.data['OrdPtnCode'] = self.GetFieldData('CSPAT00800OutBlock2','OrdPtnCode',0)
        self.data['ShtnIsuNo'] = self.GetFieldData('CSPAT00800OutBlock2','ShtnIsuNo',0)
        self.data['PrgmOrdprcPtnCode'] = self.GetFieldData('CSPAT00800OutBlock2','PrgmOrdprcPtnCode',0)
        self.data['StslOrdprcTpCode'] = self.GetFieldData('CSPAT00800OutBlock2','StslOrdprcTpCode',0)
        self.data['StslAbleYn'] = self.GetFieldData('CSPAT00800OutBlock2','StslAbleYn',0)
        self.data['MgntrnCode'] = self.GetFieldData('CSPAT00800OutBlock2','MgntrnCode',0)
        self.data['LoanDt'] = self.GetFieldData('CSPAT00800OutBlock2','LoanDt',0)
        self.data['CvrgOrdTp'] = self.GetFieldData('CSPAT00800OutBlock2','CvrgOrdTp',0)
        self.data['LpYn'] = self.GetFieldData('CSPAT00800OutBlock2','LpYn',0)
        self.data['MgempNo'] = self.GetFieldData('CSPAT00800OutBlock2','MgempNo',0)
        self.data['BnsTpCode'] = self.GetFieldData('CSPAT00800OutBlock2','BnsTpCode',0)
        self.data['SpareOrdNo'] = self.GetFieldData('CSPAT00800OutBlock2','SpareOrdNo',0)
        self.data['CvrgSeqno'] = self.GetFieldData('CSPAT00800OutBlock2','CvrgSeqno',0)
        self.data['RsvOrdNo'] = self.GetFieldData('CSPAT00800OutBlock2','RsvOrdNo',0)
        self.data['AcntNm'] = self.GetFieldData('CSPAT00800OutBlock2','AcntNm',0)
        self.data['IsuNm'] = self.GetFieldData('CSPAT00800OutBlock2','IsuNm',0)
        self.Notify()
        pass