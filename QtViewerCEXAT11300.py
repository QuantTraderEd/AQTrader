# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 23:28:45 2014

@author: assa
"""

import sqlite3 as lite
from PyQt4 import QtCore
from datetime import datetime

class QtViewerCEXAT11300(QtCore.QObject):
    receive = QtCore.pyqtSignal()
    def __init__(self):
        super(QtViewerCEXAT11300,self).__init__()
        self.dbname = None
        self.flag = True

    def Update(self, subject):
        print '-' * 20
        if type(subject.data).__name__ == 'dict':
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]
            print 'szMessage',  subject.data['szMessage']
            print 'szMessageCode', subject.data['szMessageCode']

            orgordno = subject.data['OrgOrdNo']
            ordno = subject.data['OrdNo']

            #-------------------------------

            buysell = 'cancl'
            shcode = subject.data['FnoIsuNo']
            #price = subject.data['OrdPrc']
            canclqty = subject.data['CancQty']
            type1 = None
            type2 = None
            print subject.data

            chkreq = subject.data['szMessageCode']
            orderitem = (ordno,orgordno,strnowtime,buysell,shcode,canclqty,chkreq)
            print orderitem
            if self.dbname != None and subject.data['szMessageCode'] == '00156':
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()

                cursor_db.execute("""Select OrdNo, OrgOrdNo From OrderList
                                    WHERE OrdNo = ? and ExecNo is null and BuySell = 'cancl' """,(str(ordno),))
                rows_cancl = cursor_db.fetchall()


                cursor_db.execute("""Select UnExecQty From OrderList
                                    WHERE OrdNo = ? and ExecNo is null """,(str(orgordno),))
                rows = cursor_db.fetchall()
                unexecqty = 0
                if len(rows) == 1:
                    unexecqty = int(rows[0][0])
                cursor_db.execute("""INSERT INTO OrderList(OrdNo,OrgOrdNo,Time,BuySell,ShortCD,Qty,ChkReq)
                                                VALUES(?, ?, ?, ? ,?, ?, ?)""",orderitem)
                print rows
                print rows_cancl
                print unexecqty

                if len(rows_cancl) == 0 and unexecqty > 0:
                    cursor_db.execute("""Update OrderList Set UnExecQty=?
                                                    WHERE OrdNo=? and (BuySell = 'buy' or BuySell = 'sell') """,
                                                    (str(unexecqty - unexecqty),orgordno))
                conn_db.commit()
                conn_db.close()
                self.receive.emit()
            elif self.dbname != None and subject.data['szMessageCode'] != '00156':
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()
                cursor_db.execute("""INSERT INTO OrderList(OrdNo,ExecNo,Time,BuySell,ShortCD,ExecQty,ChkReq)
                                                VALUES(?, ?, ?, ? ,?, ?, ?)""",orderitem)

        self.flag = False
