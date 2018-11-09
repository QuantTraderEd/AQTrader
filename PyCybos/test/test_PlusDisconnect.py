# -*- coding: utf-8 -*-

from ..pycybos import CpCybos


class TestClass(object):
    cpcybos = CpCybos()

    def test_PlusDisconnect(self):
        if self.cpcybos.IsConnect():
            print 'cybos connected...'

            print 'signal cybos terminate'
            self.cpcybos.PlusDisconnect()
            assert self.cpcybos.OnDisConnect()
        else:
            assert False
