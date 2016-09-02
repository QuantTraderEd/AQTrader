# -*- coding: utf-8 -*-

import sys
import logging
from datetime import datetime
import sip
from PyQt4 import QtGui, QtCore
from zerooptionviewer_thread import OptionViewerThread
from zerooptionviewer_orderwidget import OptionViewerOrderWidget
from ui_zerooptionviewer import Ui_MainWindow
from FeedCodeList import FeedCodeList

logger = logging.getLogger('ZeroOptionViewer')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('ZeroOptionViewer.log')
# fh = logging.Handlers.RotatingFileHandler('ZeroOptionViewer.log',maxBytes=104857,backupCount=3)
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
        self.initVar()
        self.initUI()
        self.initFeedCode()
        self.initStrikeList()
        self.initTableWidget()
        self.initThread()
        sip.setdestroyonexit(False)

    def closeEvent(self, event):
        self.mythread.stop()
        setting = QtCore.QSettings("ZeroOptionViewer.ini",QtCore.QSettings.IniFormat)
        setting.setValue("geometry", self.saveGeometry())

    def initVar(self):
        self.expireMonthCode = 'LA'
        
    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionStart.triggered.connect(self.onStart)
        self.resize(800, 200)
        self.myOrderWidget = OptionViewerOrderWidget(self)
        self.myOrderWidget.initZMQ()

        setting = QtCore.QSettings("ZeroOptionViewer.ini",QtCore.QSettings.IniFormat)
        if setting.value("geometry"):
            self.restoreGeometry(setting.value("geometry").toByteArray())
            # self.restoreGeometry(setting.value("geometry"))
        pass
        
    def initFeedCode(self):
        self._FeedCodeList = FeedCodeList()
        self._FeedCodeList.ReadCodeListFile()
        #for item in self._FeedCodeList.optionshcodelst:
        #    print item

    def initStrikeList(self):
        shcodelist = self._FeedCodeList.optionshcodelst
        self.strikelst = list(set([shcode[-3:] for shcode in shcodelist
                                   if shcode[3:5] == self.expireMonthCode]))
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
        
        self.ui.tableWidget.setColumnWidth(4,31)
        self.ui.tableWidget.setColumnWidth(5,31)
        self.ui.tableWidget.setColumnWidth(9,31)
        self.ui.tableWidget.setColumnWidth(10,31)
        
                
        self.ui.tableWidget.setRowCount(max(len(self.strikelst),3))
        self.ui.tableWidget.resizeRowsToContents()        

        self.alignRightColumnList = [1,3,8]        
        self.bidaskcolindex = [4,5,9,10]
        self.synthbidaskcolindex = [15,16]
        
        self.ui.tableWidget.cellDoubleClicked[int,int].connect(self.onDoubleClicked)
                                
        for i in xrange(len(self.strikelst)):
            if self.strikelst[i][-1] == '2' or self.strikelst[i][-1] == '7':
                strikeprice = self.strikelst[i] + '.5'
            else:
                strikeprice = self.strikelst[i] + '.0'             
            self.ui.tableWidget.setItem(i,7,QtGui.QTableWidgetItem(strikeprice))                
    
        
    def initThread(self):
        self.mythread = OptionViewerThread(None)
        self.mythread.receiveData[dict].connect(self.onReceiveData)
        
    def initData(self):
        shcode = '201J7267'                    
        ask1 = '0.64'
        bid1 = '0.63'
        askqty1 = '82'
        bidqty1 = '89'
        
        pos = self.strikelst.index(shcode[5:8])
        
        if shcode[:3] == '201':                
            self.updateTableWidgetItem(pos,0,shcode)
            self.updateTableWidgetItem(pos,3,askqty1)
            self.updateTableWidgetItem(pos,4,ask1)
            self.updateTableWidgetItem(pos,5,bid1)
            self.updateTableWidgetItem(pos,6,bidqty1)                
        elif shcode[:3] == '301':                
            self.updateTableWidgetItem(pos,14,shcode)
            self.updateTableWidgetItem(pos,8,askqty1)
            self.updateTableWidgetItem(pos,9,ask1)
            self.updateTableWidgetItem(pos,10,bid1)
            self.updateTableWidgetItem(pos,11,bidqty1)   
        pass
        
        
    def onStart(self):
        if not self.mythread.isRunning():                        
            self.mythread.start()
            #print "start"
        pass
    
    def updateTableWidgetItem(self,row,col,text):
        widgetItem = self.ui.tableWidget.item(row,col)
        if not widgetItem:
            NewItem = QtGui.QTableWidgetItem(text)
            if col in self.alignRightColumnList: NewItem.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            self.ui.tableWidget.setItem(row,col,NewItem)
        else:
            widgetItem.setText(text)
        pass
    
    def onDoubleClicked(self,row,col):   
        if col in self.bidaskcolindex:                        
            try:
                if col in self.bidaskcolindex[0:2]: shcode = self.ui.tableWidget.item(row,0).text()
                elif col in self.bidaskcolindex[2:4]: shcode = self.ui.tableWidget.item(row,14).text()                
            except AttributeError:                    
                return
        elif col in self.synthbidaskcolindex:
            try:
                callShCode = self.ui.tableWidget.item(row,0).text()
                putShCode = self.ui.tableWidget.item(row,14).text()                
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
            if self.ui.tableWidget.item(row,self.bidaskcolindex[0]-2) != None and \
            self.ui.tableWidget.item(row,self.bidaskcolindex[3]+2) != None:
                callPrice = float(self.ui.tableWidget.item(row,self.bidaskcolindex[0]-2).text())            
                putPrice = float(self.ui.tableWidget.item(row,self.bidaskcolindex[3]+2).text())            
                buysell = True
            else:
                return
        elif col == self.synthbidaskcolindex[1]:
            price = float(self.ui.tableWidget.item(row,self.synthbidaskcolindex[1]).text())
            if self.ui.tableWidget.item(row,self.bidaskcolindex[0]-2) != None and \
            self.ui.tableWidget.item(row,self.bidaskcolindex[3]+2) != None:
                callPrice = float(self.ui.tableWidget.item(row,self.bidaskcolindex[0]-2).text())            
                putPrice = float(self.ui.tableWidget.item(row,self.bidaskcolindex[3]+2).text())            
                buysell = False
            else:
                return
        else:
            return
            
        item = self.ui.tableWidget.item(row,col)
        rect = self.ui.tableWidget.visualItemRect(item)
        winPos = self.pos()
        rect.moveTo(rect.x() + winPos.x() + rect.width()/2, rect.y() + winPos.y() + rect.height() * 5)
        widget = QtGui.QWidget()
        widget.setGeometry(rect)
        
        if col in self.bidaskcolindex:                        
            self.myOrderWidget.initMove(widget)
            self.myOrderWidget.initOrder(buysell,shcode,price,1)
            self.myOrderWidget.show()
        elif col in self.synthbidaskcolindex:            
            self.myOrderWidget.initMove(widget)
            self.myOrderWidget.initSynthOrder(buysell,price,callShCode,callPrice,putShCode,putPrice,1)
            self.myOrderWidget.show()
        pass
        
        
    def onReceiveData(self,msg_dict):     
        nowtime = datetime.now()
        shortcd = msg_dict['ShortCD']
        if msg_dict['SecuritiesType'] == 'futures' and msg_dict['TAQ'] == 'Q':
            shortcd = msg_dict['ShortCD']
            askqty1 = msg_dict['AskQty1']
            ask1 = msg_dict['Ask1']
            bid1 = msg_dict['Bid1']
            bidqty1 = msg_dict['BidQty1']
            
            if shortcd[:3] == '101':            
                showmsg = '%s, %s, %s, %s' %(askqty1,ask1,bid1,bidqty1)
                self.statusBar().showMessage(showmsg)                
            return
            
        if msg_dict['SecuritiesType'] != 'options': return
        
        
        if msg_dict['TAQ'] == 'Q':
            askqty1 = msg_dict['AskQty1']
            ask1 = msg_dict['Ask1']
            bid1 = msg_dict['Bid1']
            bidqty1 = msg_dict['BidQty1']
            
            #if msg_dict['SecuritiesType'] != 'options': return
            
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
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    app.exec_()   


