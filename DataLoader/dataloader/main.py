# -*- coding: utf-8 -*-

import time
import logging
import datetime as dt

from logging.handlers import RotatingFileHandler
from PyQt4 import QtGui, QtCore
from dataloader_thread import DBLoaderThread

logger = logging.getLogger('DataLoader')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('DataLoader.log')
fh = RotatingFileHandler('DataLoader.log', maxBytes=5242, backupCount=3)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
# logger.addHandler(ch)


class MainForm(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initUI()
        self.initTIMER()
        self.initThread()
        pass

    def closeEvent(self, event):
        setting = QtCore.QSettings("DataLoader.ini", QtCore.QSettings.IniFormat)
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
        self.setWindowTitle('DataLoader')

        setting = QtCore.QSettings("DataLoader.ini", QtCore.QSettings.IniFormat)
        self.restoreGeometry(setting.value("geometry").toByteArray())

        pass

    def initTIMER(self):
        self.ctimer = QtCore.QTimer()
        self.ctimer.start(300000)
        self.ctimer.timeout.connect(self.ctimer_update)

    def initThread(self):
        self.dataloader_thread = DBLoaderThread(subtype='Real')
        self.dataloader_thread.finished.connect(self.NotifyThreadEnd)
        self.dataloader_thread.MsgNotify.connect(self.onNotify)

    def onNotify(self, msg):
        strtime = time.strftime('[%H:%M:%S] ')
        logger.info(msg)
        self.plainTextEditor.appendPlainText(strtime + msg)
        pass

    def NotifyThreadEnd(self):
        self.startPushButton.setText('Start')
        self.onNotify('End Count: ' + str(self.dataloader_thread.count))
        # self._DBLoaderThread.conn_memory.close()
        # self._DBLoaderThread.conn_file.close()
        pass

    def onClick(self):
        strtime = time.strftime('[%H:%M:%S] ')
        if not self.dataloader_thread.isRunning():
            self.dataloader_thread.initDB()
            self.plainTextEditor.appendPlainText(strtime + 'Start Thread')
            self.startPushButton.setText('Stop')
            self.dataloader_thread.start()
        else:
            self.dataloader_thread.stop()
            self.plainTextEditor.appendPlainText(strtime + 'Stop Thread')
            self.startPushButton.setText('Start')
        pass

    def ctimer_update(self):
        now_dt = dt.datetime.now()
        close_trigger = False
        if now_dt.hour == 6 and  now_dt.minute >= 15 and now_dt.minute <= 30:
            close_trigger = True
        elif now_dt.hour == 17 and  now_dt.minute >= 22 and now_dt.minute <= 30:
            if self.dataloader_thread.isRunning():
                logger.info("auto stop")
                self.onClick()
        elif now_dt.hour == 17 and  now_dt.minute >= 45 and now_dt.minute <= 59:
            if not self.dataloader_thread.isRunning():
                logger.info("auto start")
                self.onClick()

        if close_trigger:
            logger.info("close trigger")
            if self.dataloader_thread.isRunning():
                self.dataloader_thread.stop()
            self.close()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    local_form = MainForm()
    local_form.show()
    local_form.onClick()
    sys.exit(app.exec_())
