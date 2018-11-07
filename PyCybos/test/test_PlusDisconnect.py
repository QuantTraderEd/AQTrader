# -*- coding: utf-8 -*-

import time
from ..pycybos import CpCybos

cpcybos = CpCybos()

def test_PlusDisconnect():
    if cpcybos.IsConnect():
        print 'cybos connected...'

        print 'signal cybos terminate'
        cpcybos.PlusDisconnect()
        assert cpcybos.OnDisConnect()
    assert cpcybos.OnDisConnect()