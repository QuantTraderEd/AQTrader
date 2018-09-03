# -*- coding: utf-8 -*-


import logging
import sqlite3 as lite
import redis
from PyQt4 import QtCore
from datetime import datetime


def convert(strprice):
    return '%.2f' % round(float(strprice),2)


class QtViewerC01(QtCore.QObject):
    receive = QtCore.pyqtSignal()

    def __init__(self, zmq_socket=None, parent=None):
        super(QtViewerC01, self).__init__(parent)
        self.zmq_socket = zmq_socket
        self.dbname = None
        self.flag = True
        self.redis_client = redis.Redis()
        self.logger = logging.getLogger('ZeroOMS.Thread.C01')
        self.logger.info('init QtViewerC01')
        
    def Update(self, subject):
        # print '-' * 20
        if type(subject.data).__name__ == 'dict':
            self.logger.info(str(subject.data))
            nowtime = datetime.now()
            strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]
            
            ordno = int(subject.data['ordno'])
            execno = None
            # execno = subject.data['execno']
            autotrader_id = self.redis_client.hget('ordno_dict', ordno)
            
            if subject.data['dosugb'] == '2': buysell = 'buy'                
            elif subject.data['dosugb'] == '1': buysell = 'sell'
            else: buysell = None                
                
            shortcd = subject.data['expcode'][3:11]
            ordprice = None
            ordqty = None
            execprice = subject.data['cheprice']
            execqty = subject.data['chevol']
            unexecqty = None
            orderitem = (autotrader_id, ordno, execno, strnowtime, buysell, shortcd, ordprice, ordqty, execprice, execqty, unexecqty)
            wildcard = '?,' * len(orderitem)
            wildcard = wildcard[:-1]

            if buysell == 'buy': buysell = 'B'
            elif buysell == 'sell': buysell = 'S'
            else: buysell = ''

            msg_dict = {}
            msg_dict['AutoTraderID'] = autotrader_id
            msg_dict['OrderNo'] = ordno
            msg_dict['ExecNo'] = execno
            msg_dict['TimeStamp'] = nowtime
            msg_dict['ShortCD'] = shortcd
            msg_dict['OrderPrice'] = ordprice
            msg_dict['OrderQty'] = ordqty
            msg_dict['BuySell'] = buysell
            msg_dict['ExecPrice'] = execprice
            msg_dict['ExecQty'] = execqty

            self.zmq_socket.send_pyobj(msg_dict)

            self.logger.info(str(orderitem))

            if self.dbname is not None:
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()
                cursor_db.execute("""INSERT INTO OrderList(AutoTraderID,OrgOrdNo,ExecNo,Time,BuySell,ShortCD,Price,Qty,ExecPrice,ExecQty,UnExecQty)
                                                VALUES(%s)""" % wildcard, orderitem)
                                                
                cursor_db.execute("""Select ExecPrice,ExecQty,UnExecQty From OrderList 
                                    WHERE
                                    OrdNo = ? and
                                    ShortCD = ? and
                                    ChkReq is not null """, (str(ordno), str(shortcd), ))
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
                self.receive.emit()
                
        self.flag = False      