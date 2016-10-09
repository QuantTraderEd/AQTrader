# -*- coding: utf-8 -*-

import os
import time
import sys
import zmq
import sqlite3 as lite

from PyQt4 import QtGui, QtCore
from ui_orderlistdlg import Ui_Dialog


class OrderListDialog(QtGui.QDialog):
    def __init__(self, order_port=6001):
        super(OrderListDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)        
        self.ui.pushButton.clicked.connect(self.OnUpdateList)
        self.ui.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)        
        for i in range(self.ui.tableWidget.columnCount()):        
            if i != 3: self.ui.tableWidget.resizeColumnToContents(i)
            
        self.ui.tableWidget.cellDoubleClicked.connect(self.OnCellDoubleClicked)

        self.order_port = order_port
        self.init_zmq()

        nowtime = time.localtime()
        strtime = time.strftime('%Y%m%d',nowtime)

        self.strdbname = ''

        if nowtime.tm_hour >= 6 and nowtime.tm_hour < 16:
            self.strdbname = "orderlist_%s.db" %(strtime)
        elif nowtime.tm_hour >= 16:
            self.strdbname = "orderlist_night_%s.db" %(strtime)
        elif nowtime.tm_hour < 6:
            strtime = "%d%.2d%.2d" %(nowtime.tm_year,nowtime.tm_mon,nowtime.tm_mday-1)
            self.strdbname = "orderlist_night_%s.db" %(strtime)
        
    def __del__(self):
        if not self.socket.closed:
            self.socket.close()
        pass

    def init_zmq(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:%d" % self.order_port)
        
    def OnUpdateList(self):
        if os.path.isfile(self.strdbname):
            conn_db = lite.connect(self.strdbname)
            cursor_db = conn_db.cursor()
            cursor_db.execute('SELECT * FROM OrderList Order by ID DESC')
            col_names = [cn[0] for cn in cursor_db.description]
            rows = cursor_db.fetchall()
            self.ui.tableWidget.setRowCount(len(rows))

            # print "%s %s %2s %-25s %-7s %-8s %-9s %-4s %-5s %-5s %-12s %-5s" % tuple(col_names)
            # for row in rows:
            #     print "%s %2s %5s %-25s %-7s %-8s %-9s %-4s %-5s %-5s %-12s %-5s" % row

            rownum = 0
            for row in rows:
                for j in range(2, len(row)):
                    if row[j]:
                        self.ui.tableWidget.setItem(rownum,j-2,QtGui.QTableWidgetItem(row[j]))
                    elif not row[j]:
                        self.ui.tableWidget.setItem(rownum,j-2,QtGui.QTableWidgetItem(''))
                rownum = rownum + 1

            conn_db.close()
        pass
    
    def OnCellDoubleClicked(self,row,col):        
        type1 = self.ui.tableWidget.item(row,8).text()
        if col == 0 and (type1 == 'limit'):
            orgordno = self.ui.tableWidget.item(row,col).text()
            
            conn_db = lite.connect(self.strdbname)
            cursor_db = conn_db.cursor()
            cursor_db.execute("""Select ShortCD,UnExecQty From OrderList 
                                    WHERE OrdNo = ? and Type1 = ? """, (str(orgordno), str(type1),))
            rows = cursor_db.fetchall()
            cursor_db.close()
            
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
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mydlg = OrderListDialog()
    mydlg.show()
    app.exec_()   