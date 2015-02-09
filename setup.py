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

# executables = [ Executable('ZeroFeederMainForm.py',base = base)]
# includes = ["zmq", "zmq.utils.garbage", "zmq.backend.cython", "win32com.gen_py"]
# setup(name='test',
#       version='0.1',
#       description='Test',
#       options = {"build_exe": {"includes": includes }},
#       executables=executables
# )


#path_platforms = ( "..\..\..\PyQt4\plugins\platforms\qwindows.dll", "platforms\qwindows.dll" )
#build_options = {"includes" : [ "re", "atexit" ], "include_files" : [ path_platforms ]}
includes = ["win32com","zmq", "zmq.utils.garbage", "zmq.backend.cython","atexit"]
build_options = {
    #"includes": 'atexit'
    "includes": includes
}

options = {
    'build_exe': build_options
}

executables = [
    Executable('ZeroFeederMainForm.py', base=base)
]

setup(name='ZeroFeeder',
      version='0.1',
      description='cx_Freeze ZeroFeederMainForm',
      options=options,
      executables=executables
      )