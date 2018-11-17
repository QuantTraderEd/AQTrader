# -*- coding: utf-8 -*-

from xing_source import SourceQuery


class XAQuery_CFOEQ11100(SourceQuery):
    """
    futures & options account's deposit amnt
    """
    def __init__(self):
        super(XAQuery_CFOEQ11100, self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\CFOEQ11100.res")
        self.data = list()
        pass

    def OnSignal(self):
        self.data = list()
        data1 = dict()
        data1['RecCnt'] = self.GetFieldData('CFOEQ11100OutBlock1', 'RecCnt', 0)
        data1['AcntNo'] = self.GetFieldData('CFOEQ11100OutBlock1', 'AcntNo', 0)
        data1['Pwd'] = self.GetFieldData('CFOEQ11100OutBlock1', 'Pwd', 0)
        data1['BnsDt'] = self.GetFieldData('CFOEQ11100OutBlock1', 'BnsDt', 0)
        self.data.append(data1)

        data2 = dict()
        data2['RecCnt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'RecCnt', 0)
        data2['AcntNm'] = self.GetFieldData('CFOEQ11100OutBlock2', 'AcntNm', 0)
        data2['OpnmkDpsamtTotamt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OpnmkDpsamtTotamt', 0)
        data2['OpnmkDps'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OpnmkDps', 0)
        data2['OpnmkMnyrclAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OpnmkMnyrclAmt', 0)
        data2['OpnmkSubstAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OpnmkSubstAmt', 0)
        data2['TotAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'TotAmt', 0)
        data2['MnyrclAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'MnyrclAmt', 0)
        data2['SubstDsgnAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'SubstDsgnAmt', 0)
        data2['CsgnMgn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'CsgnMgn', 0)
        data2['MnyCsgnMgn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'MnyCsgnMgn', 0)
        data2['MaintMgn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'MaintMgn', 0)
        data2['MnyMaintMgn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'MnyMaintMgn', 0)
        data2['OutAbleAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OutAbleAmt', 0)
        data2['MnyoutAbleAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'MnyoutAbleAmt', 0)
        data2['SubstOutAbleAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'SubstOutAbleAmt', 0)
        data2['OrdAbleAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OrdAbleAmt', 0)
        data2['MnyOrdAbleAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'MnyOrdAbleAmt', 0)
        data2['AddMgnOcrTpCode'] = self.GetFieldData('CFOEQ11100OutBlock2', 'AddMgnOcrTpCode', 0)
        data2['AddMgn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'AddMgn', 0)
        data2['MnyAddMgn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'MnyAddMgn', 0)
        data2['NtdayToAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayToAmt', 0)
        data2['NtdayDps'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayDps', 0)
        data2['NtdayMnyrclAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayMnyrclAmt', 0)
        data2['NtdaySubstAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdaySubstAmt', 0)
        data2['NtdayCsgnAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayCsgnAmt', 0)
        data2['NtdayMnyCsgnMgn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayMnyCsgnMgn', 0)
        data2['NtdayMaintMgn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayMaintMgn', 0)
        data2['NtdayMnyMaintMgn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayMnyMaintMgn', 0)
        data2['NtdayOutAbleAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayOutAbleAmt', 0)
        data2['NtdayMnyoutAbleAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayMnyoutAbleAmt', 0)
        data2['NtdaySubstOutAbleAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdaySubstOutAbleAmt', 0)
        data2['NtdayOrdAbleAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayOrdAbleAmt', 0)
        data2['NtdayMnyOrdAbleAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayMnyOrdAbleAmt', 0)
        data2['NtdayAddMgnTp'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayAddMgnTp', 0)
        data2['NtdayAddMgn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayAddMgn', 0)
        data2['NtdayMnyAddMgn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdayMnyAddMgn', 0)
        data2['NtdaySettAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'NtdaySettAmt', 0)
        data2['EvalDpsamtTotamt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'EvalDpsamtTotamt', 0)
        data2['MnyEvalDpstgAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'MnyEvalDpstgAmt', 0)
        data2['DpsamtUtlgrrHibPrergAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'DpsamtUtlgrrHibPrergAmt', 0)
        data2['TaxAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'TaxAmt', 0)
        data2['CsgnMgnrat'] = self.GetFieldData('CFOEQ11100OutBlock2', 'CsgnMgnrat', 0)
        data2['CsgnMnyMgnrat'] = self.GetFieldData('CFOEQ11100OutBlock2', 'CsgnMnyMgnrat', 0)
        data2['DpstgTotamtLackAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'DpstgTotamtLackAmt', 0)
        data2['DpstgMnyLackAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'DpstgMnyLackAmt', 0)
        data2['RealInAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'RealInAmt', 0)
        data2['InAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'InAmt', 0)
        data2['OutAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OutAmt', 0)
        data2['FutsAdjstDfamt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsAdjstDfamt', 0)
        data2['FutsThdayDfamt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsThdayDfamt', 0)
        data2['FutsUpdtDfamt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsUpdtDfamt', 0)
        data2['FutsLastSettDfamt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsLastSettDfamt', 0)
        data2['OptSettDfamt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptSettDfamt', 0)
        data2['OptBuyAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptBuyAmt', 0)
        data2['OptSellAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptSellAmt', 0)
        data2['OptXrcDfamt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptXrcDfamt', 0)
        data2['OptAsgnDfamt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptAsgnDfamt', 0)
        data2['RealGdsUndAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'RealGdsUndAmt', 0)
        data2['RealGdsUndAsgnAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'RealGdsUndAsgnAmt', 0)
        data2['RealGdsUndXrcAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'RealGdsUndXrcAmt', 0)
        data2['CmsnAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'CmsnAmt', 0)
        data2['FutsCmsn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsCmsn', 0)
        data2['OptCmsn'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptCmsn', 0)
        data2['FutsCtrctQty'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsCtrctQty', 0)
        data2['FutsCtrctAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsCtrctAmt', 0)
        data2['OptsCtrctQty'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptsCtrctQty', 0)
        data2['OptsCtrctAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptsCtrctAmt', 0)
        data2['FutsUnsttQty'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsUnsttQty', 0)
        data2['FutsUnsttAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsUnsttAmt', 0)
        data2['OptsUnsttQty'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptsUnsttQty', 0)
        data2['OptsUnsttAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptsUnsttAmt', 0)
        data2['FutsBuyUnsttQty'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsBuyUnsttQty', 0)
        data2['FutsBuyUnsttAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsBuyUnsttAmt', 0)
        data2['FutsSellUnsttQty'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsSellUnsttQty', 0)
        data2['FutsSellUnsttAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsSellUnsttAmt', 0)
        data2['OptBuyUnsttQty'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptBuyUnsttQty', 0)
        data2['OptBuyUnsttAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptBuyUnsttAmt', 0)
        data2['OptSellUnsttQty'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptSellUnsttQty', 0)
        data2['OptSellUnsttAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptSellUnsttAmt', 0)
        data2['FutsBuyctrQty'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsBuyctrQty', 0)
        data2['FutsBuyctrAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsBuyctrAmt', 0)
        data2['FutsSlctrQty'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsSlctrQty', 0)
        data2['FutsSlctrAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsSlctrAmt', 0)
        data2['OptBuyctrQty'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptBuyctrQty', 0)
        data2['OptBuyctrAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptBuyctrAmt', 0)
        data2['OptSlctrQty'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptSlctrQty', 0)
        data2['OptSlctrAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptSlctrAmt', 0)
        data2['FutsBnsplAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsBnsplAmt', 0)
        data2['OptBnsplAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptBnsplAmt', 0)
        data2['FutsEvalPnlAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsEvalPnlAmt', 0)
        data2['OptEvalPnlAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptEvalPnlAmt', 0)
        data2['FutsEvalAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'FutsEvalAmt', 0)
        data2['OptEvalAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'OptEvalAmt', 0)
        data2['MktEndAfMnyInAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'MktEndAfMnyInAmt', 0)
        data2['MktEndAfMnyOutAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'MktEndAfMnyOutAmt', 0)
        data2['MktEndAfSubstDsgnAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'MktEndAfSubstDsgnAmt', 0)
        data2['MktEndAfSubstAbndAmt'] = self.GetFieldData('CFOEQ11100OutBlock2', 'MktEndAfSubstAbndAmt', 0)
        self.data.append(data2)

        self.Notify()
        pass

