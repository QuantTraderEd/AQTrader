__author__ = 'assa'

import time
from PyQt4 import QtGui
from DBLoaderThread import DBLoaderThread


class DBWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initThread()
        pass

    def initUI(self):
        self.startPushButton = QtGui.QPushButton(self)
        self.plainTextEditor = QtGui.QPlainTextEdit(self)
        self.vboxLayout = QtGui.QVBoxLayout(self)

        self.vboxLayout.addWidget(self.plainTextEditor)
        self.vboxLayout.addWidget(self.startPushButton)

        self.plainTextEditor.setReadOnly(True)
        self.startPushButton.setText('Start')
        self.startPushButton.clicked.connect(self.onClick)

        self.resize(340, 140)
        self.setWindowTitle('DBLoader')
        pass

    def initThread(self):
        self._DBLoaderThread = DBLoaderThread(subtype='Real')
        self._DBLoaderThread.finished.connect(self.NotifyThreadEnd)
        self._DBLoaderThread.MsgNotify.connect(self.onNotify)

    def NotifyThreadEnd(self):
        self.startPushButton.setText('Start')
        pass

    def onClick(self):
        strtime = time.strftime('[%H:%M:%S] ')
        if not self._DBLoaderThread.isRunning():
            self.plainTextEditor.appendPlainText(strtime + 'Start Thread')
            self.startPushButton.setText('Stop')
            self._DBLoaderThread.start()
        else:
            self._DBLoaderThread.stop()
            self.plainTextEditor.appendPlainText(strtime + 'Stop Thread')
            self.startPushButton.setText('Start')
        pass

    def onNotify(self,msg):
        strtime = time.strftime('[%H:%M:%S] ')
        self.plainTextEditor.appendPlainText(strtime + msg)
        pass

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = DBWidget()
    wdg.show()
    sys.exit(app.exec_())