
import os
import shutil
import datetime as dt
import pycybos as pc
import ExpireDateUtil as ExpireDateUtil

FutureCode = pc.CpFutureCode()
OptionCode = pc.CpOptionCode()
expiredate_util = ExpireDateUtil.ExpireDateUtil()

now_dt = dt.datetime.now()
today = now_dt.strftime('%Y%m%d')

expiredate_util.read_expire_date(os.path.dirname(ExpireDateUtil.__file__)+"\\expire_date.txt")
expire_code_lst = expiredate_util.make_expire_shortcd(today)
print expire_code_lst

filename = 'feedcodelist.txt'

f = open('feedcodelist.txt', 'w+')

big_shortcd1 = FutureCode.GetData('0', 0)
big_shortcd2 = FutureCode.GetData('0', 1)
# mini_shortcd1 = '105LB000'
# mini_shortcd2 = '105LC000'
mini_shortcd1 = '105%s000' % (expire_code_lst[0])
mini_shortcd2 = '105%s000' % (expire_code_lst[1])
f.write('<Futures/>\n')
f.write(big_shortcd1 + '000\n')
f.write(big_shortcd2 + '000\n')
f.write(mini_shortcd1 + '\n')
f.write(mini_shortcd2 + '\n')
print big_shortcd1
print big_shortcd2
print mini_shortcd1
print mini_shortcd2

f.write('<Options/>\n')

for i in xrange(OptionCode.GetCount()):
    shortcd = OptionCode.GetData('0',i)    
    if shortcd[3:5] in expire_code_lst:
        print shortcd
        f.write(shortcd+'\n')


f.write('<Equity/>\n')

EquityList = [
'069500',
'114800',
'102110',
'123310',
'105190',
'145670',
'122630',
'123320',
]

for shortcd in EquityList:
    print shortcd
    f.write(shortcd+'\n')

f.write('<Index/>\n')
f.write('U180\n')

        
f.close()

# for item in filepath:
#     src = os.getcwd() + '\\'  + filename
#     des = item+filename
#     print src
#     print des
#     shutil.copyfile(src,des)