# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 15:25:22 2015

@author: assa
"""

import time
import zmq
import sqlite3 as lite
import pandas as pd
from PyQt4 import QtGui, QtCore

class BackTestFeedingThread(QtCore.QThread):
    receiveData = QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self, parent)
        self.msg = ''
        self.mt_stop = False
        self.mt_pause = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCondition = QtCore.QWaitCondition()  
        
    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://127.0.0.1:5501")
        
    def run(self):
        self.initZMQ()
        filedbname = 'TAQ_20150526.db'
        conn = lite.connect(filedbname)
        
        cur = conn.cursor()
        cur.execute("""SELECT * FROM FutOptTickData WHERE rowid = 1""")
        names = map(lambda x: x[0], cur.description)
        sqltext = """ SELECT Id, Time FROM FutOptTickData WHERE Time > '09:00:00' """
        df = pd.read_sql(sqltext, conn)
        seqlist = list(df['Id'])
        print len(seqlist)
        # fp = open('test1','w+')
        begin = time.time()        
        
        for i in seqlist:
            cur.execute("""SELECT * FROM FutOptTickData WHERE Id = %d""" %i)
            row = cur.fetchone()
            row = dict(zip(names, row))
            self.socket.send_pyobj(row)
            # QtCore.QThread.sleep(0.1)
            time.sleep(0.1)
#            row = [str(item) for item in row]
#            msg = ','.join(row)
#            self.socket.send(msg)            
            # fp.write('%s, %s\n'%(row[4],row[0]))
            self.mutex.lock()
            if self.mt_stop == True:
                break
            if self.mt_pause == True:
                self.mt_pauseCondition.wait(self.mutex)
            self.mutex.unlock()
            
        elapsed = time.time()-begin
        print 'elapsed: ', elapsed
        # fp.close()
        pass

    def mtf_stop(self):
        self.mt_stop = True
        pass
    
    def mtf_pause(self):
        self.mt_pause = True
        pass
    
    def mtf_resume(self):
        self.mt_pause = False
        self.mt_pauseCondition.wakeAll()
    
    def mtf_reset(self):
        self.mt_stop = False
        self.mt_pause = False
        self.mutex.unlock()
        

class BackTestFeeder(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initThread()
        
    def initUI(self):
        self.button = QtGui.QPushButton('Start', self)
        self.HBoxLayOut = QtGui.QHBoxLayout(self)
        self.HBoxLayOut.addWidget(self.button)
        self.button.clicked.connect(self.onClick)
        self.setWindowTitle('BackTestFeeder')
        self.resize(440, 50)
        pass
    
    def initThread(self):
        self._thread = BackTestFeedingThread()
        self._thread.finished.connect(self.NotifyThreadEnd)
        pass
    
    
    def onClick(self):
        if not self._thread.isRunning():
            self._thread.start()
            self.button.setText('Stop')
        else:
            self._thread.terminate()
            self.button.setText('Start')
        pass
    
    def NotifyThreadEnd(self):
        self.button.setText('Start')
        pass
            
                
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = BackTestFeeder()
    wdg.show()
    sys.exit(app.exec_())
