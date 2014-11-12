# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 16:45:57 2013

@author: Administrator
"""

import sqlite3 as lite
import pandas as pd
from FeedCodeList import FeedCodeList

FeedCodeList_inst = FeedCodeList()
FeedCodeList_inst.ReadCodeListFile()


conn = lite.connect('TAQ_20141112.db')

#cursor = conn.cursor()
#cursor.execute("""SELECT * FROM FutOptTickData WHERE Time > '15:14:59.000' """)
#cursor.execute("""Select OrdNo, ExecNo, ShortCD,UnExecQty From OrderList 
#                                    WHERE OrdNo = ? and ExecNo is null """,('3640',))

#col_names = [cn[0] for cn in cursor.description]
#rows = cursor.fetchall()

#SELECT Time, ShortCD, AskQty2, AskQty1, Ask1, Bid1, BidQty1, BidQty2
#SELECT Time, ShortCD, Bid1, Ask1, BidQty1, AskQty1, Bid2, Ask2, BidQty2, AskQty2, Bid3, Ask3, BidQty3, AskQty3

sqltext = """ 
SELECT Time, ShortCD, TAQ, LastPrice, LastQty, BuySell
FROM FutOptTickData
WHERE TAQ IN ('E')
and Time between '08:55:00.000' and '08:59:30.000'
Order by ShortCD
"""

target_min = 9999
target_cd = ''
target_price = '1.5'

for shortcd in FeedCodeList_inst.optionshcodelst:
    sqltext = """
    SELECT Time, ShortCD, TAQ, LastPrice, LastQty, BuySell
    FROM FutOptTickData
    WHERE TAQ IN ('E')
    and Time between '08:55:00.000' and '08:59:30.000'
    and ShortCD = '%s'
    and SUBSTR(ShortCD,1,3) = '201'
    Order by Time DESC
    """%shortcd

    df = pd.read_sql(sqltext, conn)

    #print shortcd, len(df)
    if len(df) > 0:
        row = df.irow(0)
        print row['ShortCD'], row['Time'],row['LastPrice']
        diff = abs(float(row['LastPrice']) - 1.5)
        if diff < target_min:
            target_min = diff
            target_cd = shortcd
            target_price = row['LastPrice']

print target_cd, target_price



#print col_names
#for row in rows:
#    print row

#print "%s %-25s %-7s %-8s %-7s %-3s" %(col_names[0], col_names[1], col_names[2], col_names[3], col_names[4], col_names[5])
#
#for row in rows:
#    #print row
#    print "%2s %-25s %-7s %-8s %-7s %-3s" % row
    
#cursor.execute("UPDATE OrderList SET Qty = ? WHERE ID = ?",('10',1))
#conn.commit()

#orderitem = ('2013-10-29 09:00:01.789','True','A069500','26950','10')
#cursor.execute("INSERT INTO OrderList(Time,BuySell,ShortCD,Price,Qty) VALUES(?, ?, ?, ? ,?)",orderitem)            
#conn.commit()

conn.close()
