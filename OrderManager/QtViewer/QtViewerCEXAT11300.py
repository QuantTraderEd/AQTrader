# -*- coding: utf-8 -*-

import pprint
import logging
import sqlite3 as lite
from PyQt4 import QtCore
from datetime import datetime


class QtViewerCEXAT11300(QtCore.QObject):
    """
    kospi200 eurex option cancel order
    """
    receive = QtCore.pyqtSignal()

    def __init__(self, zmq_socket_exec_report):
        super(QtViewerCEXAT11300, self).__init__()
        self.zmq_socket_exec_report = zmq_socket_exec_report  # port 6000: real 6001: sub_real
        self.dbname = None
        self.flag = True
        self.conn = None
        self.cursor = None
        self.logger = logging.getLogger('ZeroOMS.Thread.CEXAT11300')
        self.logger.info('init QtViewerCEXAT11300')

    def initDB(self):
        if self.dbname is not None:
            self.conn = lite.connect(self.dbname)
            self.cursor = self.conn.cursor()
        pass

    def Update(self, subject):
        if type(subject.data) != dict:
            self.flag = False
            return

        nowtime = datetime.now()
        strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]
        sz_msg = subject.data['szMessage']
        msgcode = subject.data['szMessageCode']
        self.logger.info(sz_msg.strip() + msgcode)

        # msg = pprint.pformat(subject.data)
        # self.logger.info(msg)

        buysell = 'cancl'
        orgordno = subject.data['OrgOrdNo']
        ordno = subject.data['OrdNo']
        autotrader_id = subject.autotrader_id
        shortcd = subject.data['FnoIsuNo']
        canclqty = subject.data['CancQty']

        msg_dict = dict()
        msg_dict['autotrader_id'] = autotrader_id
        msg_dict['new_amend_cancel'] = 'C'
        msg_dict['ordno'] = ordno
        msg_dict['orgordno'] = orgordno
        msg_dict['timestamp'] = nowtime
        msg_dict['shortcd'] = shortcd
        # msg_dict['OrderQty'] = ordqty
        # msg_dict['BuySell'] = buysell
        msg_dict['canclqty'] = canclqty
        msg_dict['msg_code'] = msgcode

        self.logger.info('PUB-> %s' % str(msg_dict))
        self.zmq_socket_exec_report.send_pyobj(msg_dict)

        # -------------------------------

        buysell = 'cancl'
        shcode = subject.data['FnoIsuNo']
        # price = subject.data['OrdPrc']
        canclqty = subject.data['CancQty']
        type1 = None
        type2 = None

        chkreq = msgcode
        orderitem = (autotrader_id, ordno, orgordno, strnowtime, buysell, shcode, canclqty, chkreq)
        # print orderitem
        if type(self.conn) == lite.Connection and subject.data['szMessageCode'] == '00000':
            # conn_db = lite.connect(self.dbname)
            # cursor_db = conn_db.cursor()

            self.cursor.execute("""Select OrdNo, OrgOrdNo From OrderList
                                WHERE OrdNo = ? and ExecNo is null and BuySell = 'cancl' """, (str(ordno),))
            rows_cancl = self.cursor.fetchall()

            self.cursor.execute("""Select UnExecQty From OrderList
                                WHERE OrdNo = ? and ExecNo is null """,(str(orgordno),))
            rows = self.cursor.fetchall()
            unexecqty = 0
            if len(rows) == 1:
                unexecqty = int(rows[0][0])
            wildcard = '?,' * len(orderitem)
            wildcard = wildcard[:-1]
            self.conn.execute("""INSERT INTO OrderList(AutoTraderID, OrdNo,OrgOrdNo,Time,BuySell,ShortCD,Qty,ChkReq)
                                            VALUES(%s)""" % wildcard, orderitem)

            if len(rows_cancl) == 0 and unexecqty > 0:
                self.conn.execute("""Update OrderList Set UnExecQty=?
                                                WHERE OrdNo=? and (BuySell = 'buy' or BuySell = 'sell') """,
                                  ('0', orgordno))
            self.conn.commit()
            # conn_db.close()
            self.receive.emit()
        elif type(self.conn) == lite.Connection and subject.data['szMessageCode'] != '00156':
            # conn_db = lite.connect(self.dbname)
            # cursor_db = conn_db.cursor()
            wildcard = '?,' * len(orderitem)
            wildcard = wildcard[:-1]
            self.conn.execute("""INSERT INTO OrderList(AutoTraderID, OrdNo,OrgOrdNo,Time,BuySell,ShortCD,Qty,ChkReq)
                                            VALUES(%s)""" % wildcard, orderitem)
            self.conn.commit()
            self.receive.emit()

        self.flag = False
