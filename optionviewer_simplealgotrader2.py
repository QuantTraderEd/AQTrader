# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 09:01:06 2014

@author: assa
"""

import os
import time
import zmq
import sqlite3 as lite
import pandas as pd
from PyQt4 import QtCore, QtGui
from zerooptionviewer_thread import OptionViewerThread
from FeedCodeList import FeedCodeList
from datetime import datetime

def convert(strprice):
    return '%.2f' %round(float(strprice),2)


class SimpleAlgoTrader(QtGui.QWidget):
    def __init__(self,parent = None, widget = None):
        QtGui.QWidget.__init__(self,parent)
        self.initUI()
        self.initVar()
        self.initDB()
        self.initFeedCode()
        self.initStrikeList()        
        self.initThread()
        pass
        
    def initUI(self):
        self.button = QtGui.QPushButton('Start', self)
        self.button.clicked.connect(self.onClick)
        self.button.move(60, 50)
        self.setWindowTitle('SpAgTder2')
        self.resize(200, 120)
        pass
    
    def initVar(self):
        self.counter = 0
        self.counter1 = 0
        self.callShCode = ''
        self.putShCode = ''
        self.entry_counter1 = 0
        self.entry_counter2 = 0
        self.starthourshift = 1
        self.endhourshift = 1
        pass

    def initDB(self):
        self.conn = lite.connect(":memory:")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE TickData
             (Time text, ShCode text, AskQty1 text, Ask1 text, Bid1 text, BidQty1 text)""")
        pass
        
    def initFeedCode(self):
        self._FeedCodeList = FeedCodeList()
        self._FeedCodeList.ReadCodeListFile()
        pass
        
    def initZMQ(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:6000")
        pass
    
    def initThread(self):
        self.mythread = OptionViewerThread(None)
        self.mythread.receiveData[str].connect(self.onReceiveData)
        pass
    
    def initTimer(self):
        self.XTimer = QtCore.QTimer()
        self.XTimer.timeout.connect(self.onXTimerUpdate)
        pass
        
    def initStrikeList(self):
        shcodelist = self._FeedCodeList.optionshcodelst
        self.strikelst = list(set([shcode[-3:] for shcode in shcodelist]))
        self.strikelst.sort()
        self.strikelst.reverse()
        pass
    
    def onClick(self):        
        if not self.mythread.isRunning() and not self.XTimer.isActive():                        
            self.mythread.start()
            self.XTimer.start(3222)
            self.button.setText('Stop')
        else:
            self.XTimer.stop()
            self.mythread.terminate()
            self.button.setText('Start')
        pass
    
    def onReceiveData(self,msg):
        if self.callShCode == '' or self.putShCode == '':
            return
        nowtime = datetime.now()
        strnowtime = datetime.strftime(nowtime,'%H:%M:%S.%f')[:-3]
        lst = msg.split(',')
        if lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'options':
            shcode = str(lst[4])
            ask1 = convert(lst[6])
            bid1 = convert(lst[23])
            askqty1 = str(lst[11])
            bidqty1 = str(lst[28])

            if shcode in [self.callShCode,self.putShCode]:
                taqitem = (strnowtime,shcode,askqty1,ask1,bid1,bidqty1)
                #print lst[0],taqitem
                self.cur.execute("""INSERT INTO TickData(Time,ShCode,AskQty1,Ask1,Bid1,BidQty1)
                                                VALUES(?, ?, ?, ? ,?, ?)""",taqitem)
                self.conn.commit()
        pass
    
    def onXTimerUpdate(self):        
        nowtime = time.localtime()
        if self.callShCode == '' or self.putShCode == '':
            if nowtime.tm_hour == 8 + self.starthourshift and nowtime.tm_min > 59 and nowtime.tm_min > 30:
                self.getTargetShortCD()
            return
        if nowtime.tm_hour == 9 + self.starthourshift and nowtime.tm_min > 22 and nowtime.tm_min < 25 and self.entry_counter1 < 15:
            buysell = False
            shcode = self.callShCode
            price = 0.40
            qty = 1

            self.cur.execute("""SELECT Bid1,Time From TickData WHERE ShCode = ? ORDER BY TIME DESC LIMIT 1""",(shcode,))
            row = self.cur.fetchone()
            price = float(row[0])

            #print buysell,shcode,price,qty,time.strftime("%H:%M:%S",nowtime),row[1]
            self.sendOrder(buysell,shcode,price,qty)

            buysell = False
            shcode = self.putShCode
            price = 0.40
            qty = 1

            self.cur.execute("""SELECT Bid1,Time From TickData WHERE ShCode = ? ORDER BY TIME DESC LIMIT 1""",(shcode,))
            row = self.cur.fetchone()
            price = float(row[0])

            #print buysell,shcode,price,qty,time.strftime("%H:%M:%S",nowtime),row[1]
            if self.sendOrder(buysell,shcode,price,qty):
                self.entry_counter1+=1

        elif nowtime.tm_hour == 11 + self.starthourshift and nowtime.tm_min > 23 and nowtime.tm_min < 27 and self.entry_counter2 < 15:
            buysell = False
            shcode = self.callShCode
            price = 0.40
            qty = 1

            self.cur.execute("""SELECT Bid1 From TickData WHERE ShCode = ? ORDER BY TIME DESC LIMIT 1""",(shcode,))
            row = self.cur.fetchone()
            price = float(row[0])

            #print buysell,shcode,price,qty
            self.sendOrder(buysell,shcode,price,qty)

            buysell = False
            shcode = self.putShCode
            price = 0.40
            qty = 1

            self.cur.execute("""SELECT Bid1 From TickData WHERE ShCode = ? ORDER BY TIME DESC LIMIT 1""",(shcode,))
            row = self.cur.fetchone()
            price = float(row[0])

            #print buysell,shcode,price,qty
            if self.sendOrder(buysell,shcode,price,qty):
                self.entry_counter2+=1

        elif nowtime.tm_hour == 14 + self.endhourshift and nowtime.tm_min > 42 and nowtime.tm_min < 45 and self.counter < 30:
            #time.sleep(random.randint(0,2000) * 0.001)
            buysell = True
            shcode = self.callShCode
            price = 1.90
            qty = 1

            self.cur.execute("""SELECT Ask1 From TickData WHERE ShCode = ? ORDER BY TIME DESC LIMIT 1""",(shcode,))
            row = self.cur.fetchone()
            price = float(row[0])
            #print buysell,shcode,price,qty
            self.sendOrder(buysell,shcode,price,qty)

            buysell = True
            shcode = self.putShCode
            price = 1.90
            qty = 1

            self.cur.execute("""SELECT Ask1 From TickData WHERE ShCode = ? ORDER BY TIME DESC LIMIT 1""",(shcode,))
            row = self.cur.fetchone()
            price = float(row[0])

            #print buysell,shcode,price,qty
            if self.sendOrder(buysell,shcode,price,qty):
                self.counter+=1

        pass

    def sendOrder(self,buysell,shcode,price,qty):
        if type(self.socket).__name__ == 'Socket':
            msg = str(buysell) + ',' + str(shcode) + ',' + str(price) + ',' + str(qty)
            print msg
            self.socket.send(msg)
            msg_in = self.socket.recv()
            print msg_in
            return True
        else:
            print 'not define socket..'
            return False
        pass

    def getTargetShortCD(self):
        target_min = 9999
        target_cd = ''
        target_price = '1.5'

        starttime = '%.2d:55:00.000'%(8+self.starthourshift)
        endtime = '%.2d:59:30.000'%(8+self.starthourshift)

        nowtime = time.localtime()
        filedbname = time.strftime('TAQ_%Y%m%d.db',nowtime)

        if not os.path.isfile(filedbname):
            return

        conn = lite.connect(filedbname)

        for shortcd in self._FeedCodeList.optionshcodelst:
            sqltext = """
            SELECT Time, ShortCD, TAQ, LastPrice, LastQty, BuySell
            FROM FutOptTickData
            WHERE TAQ IN ('E')
            and Time between '%s' and '%s'
            and ShortCD = '%s'
            and SUBSTR(ShortCD,1,3) = '201'
            Order by Time DESC LIMIT 1
            """%(starttime,endtime,shortcd)

            df = pd.read_sql(sqltext, conn)

            #print shortcd, len(df)
            if len(df) > 0:
                row = df.irow(0)
                #print row['ShortCD'], row['Time'],row['LastPrice']
                diff = abs(float(row['LastPrice']) - 1.5)
                if diff < target_min:
                    target_min = diff
                    target_cd = shortcd
                    target_price = row['LastPrice']

        #print target_cd, target_price
        self.callShCode = target_cd

        target_min = 9999
        target_cd = ''
        target_price = '1.5'

        for shortcd in self._FeedCodeList.optionshcodelst:
            sqltext = """
            SELECT Time, ShortCD, TAQ, LastPrice, LastQty, BuySell
            FROM FutOptTickData
            WHERE TAQ IN ('E')
            and Time between '%s' and '%s'
            and ShortCD = '%s'
            and SUBSTR(ShortCD,1,3) = '301'
            Order by Time DESC LIMIT 1
            """%(starttime,endtime,shortcd)

            df = pd.read_sql(sqltext, conn)

            #print shortcd, len(df)
            if len(df) > 0:
                row = df.irow(0)
                #print row['ShortCD'], row['Time'],row['LastPrice']
                diff = abs(float(row['LastPrice']) - 1.5)
                if diff < target_min:
                    target_min = diff
                    target_cd = shortcd
                    target_price = row['LastPrice']

        #print target_cd, target_price
        self.putShCode = target_cd

        conn.close()



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = SimpleAlgoTrader()
    wdg.initZMQ()
    wdg.initTimer()
    wdg.show()    
    sys.exit(app.exec_())
        
