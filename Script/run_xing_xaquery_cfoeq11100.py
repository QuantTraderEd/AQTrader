# -*- coding: utf-8 -*-

import getpass
import datetime as dt
import pythoncom

from six.moves import input

from pyxing import XASession
from pyxing import XASessionEvents
from pyxing.xing_xaquery_cfoeq11100 import XAQuery_CFOEQ11100


# ==================== Observers ====================
class ConsoleViewer:
    def Update(self, subject):
        subject.flag = False
        # print '--------' * 5
        # if isinstance(subject.data, dict):
        #     for item in subject.data:
        #         print item, subject.data[item]
        # elif isinstance(subject.data, list):
        #     for item in subject.data:
        #         print item
        pass


def main():
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

    now_dt = dt.datetime.now()
    str_nowdt = now_dt.strftime("%Y%m%d")
    # str_nowdt = '20190722'

    user = input('user: ')
    passwd = getpass.getpass('passwd: ')
    certpw = ''

    xa_session.ConnectServer(server, port)
    ret = xa_session.Login(user, passwd, certpw, servertype, showcerterror)
    XASessionEvents.session = xa_session
    xa_session.flag = True
    while xa_session.flag:
        pythoncom.PumpWaitingMessages()

    accountlist = xa_session.GetAccountList()

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

    for key in xquery.data[1]:
        print key, xquery.data[1][key]


if __name__ == '__main__':
    main()
