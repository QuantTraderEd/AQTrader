# -*- coding: utf-8 -*-

import logging
import datetime as dt
import sip
import redis

from logging.handlers import RotatingFileHandler
from PyQt4 import QtGui, QtCore
from optionwindow_thread import OptionViewerThread
from orderwidget import OptionViewerOrderWidget
from ui.mainwindow_ui import Ui_MainWindow
from commutil.FeedCodeList import FeedCodeList
from commutil import ExpireDateUtil


logger = logging.getLogger('OptionWindow')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
# fh = logging.FileHandler('OptionWindow.log')
fh = RotatingFileHandler('OptionWindow.log', maxBytes=5242, backupCount=3)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)


def convert(strprice):
    return '%.2f' % round(float(strprice), 2)


class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.port = 5501  # Real: 5501, RealTest 5502, BackTest 5503
        self.set_auto = False
        self.set_auto_config()

        self.initExpireDateUtil()
        self.initUI()
        sip.setdestroyonexit(False)
        self.initFeedCode()
        self.initStrikeList()
        self.initTableWidget()
        self.initThread()
        self.initTIMER()
        self.initData()
        self.onStart()

    def set_auto_config(self):
        setting = QtCore.QSettings("OptionWindow.ini", QtCore.QSettings.IniFormat)
        self.set_auto = setting.value("setauto", type=bool)
        if setting.value("port", type=int) != 0:
            self.port = setting.value("port", type=int)
        if self.set_auto:
            logger.info("setauto: True")
        else:
            logger.info("setauto: False")
        logger.info("zmq port: %d" % self.port)

    def closeEvent(self, event):
        self.mythread.stop()
        setting = QtCore.QSettings("OptionWindow.ini", QtCore.QSettings.IniFormat)
        setting.setValue("geometry", self.saveGeometry())
        setting.setValue("setauto", self.set_auto)
        setting.setValue("port", self.port)
        
    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionStart.triggered.connect(self.onStart)
        self.resize(800, 200)
        QtGui.qApp.setStyle('Cleanlooks')

        self.myOrderWidget = OptionViewerOrderWidget(self)
        self.myOrderWidget.initZMQ()

        setting = QtCore.QSettings("OptionWindow.ini", QtCore.QSettings.IniFormat)
        if setting.value("geometry"):
            self.restoreGeometry(setting.value("geometry").toByteArray())
            # self.restoreGeometry(setting.value("geometry"))
        pass

    def initTIMER(self):
        self.ctimer = QtCore.QTimer()
        self.ctimer.start(300000)
        self.ctimer.timeout.connect(self.ctimer_update)

    def initFeedCode(self):
        self._FeedCodeList = FeedCodeList()
        self._FeedCodeList.read_code_list()

    def initStrikeList(self):
        shortcdlist = self._FeedCodeList.option_shortcd_list
        self.shortcd_list = list([shortcd for shortcd in shortcdlist
                                   if shortcd[3:5] == self.expireMonthCode])
        self.strikelst = list(set([shortcd[-3:] for shortcd in shortcdlist
                                   if shortcd[3:5] == self.expireMonthCode]))
        self.strikelst.sort()
        self.strikelst.reverse()
        
    def initTableWidget(self):        
        self.ui.tableWidget.resizeColumnToContents(1)
        self.ui.tableWidget.resizeColumnToContents(2)
        self.ui.tableWidget.resizeColumnToContents(3)        
        self.ui.tableWidget.resizeColumnToContents(6)
        self.ui.tableWidget.resizeColumnToContents(7)
        self.ui.tableWidget.resizeColumnToContents(8)
        self.ui.tableWidget.resizeColumnToContents(11)
        self.ui.tableWidget.resizeColumnToContents(12)
        self.ui.tableWidget.resizeColumnToContents(13)
        
        self.ui.tableWidget.resizeColumnToContents(15)
        self.ui.tableWidget.resizeColumnToContents(16)
        
        self.ui.tableWidget.setColumnWidth(2, 41)    # call last
        self.ui.tableWidget.setColumnWidth(4, 41)    # call ask
        self.ui.tableWidget.setColumnWidth(5, 41)    # call bid
        self.ui.tableWidget.setColumnWidth(9, 41)    # put ask
        self.ui.tableWidget.setColumnWidth(10, 41)   # put bid
        self.ui.tableWidget.setColumnWidth(12, 41)   # put last

        self.ui.tableWidget.setRowCount(max(len(self.strikelst), 3))
        self.ui.tableWidget.resizeRowsToContents()        

        self.alignRightColumnList = [1, 3, 4, 8, 9]
        self.bidaskcolindex = [4, 5, 9, 10]
        self.synthbidaskcolindex = [15, 16]
        
        self.ui.tableWidget.cellDoubleClicked[int,int].connect(self.onDoubleClicked)
                                
        for i in xrange(len(self.strikelst)):
            if self.strikelst[i][-1] == '2' or self.strikelst[i][-1] == '7':
                strikeprice = self.strikelst[i] + '.5'
            else:
                strikeprice = self.strikelst[i] + '.0'             
            self.ui.tableWidget.setItem(i, 7, QtGui.QTableWidgetItem(strikeprice))

    def initThread(self):
        self.mythread = OptionViewerThread(port=self.port)
        self.mythread.receiveData[dict].connect(self.onReceiveData)

    def initExpireDateUtil(self):
        self.expiredate_util = ExpireDateUtil.ExpireDateUtil()
        now_dt = dt.datetime.now()
        today = now_dt.strftime('%Y%m%d')

        # self.expiredate_util.read_expire_date(os.path.dirname(ExpireDateUtil.__file__))
        self.expiredate_util.read_expire_date()
        expire_shortcd_lst = self.expiredate_util.make_expire_shortcd(today)
        logger.info('%s' % ','.join(expire_shortcd_lst))
        self.expireMonthCode = expire_shortcd_lst[0]
        logger.info('ExpireMonthCode: %s' % self.expireMonthCode)

    def initData(self):
        redis_client = redis.Redis(port=6479)
        bidqty1_dict = redis_client.hgetall('bidqty1_dict')
        bid1_dict = redis_client.hgetall('bid1_dict')
        ask1_dict = redis_client.hgetall('ask1_dict')
        askqty1_dict = redis_client.hgetall('askqty1_dict')
        last_dict = redis_client.hgetall('last_dict')
        lastqty_dict = redis_client.hgetall('lastqty_dict')
        
        for shortcd in self.shortcd_list:
            ask1 = ask1_dict.get(shortcd, 'n/a')
            bid1 = bid1_dict.get(shortcd, 'n/a')
            askqty1 = askqty1_dict.get(shortcd, 'n/a')
            bidqty1 = bidqty1_dict.get(shortcd, 'n/a')

            last = last_dict.get(shortcd, 'n/a')
            lastqty = lastqty_dict.get(shortcd, 'n/a')

            pos = self.strikelst.index(shortcd[5:8])

            if shortcd[:3] == '201':
                self.updateTableWidgetItem(pos, 0, shortcd)
                self.updateTableWidgetItem(pos, 1, lastqty)
                self.updateTableWidgetItem(pos, 2, last)
                self.updateTableWidgetItem(pos, 3, askqty1)
                self.updateTableWidgetItem(pos, 4, ask1)
                self.updateTableWidgetItem(pos, 5, bid1)
                self.updateTableWidgetItem(pos, 6, bidqty1)
            elif shortcd[:3] == '301':
                self.updateTableWidgetItem(pos, 14, shortcd)
                self.updateTableWidgetItem(pos, 8, askqty1)
                self.updateTableWidgetItem(pos, 9, ask1)
                self.updateTableWidgetItem(pos, 10, bid1)
                self.updateTableWidgetItem(pos, 11, bidqty1)
                self.updateTableWidgetItem(pos, 12, last)
                self.updateTableWidgetItem(pos, 13, lastqty)

        pass
        
    def onStart(self):
        if not self.mythread.isRunning():                        
            self.mythread.start()
        pass
    
    def ctimer_update(self):
        now_dt = dt.datetime.now()
        close_trigger = False
        if now_dt.hour == 6 and  now_dt.minute >= 15 and now_dt.minute <= 30:
            close_trigger = True

        if close_trigger:
            logger.info("close trigger")
            if self.mythread.isRunning():
                self.mythread.stop()
            self.close()

    def updateTableWidgetItem(self,row,col,text):
        widgetItem = self.ui.tableWidget.item(row,col)
        if not widgetItem:
            NewItem = QtGui.QTableWidgetItem(text)
            if col in self.alignRightColumnList: NewItem.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            self.ui.tableWidget.setItem(row,col,NewItem)
        else:
            if isinstance(text, int):
                widgetItem.setText(str(text))
            elif isinstance(text, float):
                widgetItem.setText("%.2f" % text)
        pass
    
    def onDoubleClicked(self, row, col):
        if col in self.bidaskcolindex:                        
            try:
                if col in self.bidaskcolindex[0:2]: shortcd = self.ui.tableWidget.item(row, 0).text()
                elif col in self.bidaskcolindex[2:4]: shortcd = self.ui.tableWidget.item(row, 14).text()
            except AttributeError:                    
                return
        elif col in self.synthbidaskcolindex:
            try:
                call_shortcd = self.ui.tableWidget.item(row, 0).text()
                put_shortcd = self.ui.tableWidget.item(row, 14).text()
            except AttributeError:
                return
            
        if col == self.bidaskcolindex[0] or col == self.bidaskcolindex[2]:                          
            price = float(self.ui.tableWidget.item(row,col).text())                
            buysell = True
        elif col == self.bidaskcolindex[1] or col == self.bidaskcolindex[3]:                    
            price = float(self.ui.tableWidget.item(row,col).text())
            buysell = False
        elif col == self.synthbidaskcolindex[0]:
            price = float(self.ui.tableWidget.item(row,self.synthbidaskcolindex[0]).text())
            if self.ui.tableWidget.item(row,self.bidaskcolindex[0]-2) is not None and \
            self.ui.tableWidget.item(row,self.bidaskcolindex[3]+2) is not None:
                call_price = float(self.ui.tableWidget.item(row,self.bidaskcolindex[0]-2).text())
                put_price = float(self.ui.tableWidget.item(row,self.bidaskcolindex[3]+2).text())
                buysell = True
            else:
                return
        elif col == self.synthbidaskcolindex[1]:
            price = float(self.ui.tableWidget.item(row,self.synthbidaskcolindex[1]).text())
            if self.ui.tableWidget.item(row,self.bidaskcolindex[0]-2) is not None and \
            self.ui.tableWidget.item(row,self.bidaskcolindex[3]+2) is not None:
                call_price = float(self.ui.tableWidget.item(row,self.bidaskcolindex[0]-2).text())
                put_price = float(self.ui.tableWidget.item(row,self.bidaskcolindex[3]+2).text())
                buysell = False
            else:
                return
        else:
            return
            
        item = self.ui.tableWidget.item(row,col)
        rect = self.ui.tableWidget.visualItemRect(item)
        win_pos = self.pos()
        rect.moveTo(rect.x() + win_pos.x() + rect.width()/2, rect.y() + win_pos.y() + rect.height() * 5)
        widget = QtGui.QWidget()
        widget.setGeometry(rect)
        
        if col in self.bidaskcolindex:                        
            self.myOrderWidget.initMove(widget)
            self.myOrderWidget.initOrder(shortcd, price, 1, buysell)
            self.myOrderWidget.show()
        elif col in self.synthbidaskcolindex:            
            self.myOrderWidget.initMove(widget)
            self.myOrderWidget.initSynthOrder(buysell, price, call_shortcd, call_price, put_shortcd, put_price, 1)
            self.myOrderWidget.show()
        pass

    def onReceiveData(self, msg_dict):
        nowtime = dt.datetime.now()
        shortcd = msg_dict['ShortCD']
        frontfutures_shortcd = self._FeedCodeList.future_shortcd_list[0]
        if msg_dict['SecuritiesType'] == 'futures' and msg_dict['TAQ'] == 'Q' and shortcd == frontfutures_shortcd:
            askqty1 = msg_dict['AskQty1']
            ask1 = msg_dict['Ask1']
            bid1 = msg_dict['Bid1']
            bidqty1 = msg_dict['BidQty1']
            
            if shortcd[:3] == '101':            
                showmsg = '%s, %s, %s, %s' % (askqty1, ask1, bid1, bidqty1)
                self.statusBar().showMessage(showmsg)                
            return
            
        if msg_dict['SecuritiesType'] != 'options': return

        if msg_dict['TAQ'] == 'Q':
            askqty1 = msg_dict['AskQty1']
            ask1 = msg_dict['Ask1']
            bid1 = msg_dict['Bid1']
            bidqty1 = msg_dict['BidQty1']
            
            # if msg_dict['SecuritiesType'] != 'options': return
            
            if shortcd[3:5] != self.expireMonthCode: return
            pos = self.strikelst.index(shortcd[5:8])

            if shortcd[:3] == '201':
                self.updateTableWidgetItem(pos,0,shortcd)
                self.updateTableWidgetItem(pos,3,askqty1)
                self.updateTableWidgetItem(pos,4,ask1)
                self.updateTableWidgetItem(pos,5,bid1)
                self.updateTableWidgetItem(pos,6,bidqty1)
            elif shortcd[:3] == '301':
                self.updateTableWidgetItem(pos,14,shortcd)
                self.updateTableWidgetItem(pos,8,askqty1)
                self.updateTableWidgetItem(pos,9,ask1)
                self.updateTableWidgetItem(pos,10,bid1)
                self.updateTableWidgetItem(pos,11,bidqty1)

            if not (nowtime.hour == 15 and (nowtime.minute >= 35 or nowtime.minute <= 45)):
                self.makeSyntheticBid(pos)
                self.makeSyntheticAsk(pos)

        elif msg_dict['TAQ'] == 'T':
            lastprice = msg_dict['LastPrice']
            lastqty = msg_dict['LastQty']
            
            if shortcd[3:5] != self.expireMonthCode: return
            pos = self.strikelst.index(shortcd[5:8])
            
            if shortcd[:3] == '201':                
                self.updateTableWidgetItem(pos,0,shortcd)
                self.updateTableWidgetItem(pos,2,lastprice)
                self.updateTableWidgetItem(pos,1,lastqty)
            elif shortcd[:3] == '301':                
                self.updateTableWidgetItem(pos,14,shortcd)
                self.updateTableWidgetItem(pos,12,lastprice)
                self.updateTableWidgetItem(pos,13,lastqty)                        
                
        elif msg_dict['TAQ'] == 'E' and msg_dict['SecuritiesType'] == 'options':
            shortcd = msg_dict['ShortCD']
            expectprice = msg_dict['ExpectPrice']
            expectqty = 'E'

            if shortcd[3:5] != self.expireMonthCode: return
            pos = self.strikelst.index(shortcd[5:8])
            
            if shortcd[:3] == '201':                
                self.updateTableWidgetItem(pos,0,shortcd)
                self.updateTableWidgetItem(pos,2,expectprice)
                self.updateTableWidgetItem(pos,1,expectqty)
            elif shortcd[:3] == '301':                
                self.updateTableWidgetItem(pos,14,shortcd)
                self.updateTableWidgetItem(pos,12,expectprice) 
                self.updateTableWidgetItem(pos,13,expectqty)
#            self.makeSyntheticExpect(pos)
                

#            if not (nowtime.hour == 17 and (nowtime.minute >= 0 or nowtime.minute <= 59)):
#                self.makeSyntheticBid(pos)
#                self.makeSyntheticAsk(pos)
        pass
    
    def makeSyntheticBid(self,pos):
        try:
            callbid = self.ui.tableWidget.item(pos,5).text()
            putask = self.ui.tableWidget.item(pos,9).text()
            strike = self.ui.tableWidget.item(pos,7).text()                    
            syntheticprice = float(callbid) - float(putask) + float(strike)
            if float(callbid) != 0 and float(putask):
                self.updateTableWidgetItem(pos,16,convert(syntheticprice))
        except:
            return
        pass
    
    def makeSyntheticAsk(self,pos):
        try:        
            callask = self.ui.tableWidget.item(pos,4).text()
            putbid = self.ui.tableWidget.item(pos,10).text()
            strike = self.ui.tableWidget.item(pos,7).text()                        
            syntheticprice = float(callask) - float(putbid) + float(strike)
            if float(callask) != 0 and float(putbid):
                self.updateTableWidgetItem(pos,15,convert(syntheticprice))
        except:
            return            
        pass
    
    def makeSyntheticExpect(self,pos):
        try:
            callexpect = self.ui.tableWidget.item(pos,2).text()
            putexpect = self.ui.tableWidget.item(pos,12).text()
            strike = self.ui.tableWidget.item(pos,7).text()            
            syntheticprice = float(callexpect) - float(putexpect) + float(strike)
            if float(callexpect) !=0 and float(putexpect) != 0:
                item = convert(syntheticprice)
                self.updateTableWidgetItem(pos,15,item)
                self.updateTableWidgetItem(pos,16,item)        
        except:
            return
        pass


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    if myform.set_auto:
        myform.onStart()
    app.exec_()   


