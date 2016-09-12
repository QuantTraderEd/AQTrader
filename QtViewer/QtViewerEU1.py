# -*- coding: utf-8 -*-
"""
Created on Sun Jan 04 18:08:52 2015

@author: assa
"""

import logging
import sqlite3 as lite
from PyQt4 import QtCore
from datetime import datetime

def convert(strprice):
    return '%.2f' %round(float(strprice),2)


class QtViewerEU1(QtCore.QObject):
    receive = QtCore.pyqtSignal()

    def __init__(self, zmq_socket=None, parent=None):
        super(QtViewerEU1, self).__init__(parent)
        self.zmq_socket = zmq_socket
        self.dbname = None
        self.flag = True
        self.logger = logging.getLogger('ZeroOMS.Thread.EU1')
        self.logger.info('init QtViewerEU1')

    def Update(self, subject):
        #print '-' * 20
        if type(subject.data).__name__ == 'dict':
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]
            #print 'szMessage',  subject.data['szMessage']
            #print 'szMessageCode', subject.data['szMessageCode'],
            #print subject.data
            ordno = subject.data['ordno']
            orgordno = subject.data['orgordno']
            execno = None

            if subject.data['bnstp'] == '2': buysell = 'buy'
            elif subject.data['bnstp'] == '1': buysell = 'sell'
            else: buysell = None

            shortcd = subject.data['fnoIsuno']   # or isuno
            ordprice = None
            ordqty = None
            # ordprice = subject.data['ordprc']
            # ordqty = subject.data['ordqty']
            execprice = subject.data['execprc']
            execqty = subject.data['execqty']
            unexecqty = subject.data['unercqty']
            orderitem = (ordno, strnowtime, buysell, shortcd, ordprice, ordqty, execprice, execqty, unexecqty)

            if buysell == 'buy': buysell = 'B'
            elif buysell == 'sell': buysell = 'S'
            else: buysell = ''

            msg_dict = {}
            msg_dict['OrdNo'] = ordno
            msg_dict['ExecNo'] = execno
            msg_dict['TimeStamp'] = nowtime
            msg_dict['ShortCD'] = shortcd
            msg_dict['OrdPrice'] = ordprice
            msg_dict['OrdQty'] = ordqty
            msg_dict['buysell'] = buysell
            msg_dict['ExecPrice'] = execprice
            msg_dict['ExecQty'] = execqty

            self.zmq_socket.send_pyobj(msg_dict)

            self.logger.info(str(orderitem))

            if self.dbname != None:
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()
                cursor_db.execute("""INSERT INTO OrderList(OrgOrdNo,Time,BuySell,ShortCD,Price,Qty,ExecPrice,ExecQty,UnExecQty)
                                                VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?)""",orderitem)

                cursor_db.execute("""Select ExecPrice,ExecQty,UnExecQty From OrderList
                                    WHERE OrdNo = ? and ShortCD = ? and ChkReq is not null """,(str(ordno),str(shortcd),))
                rows = cursor_db.fetchall()
                unexecqty = 0
                avgExecPrice = 0
                avgExecQty = 0
                if len(rows) == 1:
                    if rows[0][0]:
                        avgExecPrice = float(rows[0][0])
                    if rows[0][1]:
                        avgExecQty = int(rows[0][1])
                    unexecqty = int(rows[0][2])
                    avgExecPrice = (avgExecPrice * avgExecQty + float(execprice) * int(execqty)) / (avgExecQty + int(execqty))
                    avgExecQty =  avgExecQty + int(execqty)
                    avgExecPrice = convert(avgExecPrice)


                if unexecqty > 0:
                    cursor_db.execute("""Update OrderList Set ExecPrice=?, ExecQty=?, UnExecQty=?
                                                                    WHERE OrdNo=? and ShortCD = ? and (BuySell = 'buy' or BuySell = 'sell')
                                                                    and ChkReq is not null
                                                                    """,
                                                                    (str(avgExecPrice), str(avgExecQty),str(unexecqty - int(execqty)),str(ordno),str(shortcd),))
                conn_db.commit()
                conn_db.close()
                #self.emit(QtCore.SIGNAL("OnReceiveData (QString)"),'SC1')
                self.receive.emit()

        self.flag = False


