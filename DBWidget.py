__author__ = 'assa'

import time
from PyQt4 import QtGui, QtCore
from DBLoaderThread import DBLoaderThread


class DBWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initThread()
        pass

    def closeEvent(self, event):
        setting = QtCore.QSettings("ZeroDBLoader.ini", QtCore.QSettings.IniFormat)
        setting.setValue("geometry", self.saveGeometry())

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

        setting = QtCore.QSettings("ZeroDBLoader.ini", QtCore.QSettings.IniFormat)
        self.restoreGeometry(setting.value("geometry").toByteArray())

        pass

    def initThread(self):
        self._DBLoaderThread = DBLoaderThread(subtype='Real')
        self._DBLoaderThread.finished.connect(self.NotifyThreadEnd)
        self._DBLoaderThread.MsgNotify.connect(self.onNotify)

    def NotifyThreadEnd(self):
        self.startPushButton.setText('Start')
        self.onNotify('End Count: ' + str(self._DBLoaderThread.count))
        self._DBLoaderThread.conn_memory.close()
        self._DBLoaderThread.conn_file.close()
        pass

    def onClick(self):
        strtime = time.strftime('[%H:%M:%S] ')
        if not self._DBLoaderThread.isRunning():
            self._DBLoaderThread.initDB()
            self.plainTextEditor.appendPlainText(strtime + 'Start Thread')
            self.startPushButton.setText('Stop')
            self._DBLoaderThread.start()
        else:
            self._DBLoaderThread.stop()
            self.plainTextEditor.appendPlainText(strtime + 'Stop Thread')
            self.startPushButton.setText('Start')
        pass

    def onNotify(self, msg):
        strtime = time.strftime('[%H:%M:%S] ')
        self.plainTextEditor.appendPlainText(strtime + msg)
        pass

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = DBWidget()
    wdg.show()
    sys.exit(app.exec_())