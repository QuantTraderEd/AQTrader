# -*- coding: utf-8 -*-
"""
Created on Fri Jan 09 21:27:33 2014

@author: assa
"""

from xing_source import SourceQuery

class XAQuery_CEXAQ21100(SourceQuery):
    """
    kospi eurex options now quote & state query
    """
    def __init__(self):
        super(XAQuery_CEXAQ21100,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\CEXAQ21100.res")
        pass

    def OnSignal(self):
        self.data = []
        data1 = {}
        data2 = {}
        data1['RecCnt'] = self.GetFieldData('CEXAQ21100OutBlock1','RecCnt',0)
        data1['ChoicInptTpCode'] = self.GetFieldData('CEXAQ21100OutBlock1','ChoicInptTpCode',0)
        data1['AcntNo'] = self.GetFieldData('CEXAQ21100OutBlock1','AcntNo',0)
        data1['Pwd'] = self.GetFieldData('CEXAQ21100OutBlock1','Pwd',0)
        data1['PrdtExecTpCode'] = self.GetFieldData('CEXAQ21100OutBlock1','PrdtExecTpCode',0)
        data1['StnlnSeqTp'] = self.GetFieldData('CEXAQ21100OutBlock1','StnlnSeqTp',0)

        data2['RecCnt'] = self.GetFieldData('CEXAQ21100OutBlock2','RecCnt',0)
        data2['AcntNm'] = self.GetFieldData('CEXAQ21100OutBlock2','AcntNm',0)
        data2['OrdQty'] = self.GetFieldData('CEXAQ21100OutBlock2','OrdQty',0)
        data2['ExecQty'] = self.GetFieldData('CEXAQ21100OutBlock2','ExecQty',0)

        self.data.append(data1)
        self.data.append(data2)


        nCount = self.GetBlockCount('CEXAQ21100OutBlock3')
        for i in xrange(nCount):
            data3 = {}
            data3['AcntNo1'] = self.GetFieldData('CEXAQ21100OutBlock3','AcntNo1',i)
            data3['OrdDt'] = self.GetFieldData('CEXAQ21100OutBlock3','OrdDt',i)
            data3['OrdNo'] = self.GetFieldData('CEXAQ21100OutBlock3','OrdNo',i)
            data3['OrgOrdNo'] = self.GetFieldData('CEXAQ21100OutBlock3','OrgOrdNo',i)
            data3['OrdTime'] = self.GetFieldData('CEXAQ21100OutBlock3','OrdTime',i)
            data3['FnoIsuNo'] = self.GetFieldData('CEXAQ21100OutBlock3','FnoIsuNo',i)
            data3['IsuNm'] = self.GetFieldData('CEXAQ21100OutBlock3','IsuNm',i)
            data3['BnsTpNm'] = self.GetFieldData('CEXAQ21100OutBlock3','BnsTpNm',i)
            data3['BnsTpCode'] = self.GetFieldData('CEXAQ21100OutBlock3','BnsTpCode',i)
            data3['MrcTpNm'] = self.GetFieldData('CEXAQ21100OutBlock3','MrcTpNm',i)
            data3['ErxPrcCndiTpCode'] = self.GetFieldData('CEXAQ21100OutBlock3','ErxPrcCndiTpCode',i)
            data3['FnoOrdprcPtnNm'] = self.GetFieldData('CEXAQ21100OutBlock3','FnoOrdprcPtnNm',i)
            data3['OrdCndiPrc'] = self.GetFieldData('CEXAQ21100OutBlock3','OrdCndiPrc',i)
            data3['OrdPrc'] = self.GetFieldData('CEXAQ21100OutBlock3','OrdPrc',i)
            data3['OrdQty'] = self.GetFieldData('CEXAQ21100OutBlock3','OrdQty',i)
            data3['OrdTpNm'] = self.GetFieldData('CEXAQ21100OutBlock3','OrdTpNm',i)
            data3['ExecPrc'] = self.GetFieldData('CEXAQ21100OutBlock3','ExecPrc',i)
            data3['ExecQty'] = self.GetFieldData('CEXAQ21100OutBlock3','ExecQty',i)
            data3['UnercQty'] = self.GetFieldData('CEXAQ21100OutBlock3','UnercQty',i)
            data3['CommdaCode'] = self.GetFieldData('CEXAQ21100OutBlock3','CommdaCode',i)
            data3['CommdaNm'] = self.GetFieldData('CEXAQ21100OutBlock3','CommdaNm',i)
            self.data.append(data3)

        self.Notify()
        pass

