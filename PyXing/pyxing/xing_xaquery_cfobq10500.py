# -*- coding: utf-8 -*-

from xing_source import SourceQuery


class XAQuery_CFOBQ10500(SourceQuery):
    """
    futures&options short margin table
    """
    def __init__(self):
        super(XAQuery_CFOBQ10500, self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\CFOBQ10500.res")
        pass

    def OnSignal(self):
        self.data = list()
        data1 = dict()
        data1['RecCnt'] = self.GetFieldData('CFOBQ10500OutBlock1', 'RecCnt', 0)
        data1['AcntNo'] = self.GetFieldData('CFOBQ10500OutBlock1', 'AcntNo', 0)
        data1['Pwd'] = self.GetFieldData('CFOBQ10500OutBlock1', 'Pwd', 0)

        self.data.append(data1)

        data2 = dict()
        data2['RecCnt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'RecCnt', 0)
        data2['AcntNm'] = self.GetFieldData('CFOBQ10500OutBlock2', 'AcntNm', 0)
        data2['DpsamTotamt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'DpsamTotamt', 0)
        data2['Dps'] = self.GetFieldData('CFOBQ10500OutBlock2', 'Dps', 0)
        data2['SubsAmt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'SubsAmt', 0)
        data2['FilupDpsamtTotamt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'FilupDpsamtTotamt', 0)
        data2['FilupDps'] = self.GetFieldData('CFOBQ10500OutBlock2', 'FilupDps', 0)
        data2['FutsPnlAmt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'FutsPnlAmt', 0)
        data2['WthdwAbleAmt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'WthdwAbleAmt', 0)
        data2['PsnOutAbleCurAmt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'PsnOutAbleCurAmt', 0)
        data2['PsnOutAbleSubstAmt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'PsnOutAbleSubstAmt', 0)
        data2['Mgn'] = self.GetFieldData('CFOBQ10500OutBlock2', 'Mgn', 0)
        data2['MnyMgn'] = self.GetFieldData('CFOBQ10500OutBlock2', 'MnyMgn', 0)
        data2['OrdAbleAmt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'OrdAbleAmt', 0)
        data2['MnyOrdAbleAmt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'MnyOrdAbleAmt', 0)
        data2['AddMgn'] = self.GetFieldData('CFOBQ10500OutBlock2', 'AddMgn', 0)
        data2['MnyAddMgn'] = self.GetFieldData('CFOBQ10500OutBlock2', 'MnyAddMgn', 0)
        data2['AmtPrdayChckInAmt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'AmtPrdayChckInAmt', 0)
        data2['FnoPrdaySubstSellAmt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'FnoPrdaySubstSellAmt', 0)
        data2['FnoCrdaySubstSellAmt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'FnoCrdaySubstSellAmt', 0)
        data2['FnoPrdayFdamt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'FnoPrdayFdamt', 0)
        data2['FnoCrdayFdamt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'FnoCrdayFdamt', 0)
        data2['FcurrSubsAmt'] = self.GetFieldData('CFOBQ10500OutBlock2', 'FcurrSubsAmt', 0)
        data2['FnoAcntAfmgnNm'] = self.GetFieldData('CFOBQ10500OutBlock2', 'FnoAcntAfmgnNm', 0)

        self.data.append(data2)

        data3 = dict()
        data3['PdGrpCodeNm'] = self.GetFieldData('CFOBQ10500OutBlock3', 'PdGrpCodeNm', 0)
        data3['NetRiskMgn'] = self.GetFieldData('CFOBQ10500OutBlock3', 'NetRiskMgn', 0)
        data3['PrcMgn'] = self.GetFieldData('CFOBQ10500OutBlock3', 'PrcMgn', 0)
        data3['SprdMgn'] = self.GetFieldData('CFOBQ10500OutBlock3', 'SprdMgn', 0)
        data3['PrcFlctMgn'] = self.GetFieldData('CFOBQ10500OutBlock3', 'PrcFlctMgn', 0)
        data3['MinMgn'] = self.GetFieldData('CFOBQ10500OutBlock3', 'MinMgn', 0)
        data3['OrdMgn'] = self.GetFieldData('CFOBQ10500OutBlock3', 'OrdMgn', 0)
        data3['OptNetBuyAmt'] = self.GetFieldData('CFOBQ10500OutBlock3', 'OptNetBuyAmt', 0)
        data3['CsgnMgn'] = self.GetFieldData('CFOBQ10500OutBlock3', 'CsgnMgn', 0)
        data3['MaintMgn'] = self.GetFieldData('CFOBQ10500OutBlock3', 'MaintMgn', 0)
        data3['FutsBuyExecAmt'] = self.GetFieldData('CFOBQ10500OutBlock3', 'FutsBuyExecAmt', 0)
        data3['FutsSellExecAmt'] = self.GetFieldData('CFOBQ10500OutBlock3', 'FutsSellExecAmt', 0)
        data3['OptBuyExecAmt'] = self.GetFieldData('CFOBQ10500OutBlock3', 'OptBuyExecAmt', 0)
        data3['OptSellExecAmt'] = self.GetFieldData('CFOBQ10500OutBlock3', 'OptSellExecAmt', 0)
        data3['FutsPnlAmt'] = self.GetFieldData('CFOBQ10500OutBlock3', 'FutsPnlAmt', 0)
        data3['TotRiskCsgnMgn'] = self.GetFieldData('CFOBQ10500OutBlock3', 'TotRiskCsgnMgn', 0)
        data3['UndCsgnMgn'] = self.GetFieldData('CFOBQ10500OutBlock3', 'UndCsgnMgn', 0)
        data3['MgnRdctAmt'] = self.GetFieldData('CFOBQ10500OutBlock3', 'MgnRdctAmt', 0)

        self.data.append(data3)

        self.Notify()
        pass
