# -*- coding: utf-8 -*-

from xing_source import SourceQuery

class XAQuery_CFOBQ10800(SourceQuery):
    """
    option short margin table
    """
    def __init__(self):
        super(XAQuery_CFOBQ10800,self).__init__("XA_DataSet.XAQuery")
        self.LoadFromResFile("Res\\CFOBQ10800.res")
        pass

    def OnSignal(self):
        self.data = []
        data1 = {}        
        data1['RecCnt'] = self.GetFieldData('CFOBQ10800OutBlock1','RecCnt',0)
        data1['PrdgrpClssCode'] = self.GetFieldData('CFOBQ10800OutBlock1','PrdgrpClssCode',0)
        data1['ClssGrpCode'] = self.GetFieldData('CFOBQ10800OutBlock1','ClssGrpCode',0)
        data1['FstmmTpCode'] = self.GetFieldData('CFOBQ10800OutBlock1','FstmmTpCode',0)
        
        self.data.append(data1)

        nCount = self.GetBlockCount('CFOBQ10800OutBlock2')        
        for i in xrange(nCount):
            data2 = {}
            data2['ElwXrcPrc'] = self.GetFieldData('CFOBQ10800OutBlock2','ElwXrcPrc',i)
            data2['FnoIsuNo'] = self.GetFieldData('CFOBQ10800OutBlock2','FnoIsuNo',i)
            data2['HanglIsuNm1'] = self.GetFieldData('CFOBQ10800OutBlock2','HanglIsuNm1',i)
            data2['TpNm1'] = self.GetFieldData('CFOBQ10800OutBlock2','TpNm1',i)
            data2['Thrprc1'] = self.GetFieldData('CFOBQ10800OutBlock2','Thrprc1',i)
            data2['BasePrc1'] = self.GetFieldData('CFOBQ10800OutBlock2','BasePrc1',i)
            data2['OrdMgn1'] = self.GetFieldData('CFOBQ10800OutBlock2','OrdMgn1',i)
            data2['FnoIsuNo0'] = self.GetFieldData('CFOBQ10800OutBlock2','FnoIsuNo0',i)
            data2['HanglIsuNm2'] = self.GetFieldData('CFOBQ10800OutBlock2','HanglIsuNm2',i)
            data2['TpNm2'] = self.GetFieldData('CFOBQ10800OutBlock2','TpNm2',i)
            data2['Thrprc2'] = self.GetFieldData('CFOBQ10800OutBlock2','Thrprc2',i)
            data2['BasePrc2'] = self.GetFieldData('CFOBQ10800OutBlock2','BasePrc2',i)
            data2['OrdMgn2'] = self.GetFieldData('CFOBQ10800OutBlock2','OrdMgn2',i)
            self.data.append(data2)

        self.Notify()
        pass

