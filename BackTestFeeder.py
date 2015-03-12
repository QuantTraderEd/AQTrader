# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 15:00:36 2015

@author: assa
"""

import zmq
import sqlite3 as lite
from PyQt4 import QtGui, QtCore


class BackTestFeedingThread(QtCore.QThread):
    receiveData = QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        QtCore.QThread.__init__(self,parent)
        self.msg = ''
        self.mt_stop = False
        self.mutex = QtCore.QMutex()
        self.mt_pauseCodition = QtCore.QWaitCondition()

    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://127.0.0.1:5501")

    def run(self):
        self.initZMQ()
        filedbname = 'TAQ_20150226.db'
        conn = lite.connect('./Data/' + filedbname)

        cur = conn.cursor()
        cur.execute("""SELECT COUNT(*) FROM FutOptTickData""")
        row = cur.fetchone()
        count = row[0]
        cur.execute("""SELECT * FROM FutOptTickData WHERE rowid = 1""")
        names = map(lambda x: x[0], cur.description)

        for i in xrange(count):
            cur.execute("""SELECT * FROM FutOptTickData WHERE rowid = %d"""%(i+1))
            row = cur.fetchone()
            row = dict(zip(names, row))
            self.socket.send_pyobj(row)
            #row = [str(item) for item in row]
            #msg = ','.join(row)
            #self.socket.send(msg)
        pass

class BackTestFeeder(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initThread()

    def initUI(self):
        self.button = QtGui.QPushButton('Start', self)
        self.button.clicked.connect(self.onClick)
        self.button.move(70, 40)
        self.setWindowTitle('BackTestFeeder')
        self.resize(220, 100)
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

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = BackTestFeeder()
    wdg.show()
    sys.exit(app.exec_())



