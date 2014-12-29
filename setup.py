# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 23:01:22 2014

@author: assa
"""

import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [ Executable('ZeroFeederMainForm.py',base = base)]
includes = ["zmq", "zmq.utils.garbage", "zmq.backend.cython", "win32com.gen_py"]
setup(name='test',
      version='0.1',
      description='Test',
      options = {"build_exe": {"includes": includes }},
      executables=executables
)