# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from kiwoom_source import KiwoomReal


class KiwoomFuturesTradeTick(KiwoomReal):
    """
    Real: futures trade tick
    """

    def __init__(self, kiwoom_session=None):
        super(KiwoomFuturesTradeTick, self).__init__(kiwoom_session=kiwoom_session)
        self.fidlist = [20, 10, 15, 13, 195]
        self.fid_name_dict = dict()
        self.fid_name_dict[20] = u"timestamp"
        self.fid_name_dict[10] = u"lastprice"
        self.fid_name_dict[15] = u"lastqty"
        self.fid_name_dict[13] = u"volume"
        self.fid_name_dict[195] = u'openinterest'
        self.data = dict()

    def on_signal(self, realtype, shortcd):
        if realtype == u"선물시세":
            self.data = dict()
            self.data["shortcd"] = unicode(shortcd)
            for i in self.fidlist:
                data = self.kiwoom_session.ocx.dynamicCall("GetCommRealData(QString, int)", shortcd, i)
                # print(self.fid_name_dict[i], unicode(data.toPyObject()).strip(), )
                self.data[self.fid_name_dict[i]] = unicode(data.toPyObject()).strip()
            self.notify()
            print(self.data)
            self.receiveData.emit(self.data)
