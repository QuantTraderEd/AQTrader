# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 23:56:06 2015

@author: assa
"""

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    
executables = [Executable('dataloader_main.py', base=base)]
includes = ["zmq", "zmq.utils.garbage", "zmq.backend.cython"]
setup(name='test',
      version='0.1',
      description='Test',
      options={"build_exe": {"includes": includes}},
      executables=executables
)