# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from kiwoom_source import KiwoomReal


class KiwoomOptionsTradeTick(KiwoomReal):
    """
    Real: options trade tick
    """

    def __init__(self, kiwoom_session=None):
        super(KiwoomOptionsTradeTick, self).__init__(kiwoom_session=kiwoom_session)
        self.fid_name_dict = dict()
        self.fid_name_dict[20] = u"Timestamp"
        self.fid_name_dict[10] = u"LastPrice"
        self.fid_name_dict[15] = u"LastQty"
        self.fid_name_dict[13] = u"Volume"
        self.fid_name_dict[195] = u'OpenInterest'
        self.fid_name_dict[27] = u"Ask1"
        self.fid_name_dict[28] = u"Bid1"
        self.fidlist = self.fid_name_dict.keys()
        self.data = dict()

    def on_signal(self, realtype, shortcd):
        if realtype == u"옵션시세":
            self.data = dict()
            self.data["ShortCD"] = unicode(shortcd)
            for i in self.fidlist:
                data = self.kiwoom_session.ocx.dynamicCall("GetCommRealData(QString, int)", shortcd, i)
                # print(self.fid_name_dict[i], unicode(data.toPyObject()).strip(), )
                self.data[self.fid_name_dict[i]] = unicode(data.toPyObject()).strip()
                if i == 15:
                    self.data['BuySell'] = self.data[self.fid_name_dict[i]][0]
                    self.data['LastQty'] = self.data[self.fid_name_dict[i]][1:]
            self.notify()
            print(self.data)
            # self.receiveData.emit(self.data)
