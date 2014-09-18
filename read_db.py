# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 16:45:57 2013

@author: Administrator
"""

import sqlite3 as lite
import pandas as pd

conn = lite.connect('OptionsTAQ_20140917.db')

cursor = conn.cursor()
cursor.execute('SELECT * FROM TickData')
#cursor.execute("""Select OrdNo, ExecNo, ShortCD,UnExecQty From OrderList 
#                                    WHERE OrdNo = ? and ExecNo is null """,('3640',))

col_names = [cn[0] for cn in cursor.description]
rows = cursor.fetchall()

sqltext = """ 
SELECT ShortCD, FeedSource, TAQ, SecuritiesType, Time, AskQty1, Ask1, Bid1, BidQty1  
FROM TickData
WHERE TAQ = 'Q'
AND ShortCD = '201JA265'
"""

df = pd.read_sql(sqltext, conn)

print df.head(100)

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
