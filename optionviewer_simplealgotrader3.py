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
        self.max_position = 1
        self.callShCode = ''
        self.putShCode = ''
        self.target_price = 0.5
        self.entry_counter1 = 0
        self.entry_counter2 = 0
        self.starthourshift = 0
        self.endhourshift = 0
        if self.callShCode != '' and self.putShCode != '':
            print self.callShCode, self.putShCode
            
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
            if nowtime.tm_hour == 9 + self.starthourshift and nowtime.tm_min >= 0 and nowtime.tm_min < 50:
                self.getTargetShortCD()
            return
        if nowtime.tm_hour == 9 + self.starthourshift and nowtime.tm_min > 22 and nowtime.tm_min < 50 and self.entry_counter1 < self.max_position:
            callbuysell = False
            callprice = 0.40
            callqty = 1

            putbuysell = False
            putprice = 0.40
            putqty = 1

            self.cur.execute("""SELECT Bid1,Time From TickData WHERE ShCode = ? ORDER BY TIME DESC LIMIT 1""",(self.callShCode,))
            row = self.cur.fetchone()
            callprice = float(row[0])

            self.cur.execute("""SELECT Bid1,Time From TickData WHERE ShCode = ? ORDER BY TIME DESC LIMIT 1""",(self.putShCode,))
            row = self.cur.fetchone()
            putprice = float(row[0])

            #print buysell,shcode,price,qty,time.strftime("%H:%M:%S",nowtime),row[1]

            if callprice < 1.5 and putprice < 1.5:
                if self.sendOrder(callbuysell,self.callShCode,callprice,callqty) and self.sendOrder(putbuysell,self.putShCode,putprice,putqty):
                    self.entry_counter1 += 1
            else:
                print 'this pair is imbalanced!!'


        elif nowtime.tm_hour == 14 + self.endhourshift and nowtime.tm_min > 42 and nowtime.tm_min < 45 and self.counter < self.max_position:
            #time.sleep(random.randint(0,2000) * 0.001)
            callbuysell = True
            callprice = 0.40
            callqty = 1

            putbuysell = True
            putprice = 0.40
            putqty = 1

            self.cur.execute("""SELECT Bid1,Time From TickData WHERE ShCode = ? ORDER BY TIME DESC LIMIT 1""",(self.callShCode,))
            row = self.cur.fetchone()
            callprice = float(row[0])

            self.cur.execute("""SELECT Bid1,Time From TickData WHERE ShCode = ? ORDER BY TIME DESC LIMIT 1""",(self.putShCode,))
            row = self.cur.fetchone()
            putprice = float(row[0])

            #print buysell,shcode,price,qty,time.strftime("%H:%M:%S",nowtime),row[1]

            if self.sendOrder(callbuysell,self.callShCode,callprice,callqty) and self.sendOrder(putbuysell,self.putShCode,putprice,putqty):
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
        starttime = '%.2d:57:30.000'%(8+self.starthourshift)
        endtime = '%.2d:59:59.000'%(8+self.starthourshift)

        nowtime = time.localtime()
        filedbname = time.strftime('TAQ_%Y%m%d.db',nowtime)

        if not os.path.isfile(filedbname):
            return

        conn = lite.connect(filedbname)

        target_min = 9999
        target_cd = ''
        target_price = '%.1f'%self.target_price

        sqltext = """
        SELECT Time, ShortCD, TAQ, LastPrice, LastQty, BuySell
        FROM FutOptTickData
        WHERE TAQ IN ('E')
        and Time between '%s' and '%s'
        and SUBSTR(ShortCD,1,3) = '201'
        Order by Time DESC
        """%(starttime,endtime)

        df = pd.read_sql(sqltext, conn)

        for shortcd in self._FeedCodeList.optionshcodelst:
            df_buffer = df[df['ShortCD'] == shortcd]
            if len(df_buffer) > 0:
                row = df_buffer.irow(-1)
                print row['ShortCD'], row['Time'],row['LastPrice']
                diff = abs(float(row['LastPrice']) - self.target_price)
                if diff < target_min and float(row['LastPrice']) < self.target_price * 1.2:
                    target_min = diff
                    target_cd = shortcd
                    target_price = row['LastPrice']

        #print target_cd, target_price
        self.callShCode = target_cd

        target_min = 9999
        target_cd = ''
        target_price = '%.1f'%self.target_price

        sqltext = """
        SELECT Time, ShortCD, TAQ, LastPrice, LastQty, BuySell
        FROM FutOptTickData
        WHERE TAQ IN ('E')
        and Time between '%s' and '%s'
        and SUBSTR(ShortCD,1,3) = '301'
        Order by Time DESC
        """%(starttime,endtime)

        df = pd.read_sql(sqltext, conn)

        for shortcd in self._FeedCodeList.optionshcodelst:
            df_buffer = df[df['ShortCD'] == shortcd]
            if len(df_buffer) > 0:
                row = df_buffer.irow(-1)
                print row['ShortCD'], row['Time'],row['LastPrice']
                diff = abs(float(row['LastPrice']) - self.target_price)
                if diff < target_min and float(row['LastPrice']) < self.target_price * 1.2:
                    target_min = diff
                    target_cd = shortcd
                    target_price = row['LastPrice']

        #print target_cd, target_price
        self.putShCode = target_cd

        print self.callShCode, self.putShCode

        conn.close()



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = SimpleAlgoTrader()
    wdg.initZMQ()
    wdg.initTimer()
    wdg.show()
    sys.exit(app.exec_())


