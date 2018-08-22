# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pycybos",
    version="0.1",
    author="QuantTraderEd",
    description="Python package for Cybos API",
    url="https://github.com/QuantTraderEd/AQTrader/tree/master/PyCybos",
    packages=['pycybos'],
    long_description=open('README.md').read(),
    setup_requires=['pywin32>=220'],
    # packages=find_packages(exclude=['tests']),
    # test_suite=''
)
