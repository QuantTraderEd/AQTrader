# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 16:27:33 2014

@author: assa
"""

from xing_source import SourceQuery

class XAQuery_CEXAQ31100(SourceQuery):
    """
    kospi eurex options open position and pnl information
    """
    def __init__(self):
        super(XAQuery_CEXAQ31100,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\CEXAQ31100.res")
        pass

    def OnSignal(self):
        self.data = []
        data1 = {}
        data2 = {}
        data1['RecCnt1'] = self.GetFieldData('CEXAQ31100OutBlock1','RecCnt',0)
        data1['AcntNo'] = self.GetFieldData('CEXAQ31100OutBlock1','AcntNo',0)
        data1['InptPwd'] = self.GetFieldData('CEXAQ31100OutBlock1','InptPwd',0)
        data1['IsuCode'] = self.GetFieldData('CEXAQ31100OutBlock1','IsuCode',0)
        data1['BalEvalTp'] = self.GetFieldData('CEXAQ31100OutBlock1','BalEvalTp',0)
        data1['FutsPrcEvalTp'] = self.GetFieldData('CEXAQ31100OutBlock1','FutsPrcEvalTp',0)

        data2['RecCnt'] = self.GetFieldData('CEXAQ31100OutBlock2','RecCnt',0)
        data2['AcntNo'] = self.GetFieldData('CEXAQ31100OutBlock2','AcntNo',0)
        data2['AcntNm'] = self.GetFieldData('CEXAQ31100OutBlock2','AcntNm',0)
        data2['BnsplAmt'] = self.GetFieldData('CEXAQ31100OutBlock2','BnsplAmt',0)
        data2['TotEvalAmt'] = self.GetFieldData('CEXAQ31100OutBlock2','TotEvalAmt',0)
        data2['TotPnlAmt'] = self.GetFieldData('CEXAQ31100OutBlock2','TotPnlAmt',0)

        self.data.append(data1)
        self.data.append(data2)

        nCount = self.GetBlockCount('CEXAQ31100OutBlock3')
        for i in xrange(nCount):
            data3 = {}
            data3['FnoIsuNo'] = self.GetFieldData('CEXAQ31100OutBlock3','FnoIsuNo',i)
            data3['IsuNm'] = self.GetFieldData('CEXAQ31100OutBlock3','IsuNm',i)
            data3['BnsTpCode'] = self.GetFieldData('CEXAQ31100OutBlock3','BnsTpCode',i)
            data3['BnsTpNm'] = self.GetFieldData('CEXAQ31100OutBlock3','BnsTpNm',i)
            data3['UnsttQty'] = self.GetFieldData('CEXAQ31100OutBlock3','UnsttQty',i)
            data3['LqdtAbleQty'] = self.GetFieldData('CEXAQ31100OutBlock3','LqdtAbleQty',i)
            data3['FnoAvrPrc'] = self.GetFieldData('CEXAQ31100OutBlock3','FnoAvrPrc',i)
            data3['NowPrc'] = self.GetFieldData('CEXAQ31100OutBlock3','NowPrc',i)
            data3['CmpPrc'] = self.GetFieldData('CEXAQ31100OutBlock3','CmpPrc',i)
            data3['EvalAmt'] = self.GetFieldData('CEXAQ31100OutBlock3','EvalAmt',i)
            data3['EvalPnl'] = self.GetFieldData('CEXAQ31100OutBlock3','EvalPnl',i)
            data3['PnlRat'] = self.GetFieldData('CEXAQ31100OutBlock3','PnlRat',i)
            data3['UnsttAmt'] = self.GetFieldData('CEXAQ31100OutBlock3','UnsttAmt',i)
            data3['BnsplAmt'] = self.GetFieldData('CEXAQ31100OutBlock3','BnsplAmt',i)
            self.data.append(data3)

        self.Notify()
        pass


