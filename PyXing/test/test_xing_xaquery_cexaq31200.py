# -*- coding: utf-8 -*-

import getpass
import datetime as dt
import pythoncom

from xing_login_dlg import ConsoleViewer
from ..pyxing import XASession
from ..pyxing import XASessionEvents
from ..pyxing.xing_xaquery_cexaq31200 import XAQuery_CEXAQ31200


class TestClass(object):

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

    def test_xquery(self, monkeypatch):
        # monkeypatch.setattr('builtins.input', lambda x: 'usr_id')
        monkeypatch.setattr('getpass.getpass', lambda x: '')

        now_dt = dt.datetime.now()
        str_nowdt = now_dt.strftime("%Y%m%d")

        user = 'usr_id'
        passwd = getpass.getpass('passwd:')
        certpw = ''
        self.xa_session.ConnectServer(self.server, self.port)
        # ret = self.xa_session.Login(self.user, self.passwd, self.certpw, self.servertype, self.showcerterror)
        ret = self.xa_session.Login(user, passwd, certpw, self.servertype, self.showcerterror)
        XASessionEvents.session = self.xa_session
        self.xa_session.flag = True
        while self.xa_session.flag:
            pythoncom.PumpWaitingMessages()

        accountlist = self.xa_session.GetAccountList()
        assert len(accountlist[0]) == 11
        assert len(accountlist[1]) == 11

        console_viewer = ConsoleViewer()
        xquery = XAQuery_CEXAQ31200()
        xquery.observer = console_viewer
        xquery.SetFieldData('CEXAQ31200InBlock1', 'RecCnt', 0, 1)
        xquery.SetFieldData('CEXAQ31200InBlock1', 'AcntNo', 0, accountlist[1])
        xquery.SetFieldData('CEXAQ31200InBlock1', 'InptPwd', 0, 0000)
        xquery.SetFieldData('CEXAQ31200InBlock1', 'BalEvalTp', 0, '1')
        xquery.SetFieldData('CEXAQ31200InBlock1', 'FutsPrcEvalTp', 0, '1')
        xquery.flag = True
        res = xquery.Request(False)
        while xquery.flag:
            pythoncom.PumpWaitingMessages()

        assert len(xquery.data) == 3
        assert xquery.data[0]['AcntNo'] == accountlist[1]
