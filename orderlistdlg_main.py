# -*- coding: utf-8 -*-
"""
Created on Tue Dec 03 20:14:48 2013

@author: Administrator
"""

import time
import sys
import zmq
import sqlite3 as lite

from PyQt4 import QtGui, QtCore
from ui_orderlistdlg import Ui_Dialog

class OrderListDialog(QtGui.QDialog):
    def __init__(self):
        super(OrderListDialog,self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)        
        self.ui.pushButton.clicked.connect(self.OnUpdateList)
        self.ui.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)        
        for i in range(self.ui.tableWidget.columnCount()):        
            if i != 3: self.ui.tableWidget.resizeColumnToContents(i)
            
        self.ui.tableWidget.cellDoubleClicked.connect(self.OnCellDoubleClicked)
        
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:6000")
        
        strtime = time.strftime('%Y%m%d',time.localtime())
        self.strdbname = "orderlist_%s.db" %(strtime)
        
    def __del__(self):
        if not self.socket.closed:
            self.socket.close()
        
    def OnUpdateList(self):
        conn_db = lite.connect(self.strdbname)
        cursor_db = conn_db.cursor()
        cursor_db.execute('SELECT * FROM OrderList Order by ID DESC')
        col_names = [cn[0] for cn in cursor_db.description]
        rows = cursor_db.fetchall()
        self.ui.tableWidget.setRowCount(len(rows))

#        print "%s %2s %-25s %-7s %-8s %-9s %-4s %-5s %-5s %-12s %-5s" %tuple(col_names)
#        for row in rows:            
#            print "%2s %5s %-25s %-7s %-8s %-9s %-4s %-5s %-5s %-12s %-5s" % row
        rownum = 0
        for row in rows:            
            for j in range(1,len(row)):
                if row[j]: 
                    self.ui.tableWidget.setItem(rownum,j-1,QtGui.QTableWidgetItem(row[j]))
                elif not row[j]:
                    self.ui.tableWidget.setItem(rownum,j-1,QtGui.QTableWidgetItem(''))
            rownum = rownum + 1                            
            
        conn_db.close()            
        pass
    
    def OnCellDoubleClicked(self,row,col):        
        type1 = self.ui.tableWidget.item(row,8).text()
        if col == 0 and (type1 == 'limit'):
            ordno = self.ui.tableWidget.item(row,col).text()
            
            conn_db = lite.connect(self.strdbname)
            cursor_db = conn_db.cursor()
            cursor_db.execute("""Select ShortCD,UnExecQty From OrderList 
                                    WHERE OrdNo = ? and Type1 = ? """,(str(ordno),str(type1),))
            rows = cursor_db.fetchall()
            cursor_db.close()
            
            if len(rows) == 1:
                row = rows[0]
                shcode = row[0]
                price = ''
                unexecqty = row[1]
                
                if unexecqty > 0:
                    msg = str('cancl') + ',' + str(shcode) + ',' + str(price) + ',' + str(unexecqty) + ',' + str(ordno)
                    self.socket.send(msg)
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