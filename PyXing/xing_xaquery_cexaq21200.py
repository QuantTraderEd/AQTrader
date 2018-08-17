# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 14:27:33 2014

@author: assa
"""

from xing_source import SourceQuery

class XAQuery_CEXAQ21200(SourceQuery):
    """
    kospi eurex options account margin
    """
    def __init__(self):
        super(XAQuery_CEXAQ21200,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\CEXAQ21200.res")
        pass

    def OnSignal(self):
        self.data = {}
        self.data['RecCnt1'] = self.GetFieldData('CEXAQ21200OutBlock1','RecCnt',0)
        self.data['AcntNo'] = self.GetFieldData('CEXAQ21200OutBlock1','AcntNo',0)
        self.data['Pwd'] = self.GetFieldData('CEXAQ21200OutBlock1','Pwd',0)
        self.data['QryTp'] = self.GetFieldData('CEXAQ21200OutBlock1','QryTp',0)
        self.data['OrdAmt'] = self.GetFieldData('CEXAQ21200OutBlock1','OrdAmt',0)
        self.data['RatVal'] = self.GetFieldData('CEXAQ21200OutBlock1','RatVal',0)
        self.data['FnoIsuNo'] = self.GetFieldData('CEXAQ21200OutBlock1','FnoIsuNo',0)
        self.data['BnsTpCode'] = self.GetFieldData('CEXAQ21200OutBlock1','BnsTpCode',0)
        self.data['OrdPrc'] = self.GetFieldData('CEXAQ21200OutBlock1','OrdPrc',0)
        self.data['ErxPrcCndiTpCode'] = self.GetFieldData('CEXAQ21200OutBlock1','ErxPrcCndiTpCode',0)
        self.data['RecCnt2'] = self.GetFieldData('CEXAQ21200OutBlock2','RecCnt',0)
        self.data['AcntNm'] = self.GetFieldData('CEXAQ21200OutBlock2','AcntNm',0)
        self.data['QryDt'] = self.GetFieldData('CEXAQ21200OutBlock2','QryDt',0)
        self.data['NowPrc'] = self.GetFieldData('CEXAQ21200OutBlock2','NowPrc',0)
        self.data['OrdAbleQty'] = self.GetFieldData('CEXAQ21200OutBlock2','OrdAbleQty',0)
        self.data['NewOrdAbleQty'] = self.GetFieldData('CEXAQ21200OutBlock2','NewOrdAbleQty',0)
        self.data['LqdtOrdAbleQty'] = self.GetFieldData('CEXAQ21200OutBlock2','LqdtOrdAbleQty',0)
        self.data['UsePreargMgn'] = self.GetFieldData('CEXAQ21200OutBlock2','UsePreargMgn',0)
        self.data['UsePreargMnyMgn'] = self.GetFieldData('CEXAQ21200OutBlock2','UsePreargMnyMgn',0)
        self.data['OrdAbleAmt'] = self.GetFieldData('CEXAQ21200OutBlock2','OrdAbleAmt',0)
        self.data['MnyOrdAbleAmt'] = self.GetFieldData('CEXAQ21200OutBlock2','MnyOrdAbleAmt',0)

        self.Notify()
        pass