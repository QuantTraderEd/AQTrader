# -*- coding: utf-8 -*-

from kiwoom_source import KiwoomReal


class KiwoomFuturesQuoteTick(KiwoomReal):
    """
    Real: futures quote tick
    """

    def __init__(self, kiwoom_session=None):
        super(KiwoomFuturesQuoteTick, self).__init__(kiwoom_session=kiwoom_session)
        self.fid_name_dict = dict()
        self.fid_name_dict[21] = u"TimeStamp"
        for i in xrange(1, 5):
            self.fid_name_dict[40 + i] = u"Ask%d" % i
            self.fid_name_dict[60 + i] = u"AskQty%d" % i
            self.fid_name_dict[100 + i] = u"AskCnt%d" % i

            self.fid_name_dict[50 + i] = u"Bid%d" % i
            self.fid_name_dict[70 + i] = u"BidQty%d" % i
            self.fid_name_dict[110 + i] = u"BidCnt%d" % i

        self.fid_name_dict[121] = u"TotalAskQty"
        self.fid_name_dict[123] = u"TotalAskCnt"
        self.fid_name_dict[125] = u"totalBidQty"
        self.fid_name_dict[127] = u"TotalBidCnt"

        self.fidlist = self.fid_name_dict.keys()
        self.data = dict()

    def on_signal(self, realtype, shortcd):
        if realtype == u"선물호가잔량":
            self.data["shortcd"] = shortcd
            for i in self.fidlist:
                data = self.kiwoom_session.ocx.dynamicCall("GetCommRealData(QString, int)", shortcd, i)
                print(self.fid_name_dict[i], unicode(data.toPyObject()).strip(), )
                self.data[self.fid_name_dict[i]] = unicode(data.toPyObject()).strip()
            self.notify()
            self.receiveData.emit(self.data)
