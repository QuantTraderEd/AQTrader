# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from ..dataloader.dataloader_main import MainForm


class TestClass(object):
    app = QtGui.QApplication(sys.argv)
    local_form = MainForm()
    local_form.show()
    local_form.onClick()

    def test_thread_running(self):
        assert self.local_form.dataloader_thread.isRunning()
