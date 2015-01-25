# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 09:01:06 2015

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
        self.setWindowTitle('SpAgTder4')
        self.resize(200, 120)
        pass

    def initVar(self):
        self.counter = 0
        self.counter1 = 0
        self.max_position = 1
        self.expireMonthCode = 'K2'
        self.callShCode = '201K2252'
        self.putShCode = '301K2250'
        self.callmidprice = 0
        self.putmidprice = 0
        self.target_price = 1.00
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
             (Time text, ShCode text, LastPrice TEXT, LastQty TEXT)""")
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
        if lst[1] == 'cybos' and lst[2] == 'E' and lst[3] == 'options':
            shcode = str(lst[4])
            expectprice = convert(lst[6])
            expectqty = 'E'

            if shcode in [self.callShCode,self.putShCode]:
                if shcode[:3] == '201': self.callmidprice = expectprice
                if shcode[:3] == '301': self.putmidprice = expectprice
                #print self.callShCode, self.callmidprice, self.putShCode, self.putmidprice,
                #print 'strangle price:', float(self.callmidprice) + float(self.putmidprice)
                taqitem = (strnowtime,shcode,expectprice,expectqty)
                #print lst[0],taqitem
                self.cur.execute("""INSERT INTO TickData(Time,ShCode,LastPrice,LastQty)
                                                VALUES(?, ?, ?, ?)""",taqitem)
                self.conn.commit()
        pass

    def onXTimerUpdate(self):
        nowtime = time.localtime()
        if self.callShCode == '' or self.putShCode == '':
            if nowtime.tm_hour == 9 + self.starthourshift and nowtime.tm_min >= 0 and nowtime.tm_min < 50:
            #if nowtime.tm_hour == 9 + self.starthourshift and nowtime.tm_min >= 20 and nowtime.tm_min < 22:
                self.getTargetShortCD()
            return

        if nowtime.tm_hour == 15 + self.endhourshift and nowtime.tm_min == 13 and self.counter < self.max_position:
            #time.sleep(random.randint(0,2000) * 0.001)
            callbuysell = True
            callprice = 0.40
            callqty = 2

            putbuysell = True
            putprice = 0.40
            putqty = 2

            self.cur.execute("""SELECT LastPrice,Time From TickData WHERE ShCode = ? ORDER BY TIME DESC LIMIT 1""",(self.callShCode,))
            row = self.cur.fetchone()
            callprice = round(float(row[0]) + 0.12,2)

            self.cur.execute("""SELECT LastPrice,Time From TickData WHERE ShCode = ? ORDER BY TIME DESC LIMIT 1""",(self.putShCode,))
            row = self.cur.fetchone()
            putprice = round(float(row[0]) + 0.12,2)

            #print buysell,shcode,price,qty,time.strftime("%H:%M:%S",nowtime),row[1]
            print 'call: ', self.callShCode, callprice, callqty,'put: ', self.putShCode, putprice, putqty


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

        #starttime = '%.2d:18:30.000'%(9+self.starthourshift)
        #endtime = '%.2d:21:00.000'%(9+self.starthourshift)

        nowtime = time.localtime()
        filedbname = time.strftime('TAQ_%Y%m%d.db',nowtime)

        if not os.path.isfile(filedbname):
            print 'no filedb'
            return

        conn = lite.connect(filedbname)

        target_min = 9999
        target_cd = ''
        target_price = '%.1f'%self.target_price

        if endtime < '%.2d:00:00.000'%(9+self.starthourshift):
            sqltext = """
            SELECT Time, ShortCD, TAQ, LastPrice, LastQty, BuySell
            FROM FutOptTickData
            WHERE TAQ IN ('E')
            and Time between '%s' and '%s'
            Order by Time DESC
            """%(starttime,endtime)
        else:
            sqltext = """
            SELECT Time, ShortCD, TAQ, Ask1, Bid1
            FROM FutOptTickData
            WHERE TAQ ='Q'
            and Time between '%s' and '%s'
            Order by Time DESC
            """%(starttime,endtime)

        df = pd.read_sql(sqltext, conn)
        df_call = df[df['ShortCD'].str.contains('201' + self.expireMonthCode)]
        df_put = df[df['ShortCD'].str.contains('301' + self.expireMonthCode)]

        conn.close()

        if len(df) == 0:
            print 'no expection price in db'
            return


        for shortcd in self._FeedCodeList.optionshcodelst:
            df_buffer = df_call[df_call['ShortCD'] == shortcd]
            if len(df_buffer) > 0:
                row = df_buffer.irow(-1)
                if row['TAQ'] == 'Q':
                    print row['ShortCD'], row['Time'],row['Ask1'],row['Bid1']
                    midprice = (float(row['Ask1']) + float(row['Bid1'])) / 2
                    diff = abs(midprice - self.target_price)
                    if diff < target_min and midprice < self.target_price * 1.2:
                        target_min = diff
                        target_cd = shortcd
                elif row['TAQ'] == 'E':
                    print row['ShortCD'], row['Time'],row['LastPrice']
                    midprice =  float(row['LastPrice'])
                    diff = abs(midprice - self.target_price)
                    if diff < target_min and midprice < self.target_price * 1.2:
                        target_min = diff
                        target_cd = shortcd


        self.callShCode = target_cd

        target_min = 9999
        target_cd = ''


        for shortcd in self._FeedCodeList.optionshcodelst:
            df_buffer = df_put[df_put['ShortCD'] == shortcd]
            if len(df_buffer) > 0:
                row = df_buffer.irow(-1)
                if row['TAQ'] == 'Q':
                    print row['ShortCD'], row['Time'],row['Ask1'],row['Bid1']
                    midprice = (float(row['Ask1']) + float(row['Bid1'])) / 2
                    diff = abs(midprice - self.target_price)
                    if diff < target_min and midprice < self.target_price * 1.2:
                        target_min = diff
                        target_cd = shortcd
                elif row['TAQ'] == 'E':
                    print row['ShortCD'], row['Time'],row['LastPrice']
                    midprice =  float(row['LastPrice'])
                    diff = abs(midprice - self.target_price)
                    if diff < target_min and midprice < self.target_price * 1.2:
                        target_min = diff
                        target_cd = shortcd



        self.putShCode = target_cd

        print self.callShCode, self.putShCode





if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = SimpleAlgoTrader()
    wdg.initZMQ()
    wdg.initTimer()
    wdg.show()
    sys.exit(app.exec_())


