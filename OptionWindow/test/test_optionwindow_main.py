# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from ..optionwindow.optionwindow_main import MainForm


class TestClass(object):
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()

    def test_thread_running(self):
        assert self.myform.mythread.isRunning()
