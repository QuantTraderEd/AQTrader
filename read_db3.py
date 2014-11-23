# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 23:00:00 2014

@author: assa
"""

import sqlite3 as lite
import pandas as pd

conn = lite.connect('./Data/TAQ_20141120.db')


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
AND ShortCD IN ('201JC250','301JC250')
Order by Time
"""

df = pd.read_sql(sqltext, conn)

df_call = df[df['ShortCD']=='201JC250']
df_put = df[df['ShortCD']=='301JC250']

