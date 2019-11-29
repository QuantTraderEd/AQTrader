# -*- coding: utf-8 -*-

import psutil
import Script.TotalRun_live_patch as total_run
from Script.TotalRun_live_patch import cp_start


class TestClass(object):

    pid_dict = dict()

    def test_python_app_kill(self):
        total_run.show_task_list()
        total_run.python_app_kill()

    def test_cp_start(self):
        is_start_cp = cp_start('')
        assert is_start_cp
        total_run.close_notice_window()

    def test_kill_proc(self):

        total_run.show_task_list()
        total_run.cp_kill()

        proc_list = [proc.name() for proc in psutil.process_iter()]
        assert not ("DibServer.exe" in proc_list)
        # assert not ('CpStart.exe' in proc_list)
