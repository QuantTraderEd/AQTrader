# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from kiwoom_source import KiwoomReal


class KiwoomFuturesQuoteTick(KiwoomReal):
    """
    Real: futures quote tick
    """

    def __init__(self, kiwoom_session=None):
        super(KiwoomFuturesQuoteTick, self).__init__(kiwoom_session=kiwoom_session)
        self.fidlist = [21]
        self.fid_name_dict = dict()
        self.fid_name_dict[21] = u"timestamp"

        for i in xrange(1, 5):
            self.fid_name_dict[40 + i] = u"ask%d" % i
            self.fid_name_dict[60 + i] = u"askqty%d" % i
            self.fid_name_dict[100 + i] = u"askcnt%d" % i

            self.fid_name_dict[50 + i] = u"bid%d" % i
            self.fid_name_dict[70 + i] = u"bidqty%d" % i
            self.fid_name_dict[110 + i] = u"bidcnt%d" % i

            self.fidlist = self.fidlist + [40 + i, 60 + i, 100 + i]
            self.fidlist = self.fidlist + [50 + i, 70 + i, 110 + i]

        self.fidlist = self.fidlist + [121, 123, 125, 127]
        self.fid_name_dict[121] = u"totalaskqty"
        self.fid_name_dict[123] = u"totalaskcnt"
        self.fid_name_dict[125] = u"totalbidqty"
        self.fid_name_dict[127] = u"totalbidcnt"

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
