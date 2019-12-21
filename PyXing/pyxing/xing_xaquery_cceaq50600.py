# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 16:27:33 2014

@author: assa
"""

from xing_source import SourceQuery

class XAQuery_CCEAQ50600(SourceQuery):
    """
    kospi cme futures cash account and total info
    """
    def __init__(self):
        super(XAQuery_CCEAQ50600,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\CCEAQ50600.res")
        self.ncount = 0
        pass

    def OnSignal(self):
        self.data = list()
        data1 = dict()
        data2 = dict()
        data1['RecCnt'] = self.GetFieldData('CCEAQ50600OutBlock1', 'RecCnt', 0)
        data1['AcntNo'] = self.GetFieldData('CCEAQ50600OutBlock1', 'AcntNo', 0)
        data1['InptPwd'] = self.GetFieldData('CCEAQ50600OutBlock1', 'InptPwd', 0)
        data1['BalEvalTp'] = self.GetFieldData('CCEAQ50600OutBlock1', 'BalEvalTp', 0)
        data1['FutsPrcEvalTp'] = self.GetFieldData('CCEAQ50600OutBlock1', 'FutsPrcEvalTp', 0)

        data2['RecCnt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'RecCnt', 0)
        data2['AcntNo'] = self.GetFieldData('CCEAQ50600OutBlock2', 'AcntNo', 0)
        data2['AcntNm'] = self.GetFieldData('CCEAQ50600OutBlock2', 'AcntNm', 0)
        data2['EvalDpsamtTotamt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'EvalDpsamtTotamt', 0)
        data2['MnyEvalDpstgAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'MnyEvalDpstgAmt', 0)
        data2['DpsamtTotamt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'DpsamtTotamt', 0)
        data2['DpstgMny'] = self.GetFieldData('CCEAQ50600OutBlock2', 'DpstgMny', 0)
        data2['PsnOutAbleTotAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'PsnOutAbleTotAmt', 0)
        data2['PsnOutAbleCurAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'PsnOutAbleCurAmt', 0)
        data2['OrdAbleTotAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'OrdAbleTotAmt', 0)
        data2['MnyOrdAbleAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'MnyOrdAbleAmt', 0)
        data2['CsgnMgnTotamt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'CsgnMgnTotamt', 0)
        data2['MnyCsgnMgn'] = self.GetFieldData('CCEAQ50600OutBlock2', 'MnyCsgnMgn', 0)
        data2['AddMgnTotamt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'AddMgnTotamt', 0)
        data2['MnyAddMgn'] = self.GetFieldData('CCEAQ50600OutBlock2', 'MnyAddMgn', 0)
        data2['CmsnAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'CmsnAmt', 0)
        data2['FutsEvalPnlAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'FutsEvalPnlAmt', 0)
        data2['OptEvalPnlAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'OptEvalPnlAmt', 0)
        data2['OptEvalAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'OptEvalAmt', 0)
        data2['OptBnsplAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'OptBnsplAmt', 0)
        data2['FutsAdjstDfamt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'FutsAdjstDfamt', 0)
        data2['TotPnlAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'TotPnlAmt', 0)
        data2['NetPnlAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'NetPnlAmt', 0)
        data2['TotEvalAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'TotEvalAmt', 0)
        data2['MnyinAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'MnyinAmt', 0)
        data2['MnyoutAmt'] = self.GetFieldData('CCEAQ50600OutBlock2', 'MnyoutAmt', 0)

        self.data.append(data1)
        self.data.append(data2)

        self.ncount = self.GetBlockCount('CCEAQ50600OutBlock3')
        for i in xrange(self.ncount):
            data3 = {}
            data3['FnoIsuNo'] = self.GetFieldData('CCEAQ50600OutBlock3', 'FnoIsuNo', i)
            data3['IsuNm'] = self.GetFieldData('CCEAQ50600OutBlock3', 'IsuNm', i)
            data3['BnsTpCode'] = self.GetFieldData('CCEAQ50600OutBlock3', 'BnsTpCode', i)
            data3['BnsTpNm'] = self.GetFieldData('CCEAQ50600OutBlock3', 'BnsTpNm', i)
            data3['UnsttQty'] = self.GetFieldData('CCEAQ50600OutBlock3', 'UnsttQty', i)
            data3['FnoAvrPrc'] = self.GetFieldData('CCEAQ50600OutBlock3', 'FnoAvrPrc', i)
            data3['NowPrc'] = self.GetFieldData('CCEAQ50600OutBlock3', 'NowPrc', i)
            data3['CmpPrc'] = self.GetFieldData('CCEAQ50600OutBlock3', 'CmpPrc', i)
            data3['EvalPnl'] = self.GetFieldData('CCEAQ50600OutBlock3', 'EvalPnl', i)
            data3['PnlRat'] = self.GetFieldData('CCEAQ50600OutBlock3', 'PnlRat', i)
            data3['EvalAmt'] = self.GetFieldData('CCEAQ50600OutBlock3', 'EvalAmt', i)
            self.data.append(data3)
        self.Notify()
        pass
