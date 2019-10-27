# -*- coding: utf-8 -*-

import time
import zmq
import logging
import pythoncom

from PyQt4 import QtCore
from PyQt4 import QtGui

from datafeeder_ui import Ui_MainWindow
from DataFeeder.xinglogindlg.xinglogindlg import LoginForm
from ZMQTickSender import ZMQTickSender_New


class MainForm(QtGui.QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        # self.port = 5501  # Real: 5501, RealTest 5502, BackTest 5503
        # self.set_auto = False
        # self.auto_config = self.set_auto_config()

        self.init_ui()
        # self.init_timer()
        # self.init_api()
        # self.init_feedcode()
        # self.init_taq_feederlist()
        # self.init_zmq()
        #
        # self.exchange_code = 'KRX'
        # self.filename = 'prevclose.txt'
        #
        # if self.set_auto:
        #     self.slot_CheckCybosStarter(0, 2)
        #     self.auto_start_xing(self.auto_config)

    def init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QtGui.qApp.setStyle('Cleanlooks')
        self.login_cybos = QtGui.QTableWidgetItem("login_cybos")
        self.login_xing = QtGui.QTableWidgetItem("login_xing")
        self.login_kiwoom = QtGui.QTableWidgetItem("login_kiwoom")
        self.status_xi = QtGui.QTableWidgetItem("ready")
        self.status_cy = QtGui.QTableWidgetItem("ready")
        self.ui.tableWidget.setItem(0, 2, self.login_cybos)
        self.ui.tableWidget.setItem(1, 2, self.login_xing)
        self.ui.tableWidget.setItem(2, 2, self.login_kiwoom)
        self.ui.tableWidget.setItem(0, 1, self.status_cy)
        self.ui.tableWidget.setItem(1, 1, self.status_xi)
        # self.ui.tableWidget.cellClicked.connect(self.cell_was_clicked)
        #
        # setting = QtCore.QSettings("ZeroFeeder.ini", QtCore.QSettings.IniFormat)
        # value = setting.value("geometry")
        # if value:
        #     self.restoreGeometry(setting.value("geometry").toByteArray())
        pass


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    app.exec_()