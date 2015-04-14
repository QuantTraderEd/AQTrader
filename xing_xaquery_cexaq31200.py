# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 16:27:33 2014

@author: assa
"""

from xing_source import SourceQuery

class XAQuery_CEXAQ31200(SourceQuery):
    """
    kospi eurex options cash account and total info
    """
    def __init__(self):
        super(XAQuery_CEXAQ31200,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\CEXAQ31200.res")
        pass

    def OnSignal(self):
        self.data = []
        data1 = {}
        data2 = {}
        data1['RecCnt1'] = self.GetFieldData('CEXAQ31200OutBlock1','RecCnt',0)
        data1['AcntNo'] = self.GetFieldData('CEXAQ31200OutBlock1','AcntNo',0)
        data1['InptPwd'] = self.GetFieldData('CEXAQ31200OutBlock1','InptPwd',0)
        data1['BalEvalTp'] = self.GetFieldData('CEXAQ31200OutBlock1','BalEvalTp',0)
        data1['FutsPrcEvalTp'] = self.GetFieldData('CEXAQ31200OutBlock1','FutsPrcEvalTp',0)

        data2['RecCnt'] = self.GetFieldData('CEXAQ31200OutBlock2','RecCnt',0)
        data2['AcntNo'] = self.GetFieldData('CEXAQ31200OutBlock2','AcntNo',0)
        data2['AcntNm'] = self.GetFieldData('CEXAQ31200OutBlock2','AcntNm',0)
        data2['EvalDpsamtTotamt'] = self.GetFieldData('CEXAQ31200OutBlock2','EvalDpsamtTotamt',0)
        data2['MnyEvalDpstgAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','MnyEvalDpstgAmt',0)
        data2['DpsamtTotamt'] = self.GetFieldData('CEXAQ31200OutBlock2','DpsamtTotamt',0)
        data2['DpstgMny'] = self.GetFieldData('CEXAQ31200OutBlock2','DpstgMny',0)
        data2['PsnOutAbleTotAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','PsnOutAbleTotAmt',0)
        data2['PsnOutAbleCurAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','PsnOutAbleCurAmt',0)
        data2['OrdAbleTotAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','OrdAbleTotAmt',0)
        data2['MnyOrdAbleAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','MnyOrdAbleAmt',0)
        data2['CsgnMgnTotamt'] = self.GetFieldData('CEXAQ31200OutBlock2','CsgnMgnTotamt',0)
        data2['MnyCsgnMgn'] = self.GetFieldData('CEXAQ31200OutBlock2','MnyCsgnMgn',0)
        data2['AddMgnTotamt'] = self.GetFieldData('CEXAQ31200OutBlock2','AddMgnTotamt',0)
        data2['MnyAddMgn'] = self.GetFieldData('CEXAQ31200OutBlock2','MnyAddMgn',0)
        data2['CmsnAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','CmsnAmt',0)
        data2['FutsEvalPnlAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','FutsEvalPnlAmt',0)
        data2['OptEvalPnlAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','OptEvalPnlAmt',0)
        data2['OptEvalAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','OptEvalAmt',0)
        data2['OptBnsplAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','OptBnsplAmt',0)
        data2['FutsAdjstDfamt'] = self.GetFieldData('CEXAQ31200OutBlock2','FutsAdjstDfamt',0)
        data2['TotPnlAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','TotPnlAmt',0)
        data2['NetPnlAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','NetPnlAmt',0)
        data2['TotEvalAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','TotEvalAmt',0)
        data2['MnyinAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','MnyinAmt',0)
        data2['MnyoutAmt'] = self.GetFieldData('CEXAQ31200OutBlock2','MnyoutAmt',0)


        self.data.append(data1)
        self.data.append(data2)

        nCount = self.GetBlockCount('CEXAQ31200OutBlock3')
        for i in xrange(nCount):
            data3 = {}
            data3['FnoIsuNo'] = self.GetFieldData('CEXAQ31200OutBlock3','FnoIsuNo',i)
            data3['IsuNm'] = self.GetFieldData('CEXAQ31200OutBlock3','IsuNm',i)
            data3['BnsTpCode'] = self.GetFieldData('CEXAQ31200OutBlock3','BnsTpCode',i)
            data3['BnsTpNm'] = self.GetFieldData('CEXAQ31200OutBlock3','BnsTpNm',i)
            data3['UnsttQty'] = self.GetFieldData('CEXAQ31200OutBlock3','UnsttQty',i)
            data3['FnoAvrPrc'] = self.GetFieldData('CEXAQ31200OutBlock3','FnoAvrPrc',i)
            data3['NowPrc'] = self.GetFieldData('CEXAQ31200OutBlock3','NowPrc',i)
            data3['CmpPrc'] = self.GetFieldData('CEXAQ31200OutBlock3','CmpPrc',i)
            data3['EvalPnl'] = self.GetFieldData('CEXAQ31200OutBlock3','EvalPnl',i)
            data3['PnlRat'] = self.GetFieldData('CEXAQ31200OutBlock3','PnlRat',i)
            data3['EvalAmt'] = self.GetFieldData('CEXAQ31200OutBlock3','EvalAmt',i)
            data3['LqdtAbleQty'] = self.GetFieldData('CEXAQ31200OutBlock3','LqdtAbleQty',i)
            self.data.append(data3)

        self.Notify()
        pass
