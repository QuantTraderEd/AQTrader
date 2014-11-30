# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 23:00:00 2014

@author: assa
"""

import pylab
import sqlite3 as lite
import pandas as pd

conn = lite.connect('./SQLite/Data/TAQ_20141120.db')


sqltext = """
SELECT DISTINCT ShortCD
FROM FutOptTickData
WHERE TAQ IN ('E')
and Time between '08:58:00.000' and '08:59:30.000'
Order by ShortCD
"""

df = pd.read_sql(sqltext, conn)

call_lst = list(df[df['ShortCD'].str.contains('201')]['ShortCD'])
put_lst = list(df[df['ShortCD'].str.contains('301')]['ShortCD'])
option_lst = call_lst + put_lst

sqltext = """
SELECT Time, ShortCD, TAQ, LastPrice, LastQty, BuySell
FROM FutOptTickData
WHERE TAQ IN ('E')
and Time between '08:58:00.000' and '08:59:30.000'
Order by ShortCD
"""

df = pd.read_sql(sqltext, conn)

for shortcd in call_lst:
    df_buffer = df[df['ShortCD'] == shortcd]
    if len(df_buffer) > 0:
        row = df_buffer.irow(-1)
        print row['ShortCD'], row['Time'],row['LastPrice']

for shortcd in put_lst:
    df_buffer = df[df['ShortCD'] == shortcd]
    if len(df_buffer) > 0:
        row = df_buffer.irow(-1)
        print row['ShortCD'], row['Time'],row['LastPrice']

call_strike = [shortcd[-3:] for shortcd in call_lst]
put_strike = [shortcd[-3:] for shortcd in put_lst]

strike_lst = list(set(call_strike) & set(put_strike))


for strike in strike_lst:
    call_shortcd = '201JC' + strike
    put_shortcd = '301JC' + strike
    df_call = df[df['ShortCD'] == call_shortcd]
    df_put = df[df['ShortCD'] == put_shortcd]
    row_call = df_call.irow(-1)
    row_put = df_put.irow(-1)
    print row_call['ShortCD'], row_call['Time'],row_call['LastPrice']
    print row_put['ShortCD'], row_put['Time'],row_put['LastPrice']
    callputsum = float(row_call['LastPrice']) + float(row_put['LastPrice'])
    print strike, callputsum


sqltext = """
SELECT ShortCD, FeedSource, TAQ, SecuritiesType, Time, AskQty1, Ask1, Bid1, BidQty1
FROM FutOptTickData
WHERE TAQ = 'Q'
AND Time Between '09:00:00.000' and '10:00:00.000'
AND Bid1 > '0.00'
AND ShortCD IN ('201JC250','301JC250')
Order by Time
"""

df = pd.read_sql(sqltext, conn)

df_call = df[df['ShortCD']=='201JC250']
df_put = df[df['ShortCD']=='301JC250']

df_mid = pd.merge(df_call,df_put,on='Time',how='outer',sort=True)
df_mid = df_mid.fillna(method='pad')

df_mid = df_mid[['Time','ShortCD_x','AskQty1_x','Ask1_x','Bid1_x','BidQty1_x','ShortCD_y','AskQty1_y','Ask1_y','Bid1_y','BidQty1_y']]
df_mid = df_mid[df_mid['Bid1_y'].notnull()]


df_mid[['Ask1_x','Bid1_x','Ask1_y','Bid1_y']] = df_mid[['Ask1_x','Bid1_x','Ask1_y','Bid1_y']].astype(float)
df_mid['Syth_Bid'] = 250 + df_mid['Bid1_x'] - df_mid['Ask1_y']
df_mid['Syth_Ask'] = 250 + df_mid['Ask1_x'] - df_mid['Bid1_y']


#df_mid[['Time','Syth_Bid','Syth_Ask']].plot(x=df_mid['Time'])
#matplotlib.show()


sqltext = """
SELECT ShortCD, FeedSource, TAQ, SecuritiesType, Time, AskQty1, Ask1, Bid1, BidQty1
FROM FutOptTickData
WHERE TAQ = 'Q'
AND Time Between '09:00:00.000' and '10:00:00.000'
AND Bid1 > '0.00'
AND ShortCD IN ('201JC252','301JC252')
Order by Time
"""

df = pd.read_sql(sqltext, conn)

df_call = df[df['ShortCD']=='201JC252']
df_put = df[df['ShortCD']=='301JC252']

df_up = pd.merge(df_call,df_put,on='Time',how='outer',sort=True)
df_up = df_up.fillna(method='pad')

df_up = df_up[['Time','ShortCD_x','AskQty1_x','Ask1_x','Bid1_x','BidQty1_x','ShortCD_y','AskQty1_y','Ask1_y','Bid1_y','BidQty1_y']]
df_up = df_up[df_up['Bid1_y'].notnull()]


df_up[['Ask1_x','Bid1_x','Ask1_y','Bid1_y']] = df_up[['Ask1_x','Bid1_x','Ask1_y','Bid1_y']].astype(float)
df_up['Syth_Bid'] = 252.5 + df_up['Bid1_x'] - df_up['Ask1_y']
df_up['Syth_Ask'] = 252.5 + df_up['Ask1_x'] - df_up['Bid1_y']


#df_up[['Time','Syth_Bid','Syth_Ask']].plot(x=df_up['Time'])


sqltext = """
SELECT ShortCD, FeedSource, TAQ, SecuritiesType, Time, AskQty1, Ask1, Bid1, BidQty1
FROM FutOptTickData
WHERE TAQ = 'Q'
AND Time Between '09:00:00.000' and '10:00:00.000'
AND Bid1 > '0.00'
AND ShortCD IN ('201JC247','301JC247')
Order by Time
"""

df = pd.read_sql(sqltext, conn)

df_call = df[df['ShortCD']=='201JC247']
df_put = df[df['ShortCD']=='301JC247']

df_dn = pd.merge(df_call,df_put,on='Time',how='outer',sort=True)
df_dn = df_dn.fillna(method='pad')

df_dn = df_dn[['Time','ShortCD_x','AskQty1_x','Ask1_x','Bid1_x','BidQty1_x',
                        'ShortCD_y','AskQty1_y','Ask1_y','Bid1_y','BidQty1_y']]

df_dn = df_dn[df_dn['Bid1_y'].notnull()]


df_dn[['Ask1_x','Bid1_x','Ask1_y','Bid1_y']] = df_dn[['Ask1_x','Bid1_x','Ask1_y','Bid1_y']].astype(float)
df_dn['Syth_Bid'] = 247.5 + df_dn['Bid1_x'] - df_dn['Ask1_y']
df_dn['Syth_Ask'] = 247.5 + df_dn['Ask1_x'] - df_dn['Bid1_y']





df_syth = pd.merge(df_dn[['Time','Syth_Ask','Syth_Bid']],df_mid[['Time','Syth_Ask','Syth_Bid']],on='Time',how='outer',sort=True)
df_syth = df_syth.fillna(method='pad')
df_syth = df_syth[df_syth['Syth_Ask_y'].notnull()]

df_syth['Arb1'] = df_syth['Syth_Bid_x'] - df_syth['Syth_Ask_y']
df_syth['Arb2'] = df_syth['Syth_Bid_y'] - df_syth['Syth_Ask_x']

#df_syth[['Syth_Bid_x','Syth_Ask_x', 'Syth_Bid_y', 'Syth_Ask_y']].plot()
#pylab.show()
