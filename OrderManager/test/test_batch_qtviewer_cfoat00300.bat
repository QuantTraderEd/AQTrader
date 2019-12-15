@echo off
echo start test_batch
cd ..
C:\ProgramData\Anaconda2\python.exe "C:\Program Files\JetBrains\PyCharm Community Edition 2019.1.3\helpers\pycharm\_jb_pytest_runner.py" --target test/test_qtviewer_cfoat00300.py::TestClass > test/log.txt
cd test
echo end test_batch
