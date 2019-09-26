# -*- coding: utf-8 -*-

import os
import datetime as dt

now_dt = dt.datetime.now()
strdate = now_dt.strftime("%Y%m%d")
# strdate = '20190719'
os.chdir(os.path.dirname(os.path.abspath(__file__)))

result = os.system('runipy -o miniarb_research_template.ipynb')
if not result:
    result = os.system('jupyter nbconvert miniarb_research_template.ipynb')
    # result = os.system('ren miniarb_research_template.html miniarb_research_%s.html' % strdate)
    result = os.system('move miniarb_research_template.html ./miniarb_research/miniarb_research_%s.html' % strdate)
    print 'complete to make html'
else:
    print 'error to make run ipynb'
