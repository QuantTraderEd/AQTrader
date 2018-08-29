# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 13:22:19 2014

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

class t0414Viewer:
    def __init__(self):
        self.flag = False
    def Update(self, subject):
        print '--------' * 5
        for item in subject.data[1:]:
            shcode = item['expcode']
            pamt = item['pamt']
            janqty = item['janqty']
            mdposqt = item['mdposqt']
            print shcode,pamt,janqty,mdposqt
        self.flag = True
        self.data = subject.data
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
    
    
    _t0414viewer = t0414Viewer()
    
    _XAQuery_t0424 = px.XAQuery_t0424()
    _XAQuery_t0424.observer = _t0414viewer
    _XAQuery_t0424.SetFieldData('t0424InBlock','accno',0,accountlist[1])
    _XAQuery_t0424.SetFieldData('t0424InBlock','passwd',0,'0000')
    _XAQuery_t0424.SetFieldData('t0424InBlock','prcgb',0,'1')
    _XAQuery_t0424.SetFieldData('t0424InBlock','chegb',0,'2')
    _XAQuery_t0424.SetFieldData('t0424InBlock','dangb',0,'0')
    _XAQuery_t0424.SetFieldData('t0424InBlock','charge',0,'1')
    _XAQuery_t0424.SetFieldData('t0424InBlock','cts_expcode',0,'')
    _XAQuery_t0424.Request()
        
    
    button = QtGui.QPushButton("Exit")
    button.show()
    QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), app.exit)
    app.exec_()