# -*- coding: utf-8 -*-

import sys
import zmq
import redis

from PyQt4 import QtGui

from OrderManager.zerooms_main import MainForm


class TestClass(object):
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()

    def test_auto_config(self):
        assert self.myform.set_auto
        if self.myform.set_auto:
            self.myform.slot_ToggleExecute(True)
            self.myform.ui.actionExecute.setChecked(True)

    def test_thread_running(self):
        assert self.myform.ordermachineThread.isRunning()