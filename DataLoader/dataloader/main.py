# -*- coding: utf-8 -*-

import time
import json
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
logger.addHandler(ch)


class MainForm(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.port = 5501  # Real: 5501, RealTest 5502, BackTest 5503
        self.set_auto = False
        self.set_auto_config()

        self.init_ui()
        self.initTIMER()
        self.initThread()
        pass

    def set_auto_config(self):
        setting = QtCore.QSettings("DataLoader.ini", QtCore.QSettings.IniFormat)
        self.set_auto = setting.value("setauto", type=bool)
        self.port = setting.value("port", type=int)
        if self.set_auto:
            logger.info("setauto: True")
        else:
            logger.info("setauto: False")
        logger.info("zmq port: %d" % self.port)

    def closeEvent(self, event):
        setting = QtCore.QSettings("DataLoader.ini", QtCore.QSettings.IniFormat)
        setting.setValue("geometry", self.saveGeometry())
        setting.setValue("setauto", self.set_auto)
        setting.setValue("port", self.port)

    def init_ui(self):
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
        icon = QtGui.QIcon("./resource/database-arrow-down-icon.png")
        self.setWindowIcon(icon)
        QtGui.qApp.setStyle('Cleanlooks')

        setting = QtCore.QSettings("DataLoader.ini", QtCore.QSettings.IniFormat)
        self.restoreGeometry(setting.value("geometry").toByteArray())
        pass

    def initTIMER(self):
        self.ctimer = QtCore.QTimer()
        self.ctimer.start(300000)
        self.ctimer.timeout.connect(self.ctimer_update)

    def initThread(self):
        self.dataloader_thread = DBLoaderThread(port=self.port)
        self.dataloader_thread.filepath = './TAQ_Data/'
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
        if now_dt.hour == 6 and  now_dt.minute >= 0 and now_dt.minute <= 20:
            close_trigger = True
        elif now_dt.hour == 17 and  now_dt.minute >= 0 and now_dt.minute <= 20:
            close_trigger = True

        if close_trigger:
            logger.info("close trigger")
            if self.dataloader_thread.isRunning():
                self.dataloader_thread.stop()
            self.close()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    if myform.set_auto:
        myform.onClick()
    app.exec_()
