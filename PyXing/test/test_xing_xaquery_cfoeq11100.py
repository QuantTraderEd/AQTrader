# -*- coding: utf-8 -*-

import getpass
import datetime as dt
import pythoncom

from xing_login_dlg import ConsoleViewer
from ..pyxing import XASession
from ..pyxing import XASessionEvents
from ..pyxing.xing_xaquery_cfoeq11100 import XAQuery_CFOEQ11100


class TestClass(object):
    """
    잔고 & 평가금액 조회 (KRX)
    """
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
        # str_nowdt = '20190722'

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
        xquery = XAQuery_CFOEQ11100()
        xquery.observer = console_viewer
        xquery.SetFieldData('CFOEQ11100InBlock1', 'RecCnt', 0, 1)
        xquery.SetFieldData('CFOEQ11100InBlock1', 'AcntNo', 0, accountlist[1])
        xquery.SetFieldData('CFOEQ11100InBlock1', 'Pwd', 0, 0000)
        xquery.SetFieldData('CFOEQ11100InBlock1', 'BnsDt', 0, str_nowdt)
        xquery.flag = True
        res = xquery.Request(False)
        while xquery.flag:
            pythoncom.PumpWaitingMessages()

        assert len(xquery.data) == 2
        assert xquery.data[1]['RecCnt'] == '1'
        assert xquery.data[0]['BnsDt'] == str_nowdt

        for key in xquery.data[1]:
            print key, xquery.data[1][key]
