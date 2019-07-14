# -*- coding: utf-8 -*-

import os
import datetime as dt
now_dt = dt.datetime.now()
strdate = now_dt.strftime("%Y%m%d")
# strdate = '20170516'
os.chdir('D:/Python/ZeroTrader_Test/algo strategy')

result = os.system('runipy -o miniarb_research_template.ipynb')
if not result:
    result = os.system('jupyter nbconvert miniarb_research_template.ipynb')
    result = os.system('ren miniarb_research_template.html miniarb_research_%s.html' % strdate)
    print 'complete to make html'
else:
    print 'error to make run ipynb'