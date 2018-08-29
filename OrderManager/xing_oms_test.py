# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 19:27:11 2014

@author: assa
"""

import sys
import pyxing as px
import sqlite3 as lite

from pythoncom import PumpWaitingMessages

# ==================== Observers ====================
class ConsoleViewer:
    def Update(self, subject):
        print '--------' * 5
        for item in subject.data:
            if type(subject.data).__name__ == 'dict': 
                print item,subject.data[item]
            elif type(subject.data).__name__ == 'list': 
                if type(item).__name__ == 'dict':
                    # Occur OutBlcok
                    print '--------' * 5
                    for subitem in item:
                        print subitem,item[subitem]                                    
                else:
                    print item                
        pass
    
class t0415Viewer:
    def __init__(self):
        self.dbname = None
    def Update(self, subject):
        print '--------' * 5
        for item in subject.data[1:]:
            ordno = item['ordno']
            ordtime = item['ordtime']            
            medosu = item['medosu']
            shcode = item['expcode']
            price = item['price']
            qty= item['qty']
            hogagb = item['hogagb']
            execprice = item['cheprice']
            execqty = item['cheqty']
            unexecqty = item['orderem']
            
            unexecqty = str(int(qty) - int(execqty))
            ordtime = ordtime[0:2] + ':' + ordtime[2:4] + ':' + ordtime[4:6]
            buysell = ''
            if medosu == u'\ub9e4\uc218':
                buysell = 'buy'
            elif medosu == u'\ub9e4\ub3c4':
                buysell = 'sell'
            else:
                buysell = 'cancl'
            
            if hogagb == '00':
                type1 = 'limit'
                type2 = 'GFD'
            elif hogagb == '03':
                type1 = 'market'
                type2 = 'GFD'
            elif hogagb == '10':
                type1 = 'limit'
                type2 = 'IOC'
            elif hogagb == '13':
                type1 = 'market'
                type2 = 'IOC'
            elif hogagb == '22':
                type1 = 'limit'
                type2 = 'FOK'
            elif hogagb == '23':
                type1 = 'market'
                type2 = 'FOK'
            else:
                type1 = None
                type2 = None
                
            print ordno,ordtime,medosu,shcode,price,qty,type1,type2,execprice,execqty,unexecqty
            if self.dbname != None:
                conn_db = lite.connect(self.dbname)
                cursor_db = conn_db.cursor()
                orderitem = (ordno,ordtime,buysell,shcode,price,qty,type1,type2,unexecqty) 
                cursor_db.execute("""INSERT INTO OrderList(OrdNo,Time,BuySell,ShortCD,Price,Qty,Type1,Type2,UnExecQty) 
                                                VALUES(?, ?, ?, ? ,?, ?, ?, ?, ?)""",orderitem)
                conn_db.commit()
                conn_db.close()

        pass
    
if __name__ == '__main__':
    import PyQt4.QtGui as QtGui
    import PyQt4.QtCore as QtCore
    print 'main: start'
    app = QtGui.QApplication(sys.argv)

    viewer = ConsoleViewer()
    server = 'demo.etrade.co.kr'
    port = 20001
    servertype = 1      #demo server  
    showcerterror = 1
    user = 'eddy777'
    password = 'c9792458'
    certpw = ''
    _XASession = px.XASession()
    _XASession.observer = viewer
    _XASession.ConnectServer(server,port)
    _XASession.Login(user,password,certpw,servertype,showcerterror)
    
    while _XASession.flag:
        PumpWaitingMessages()


    accountlist = _XASession.GetAccountList()    
    print accountlist
    
    strdbname = 'orderlist_omstest.db'    
    
    
    conn_db = lite.connect(strdbname)
    cursor_db = conn_db.cursor()
    cursor_db.execute("DROP TABLE IF EXISTS OrderList")
    cursor_db.execute("""CREATE TABLE OrderList(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                                   OrdNo TEXT,
                                   OrgOrdNo TEXT,
                                   ExecNo TEXT,
                                   Time TEXT,                  
                                   BuySell TEXT,                                       
                                   ShortCD TEXT,
                                   Price TEXT,
                                   Qty TEXT,
                                   Type1 TEXT,
                                   Type2 TEXT,
                                   ExecPrice TEXT,
                                   ExecQty TEXT,
                                   UnExecQty TEXT,
                                   ChkReq TEXT
                                   )""")    
    conn_db.close()
    
    _t0415viewer = t0415Viewer()    
    _t0415viewer.dbname = strdbname
    
    _XAQuery_t0425 = px.XAQuery_t0425()
    _XAQuery_t0425.observer = _t0415viewer
    _XAQuery_t0425.SetFieldData('t0425InBlock','accno',0,accountlist[1])
    _XAQuery_t0425.SetFieldData('t0425InBlock','passwd',0,'0000')
    _XAQuery_t0425.SetFieldData('t0425InBlock','expcode',0,'')
    _XAQuery_t0425.SetFieldData('t0425InBlock','chegb',0,'2')   # 0: total, 1:exec 2:unexec
    _XAQuery_t0425.SetFieldData('t0425InBlock','medosu',0,'0')  # 0: total, 1:sell 2:buy
    _XAQuery_t0425.SetFieldData('t0425InBlock','sortgb',0,'1')  # 1: inceent 2: decent
    _XAQuery_t0425.SetFieldData('t0425InBlock','cts_ordno',0,'')    # consecutive key value
    _XAQuery_t0425.Request()
    
    
    
    button = QtGui.QPushButton("Exit")
    button.show()
    QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), app.exit)
    app.exec_()