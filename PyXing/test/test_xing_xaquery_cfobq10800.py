# -*- coding: utf-8 -*-

import pythoncom

from xing_login_dlg import ConsoleViewer
from ..pyxing import XASession
from ..pyxing import XASessionEvents
from ..pyxing.xing_xaquery_cfobq10500 import XAQuery_CFOBQ10500


class TestClass(object):
    user = ''
    passwd = ''
    certpw = ''
    servertype = 1
    showcerterror = 1
    server_text = 'demo server'
    port = 20001

    if server_text == 'real server':
        server = 'hts.etrade.co.kr'
        servertype = 0
    elif server_text == 'demo server':
        server = 'demo.etrade.co.kr'
        servertype = 1

    xa_session = XASession()
    # xa_session.observer = proxy(self)

    def test_login(self):
        self.xa_session.ConnectServer(self.server, self.port)
        ret = self.xa_session.Login(self.user, self.passwd, self.certpw, self.servertype, self.showcerterror)
        XASessionEvents.session = self.xa_session
        self.xa_session.flag = True
        while self.xa_session.flag:
            pythoncom.PumpWaitingMessages()

        accountlist = self.xa_session.GetAccountList()
        assert len(accountlist[0]) == 11
        assert len(accountlist[1]) == 11

    def test_xquery(self):
        accountlist = self.xa_session.GetAccountList()
        console_viewer = ConsoleViewer()
        xquery = XAQuery_CFOBQ10500()
        xquery.observer = console_viewer
        xquery.SetFieldData('CFOBQ10500InBlock1', 'RecCnt', 0, 1)
        xquery.SetFieldData('CFOBQ10500InBlock1', 'AcntNo', 0, accountlist[1])
        xquery.SetFieldData('CFOBQ10500InBlock1', 'Pwd', 0, 0000)
        xquery.flag = True
        res = xquery.Request(False)
        while xquery.flag:
            pythoncom.PumpWaitingMessages()
        assert len(xquery.data) == 3
        assert xquery.data[1]['RecCnt'] == '1'
