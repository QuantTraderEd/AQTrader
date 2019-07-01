# -*- coding: utf-8 -*-

from __future__ import print_function

from kiwoom_source import Kiwoom


class KiwoomOPT50001(Kiwoom):
    """
    TR: futures & option last price
    """
    def __init__(self):
        super(KiwoomOPT50001, self).__init__()

    def on_signal(self, trcode, rqname):
        if trcode == u"opt50001":
            data = self.ocx.dynamicCall("GetCommDataEx(QString, QString)", trcode, rqname)
            data = unicode(data.toPyObject())
            self.data = data
            if self.event is not None:
                self.event.exit()
