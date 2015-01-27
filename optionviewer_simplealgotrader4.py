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

def convert_strike(strike):
    if type(strike).__name__ == 'unicode':
        if strike[2] == '2' or strike[2] == '7':
            return '%s.5'%strike
        else:
            return strike
    pass


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
        self.callShCode = ''
        self.putShCode = ''
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
            if nowtime.tm_hour == 15 + self.starthourshift and nowtime.tm_min >= 10 and nowtime.tm_min < 45:
                self.getTargetShortCD()
            return

        if nowtime.tm_hour == 15 + self.endhourshift and nowtime.tm_min == 13 and self.counter < self.max_position:
            if self.callShCode == '' or self.putShCode != '': return
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
        starttime = '%.2d:05:00.000'%(15+self.endhourshift)
        endtime = '%.2d:15:09.000'%(15+self.endhourshift)

        #starttime = '%.2d:18:30.000'%(9+self.starthourshift)
        #endtime = '%.2d:21:00.000'%(9+self.starthourshift)

        nowtime = time.localtime()
        filedbname = time.strftime('TAQ_%Y%m%d.db',nowtime)

        if not os.path.isfile(filedbname):
            print 'no filedb'
            return

        conn = lite.connect(filedbname)

        sql_text = """
        SELECT Time, ShortCD, LastPrice
        FROM FutOptTickData
        WHERE TAQ = 'E'
        and Time between '%s' and '%s'
        and substr(ShortCD,4,2) = '%s'
        """%(starttime,endtime,self.expireMonthCode)

        df = pd.read_sql(sql_text,conn)
        conn.close()
                
        df_call = df[df['ShortCD'].str[:3] == '201']
        df_put = df[df['ShortCD'].str[:3] == '301']
        
        #ShortCDSet = set(list(df['ShortCD']))
        #CallShortCDSet = set(df_call['ShortCD'])
        #PutShortCDSet = set(df_put['ShortCD'])
        
        StrikeLst = list(set(df_call['ShortCD'].str[-3:]).intersection(set(df_put['ShortCD'].str[-3:])))
        StrikeLst.sort()
        
        df_call_last = pd.DataFrame()
        df_put_last = pd.DataFrame()
        
        for strike in StrikeLst:
            shortcd = '201%s%s'%(self.expireMonthCode,strike)
            df_tmp = df[df['ShortCD'] == shortcd][-1:]
            df_tmp['Strike'] = convert_strike(strike)
            if len(df_call_last) == 0: df_call_last = df_tmp
            else: df_call_last = df_call_last.append(df_tmp)
            print shortcd
            shortcd = '301%s%s'%(self.expireMonthCode,strike)
            df_tmp = df[df['ShortCD'] == shortcd][-1:]
            df_tmp['Strike'] = convert_strike(strike)
            if len(df_put_last) == 0: df_put_last = df_tmp
            else: df_put_last = df_put_last.append(df_tmp)
            print shortcd

        df_syth = df_call_last.merge(df_put_last,left_on='Strike',right_on='Strike',how='outer')
        df_syth['SythPrice'] = df_syth['LastPrice_x'].astype(float) - df_syth['LastPrice_y'].astype(float) + df_syth['Strike'].astype(float)
        
        df_syth['Differ'] = abs(df_syth['LastPrice_x'].astype(float) - df_syth['LastPrice_y'].astype(float))
        df_syth = df_syth.sort('Differ')
        
        
        df_syth['Differ'] = abs(df_syth['LastPrice_x'].astype(float) - df_syth['LastPrice_y'].astype(float))
        df_syth = df_syth.sort('Differ')
        
        call_atm_price = df_syth.iloc[0]['LastPrice_x']
        put_atm_price = df_syth.iloc[0]['LastPrice_y']
        
        print call_atm_price, put_atm_price
        call_condition = (df_call_last['LastPrice'] <= call_atm_price) & (df_call_last['LastPrice'].astype(float) < 2.88)
        put_condition = (df_put_last['LastPrice'] <= put_atm_price) & (df_put_last['LastPrice'].astype(float) < 2.88)
        

        call_target_shortcd = df_call_last[call_condition].sort('LastPrice').iloc[0]['ShortCD']
        put_target_shortcd = df_put_last[put_condition].sort('LastPrice').iloc[0]['ShortCD']
                
        

        self.callShCode = call_target_shortcd
        self.putShCode = put_target_shortcd

        print self.callShCode, self.putShCode



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    wdg = SimpleAlgoTrader()
    wdg.initZMQ()
    wdg.initTimer()
    wdg.show()
    sys.exit(app.exec_())


