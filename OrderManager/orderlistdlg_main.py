# -*- coding: utf-8 -*-

import os
import time
import sys
import logging
import zmq
import sqlite3 as lite

from PyQt4 import QtGui, QtCore
from ui_orderlistdlg import Ui_Dialog


class OrderListDialog(QtGui.QDialog):
    def __init__(self, order_port=6001):
        super(OrderListDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)        
        self.ui.pushButton.clicked.connect(self.on_update_list)
        self.ui.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.resizeRowsToContents()
        for i in range(self.ui.tableWidget.columnCount()):        
            if i != 3: self.ui.tableWidget.resizeColumnToContents(i)
        self.ui.tableWidget.setColumnWidth(5, 80)
        self.ui.tableWidget.cellDoubleClicked.connect(self.on_cell_double_clicked)

        self.logger = logging.getLogger('ZeroOMS.OrderListDlg')
        self.logger.info('Init OrderListDlg')

        self.order_port = order_port
        self.init_zmq()

        nowtime = time.localtime()
        strtime = time.strftime('%Y%m%d', nowtime)

        self.strdbname = ''

        # if nowtime.tm_hour >= 6 and nowtime.tm_hour < 16:
        #     self.strdbname = "orderlist_%s.db" %(strtime)
        # elif nowtime.tm_hour >= 16:
        #     self.strdbname = "orderlist_night_%s.db" %(strtime)
        # elif nowtime.tm_hour < 6:
        #     strtime = "%d%.2d%.2d" %(nowtime.tm_year,nowtime.tm_mon,nowtime.tm_mday-1)
        #     self.strdbname = "orderlist_night_%s.db" %(strtime)
        #
        # self.strdbname = 'C:/Python/' + self.strdbname
        
    def __del__(self):
        if not self.socket.closed:
            self.socket.close()
        pass

    def init_zmq(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:%d" % self.order_port)

    def init_dbname(self, strdbname):
        self.strdbname = strdbname
        self.conn_db = lite.connect(self.strdbname)
        self.cursor_db = self.conn_db.cursor()

    def on_update_list(self):
        if not os.path.isfile(self.strdbname):
            return

        self.cursor_db.execute('SELECT * FROM OrderList Order by ID DESC')
        # col_names = [cn[0] for cn in self.cursor_db.description]
        rows = self.cursor_db.fetchall()
        self.ui.tableWidget.setRowCount(len(rows))
        self.ui.tableWidget.resizeRowsToContents()

        # print "%s %s %2s %-25s %-7s %-8s %-9s %-4s %-5s %-5s %-12s %-5s" % tuple(col_names)
        # for row in rows:
        #     print "%s %2s %5s %-25s %-7s %-8s %-9s %-4s %-5s %-5s %-12s %-5s" % row

        rownum = 0
        for row in rows:
            for j in range(2, len(row)):
                if row[j]:
                    self.ui.tableWidget.setItem(rownum, j-2, QtGui.QTableWidgetItem(row[j]))
                elif not row[j]:
                    self.ui.tableWidget.setItem(rownum, j-2, QtGui.QTableWidgetItem(''))
            rownum = rownum + 1

        self.adjust_transaction_reversion()
        pass
    
    def on_cell_double_clicked(self, row, col):
        type1 = self.ui.tableWidget.item(row,8).text()
        if col == 0 and (type1 == 'limit'):
            orgordno = self.ui.tableWidget.item(row,col).text()
            
            # conn_db = lite.connect(self.strdbname)
            self.cursor_db = self.conn_db.cursor()
            self.cursor_db.execute("""Select ShortCD,UnExecQty From OrderList
                                    WHERE OrdNo = ? and Type1 = ? """, (str(orgordno), str(type1),))
            rows = self.cursor_db.fetchall()
            # cursor_db.close()
            
            if len(rows) == 1:
                row = rows[0]
                shortcd = row[0]
                unexecqty = row[1]
                
                if unexecqty > 0:
                    # msg = str('cancl') + ',' + str(shcode) + ',' + str(price) + ',' + str(unexecqty) + ',' + str(ordno)
                    # self.socket.send(msg)
                    msg_dict = {}
                    msg_dict['ShortCD'] = shortcd
                    msg_dict['OrderQty'] = unexecqty                    
                    msg_dict['NewAmendCancel'] = 'C'                    
                    msg_dict['OrgOrderNo'] = orgordno
                    self.socket.send_pyobj(msg_dict)
                    msg_in = self.socket.recv()
                    print msg_in
            else:
                print 'rows > 1 @ orderlistdlgCanclOrder'
        pass

    def adjust_transaction_reversion(self):
        sqltext = """
        SELECT
            OrdNo,
            Qty
        FROM
            OrderList
        WHERE
            UnExecQty > 0 AND
            -- OrdNo = 5510 AND
            ChkReq IN ('00040', '00039')
        """
        self.cursor_db.execute(sqltext)
        rows = self.cursor_db.fetchall()
        for row in rows:
            orgordno = row[0]
            orderqty = row[1]
            sqltext = """
            SELECT
                SUM(ExecPrice * ExecQty),
                SUM(ExecQty),
                COUNT(ExecQty)
            FROM
                OrderList
            WHERE
                OrgOrdNo = %s    AND
                ExecQty > 0      AND
                IFNULL(ChkReq,'') = ''
            """ % orgordno
            self.cursor_db.execute(sqltext)
            exec_row = self.cursor_db.fetchone()

            if exec_row[2] == 0:
                continue

            exec_qty_sum = exec_row[1]
            avg_exec_price = float(exec_row[0]) / exec_qty_sum
            unexecqty = int(orderqty) - int(exec_qty_sum)
            # print avg_exec_price, exec_qty_sum, unexecqty
            self.logger.info('adjust execqty of ordno-> %s' % orgordno)
            self.cursor_db.execute("""Update
                                        OrderList
                                      Set
                                        ExecPrice=?,
                                        ExecQty=?,
                                        UnExecQty=?
                                      WHERE
                                        OrdNo=?  AND
                                        ChkReq IN ('00040', '00039')
                                   """, (str(avg_exec_price), str(exec_qty_sum), str(unexecqty), orgordno))
        self.conn_db.commit()
        pass
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mydlg = OrderListDialog()
    # mydlg.init_dbname('C:/Python/ZeroTrader_Test/ZeroOMS/orderlist_db/orderlist_20170329.db')
    mydlg.init_dbname('C:/Python/ZeroTrader/ZeroOMS/orderlist_db/orderlist_night_20170419.db')
    mydlg.adjust_transaction_reversion()
    mydlg.show()
    app.exec_()   