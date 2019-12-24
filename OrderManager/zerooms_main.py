# -*- coding: utf-8 -*-

import time
import re
import pythoncom
import ctypes

import logging
import datetime as dt
import pyxing as px
import sqlite3 as lite
import pandas as pd

from os import path
from PyQt4 import QtCore, QtGui
from ui_zerooms import Ui_MainWindow
from xinglogindlg import LoginForm
from zerooms_thread import OrderMachineNewThread
from orderlistdlg_main import OrderListDialog
from zerodigitviewer.zerodigitviewer_main import ZeroDigitViewer, observer_CEXAQ31100
from zeropositionviewer.zeropositionviewer import ZeroPositionViewer

from weakref import proxy

import commutil.ExpireDateUtil as ExpireDateUtil

logger = logging.getLogger('ZeroOMS')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('ZeroOMS.log')
# fh = logging.Handlers.RotatingFileHandler('ZeroOMS.log',maxBytes=104857,backupCount=3)
fh.setLevel(logging.INFO)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s '
                              '%(filename)s %(funcName)s() %(lineno)d:\t\t'
                              '%(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)


class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.order_port = 6001   # real: 6001 test: 6002
        self.exec_port = 7001    # real: 7001 test: 7002
        self.accountindex = 1
        self.db_path = path.dirname(__file__) + '/orderlist_db/'  # './orderlist_db/'
        self.set_auto = False
        self.auto_config = self.set_auto_config()

        self.initUI()

        self.ctimer = QtCore.QTimer()
        self.ctimer.start(1000)
        self.ctimer.timeout.connect(self.ctimerUpdate)
        self.autotimer = QtCore.QTimer()
        self.autotimer.start(20000)
        self.autotimer.timeout.connect(self.autotimer_update)
        self.xingTimer = QtCore.QTimer()
        self.xingTimer.timeout.connect(self.xingTimerUpdate)
        
        self.FuturesOptionTAQFeederLst = []
        self.EquityTAQFeederLst = []
        
        self.XASession_observer = XingXASessionUpdate(proxy(self.status_xi))
        self.XASession = px.XASession()
        self.XASession.Attach(self.XASession_observer)
        self.accountlist = []
        self.servername = ''

        now_dt = dt.datetime.now()

        if now_dt.hour >= 7 and now_dt.hour < 17:
            self.exchange_code = 'KRX'
        else:
            self.exchange_code = 'EUREX'
        logger.info("exchange_code: %s" % self.exchange_code)

        self.initDB()
        self.initThread()
        self.initExpireDateUtil()

        if self.set_auto:
            self.auto_start_xing(self.auto_config)

        logger.info('Start ZeroOMS')
        pass

    def set_auto_config(self):
        setting = QtCore.QSettings("ZeroOMS.ini", QtCore.QSettings.IniFormat)
        self.set_auto = setting.value("setauto", type=bool)
        if setting.value("order_port", type=int) != 0:
            self.order_port = setting.value("order_port", type=int)
        if setting.value("exec_port", type=int) != 0:
            self.exec_port = setting.value("exec_port", type=int)
        auto_config = dict()
        auto_config['id'] = str(setting.value("id", type=str))
        auto_config['pwd'] = str(setting.value("pwd", type=str))
        auto_config['cetpwd'] = str(setting.value("cetpwd", type=str))
        auto_config['servertype'] = setting.value("servertype", type=int)
        if self.set_auto:
            logger.info("setauto: True")
        else:
            logger.info("setauto: False")
        logger.info("order_port: %d" % self.order_port)
        logger.info("exec_port: %d" % self.exec_port)
        print auto_config
        return auto_config

    def closeEvent(self, event):
        self.XASession.DisconnectServer()
        setting = QtCore.QSettings("ZeroOMS.ini", QtCore.QSettings.IniFormat)
        setting.setValue("OMS_Geometry", self.saveGeometry())
        setting.setValue("OrdListDlg_Geometry", self.myOrdListDlg.saveGeometry())
        setting.setValue("PositionViewer_Geometry", self.myPositionViewer.saveGeometry())
        setting.setValue("DigitViewer_Geometry", self.myDigitViewer.saveGeometry())
        setting.setValue("OrdListDlg_Show", self.myOrdListDlg.isVisible())
        setting.setValue("PositionViewer_Show", self.myPositionViewer.isVisible())
        setting.setValue("DigitViewer_Show", self.myDigitViewer.isVisible())
        setting.setValue("setauto", self.set_auto)
        setting.setValue("order_port", self.order_port)
        setting.setValue("exec_port", self.exec_port)
        self.myOrdListDlg.close()
        self.myPositionViewer.close()
        self.myDigitViewer.close()
        logger.info("Close ZeroOMS")
        event.accept()
        super(MainForm, self).closeEvent(event)
        ctypes.windll.user32.PostQuitMessage(0)

    def initUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.labelTimer = QtGui.QLabel(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        self.ui.statusbar.addPermanentWidget(self.labelTimer)

        QtGui.qApp.setStyle('Cleanlooks')

        self.conn_xi = QtGui.QTableWidgetItem("conn xi")
        self.status_xi = QtGui.QTableWidgetItem("ready")
        self.ui.tableWidget.setItem(0,2,self.conn_xi)
        self.ui.tableWidget.setItem(0,1,self.status_xi)

        self.myOrdListDlg = OrderListDialog(order_port=self.order_port)
        self.myPositionViewer = ZeroPositionViewer()
        self.myDigitViewer = ZeroDigitViewer()

        self.ui.actionDigitView.triggered.connect(self.triggeredDigitViewer)
        self.ui.actionPositionView.triggered.connect(self.trigeredPositionViewer)

        setting = QtCore.QSettings("ZeroOMS.ini", QtCore.QSettings.IniFormat)
        self.restoreGeometry(setting.value("OMS_Geometry").toByteArray())
        self.myOrdListDlg.restoreGeometry(setting.value("OrdListDlg_Geometry").toByteArray())
        self.myPositionViewer.restoreGeometry(setting.value("PositionViewer_Geometry").toByteArray())
        self.myDigitViewer.restoreGeometry(setting.value("DigitViewer_Geometry").toByteArray())
        if setting.value("OrdListDlg_Show").toBool():
            self.myOrdListDlg.show()
        if setting.value("PositionViewer_Show").toBool():
            self.myPositionViewer.show()
        if setting.value("DigitViewer_Show").toBool():
            self.myDigitViewer.show()

    def initDB(self):
        nowtime = time.localtime()
        strtime = time.strftime('%Y%m%d', nowtime)
        if nowtime.tm_hour >= 6 and nowtime.tm_hour < 17:
            strdbname = "orderlist_%s.db" % strtime
        elif nowtime.tm_hour >= 17:
            strdbname = "orderlist_night_%s.db" % strtime
        elif nowtime.tm_hour < 6:
            strtime = "%d%.2d%.2d" % (nowtime.tm_year, nowtime.tm_mon, nowtime.tm_mday-1)
            strdbname = "orderlist_night_%s.db" % strtime

        strdbname = self.db_path + strdbname
        logger.info("Order List DB: %s" % strdbname)

        if not path.isfile(strdbname):
            self.conn_db = lite.connect(strdbname)
            self.create_db_table()
            self.conn_db.close()
            logger.info('Init New OrdList DB File: %s' % strdbname)
        else:
            self.conn_db = lite.connect(strdbname)
            sql_text = "SELECT name FROM sqlite_master WHERE type='table'"
            df_master = pd.read_sql(sql_text, self.conn_db)
            if df_master['name'][0] != 'OrderList':
                self.create_db_table()
            self.conn_db.close()

        self.myOrdListDlg.init_dbname(strdbname)

    def create_db_table(self):
        self.cursor_db = self.conn_db.cursor()
        self.cursor_db.execute("""CREATE TABLE OrderList(Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                   AutoTraderID TEXT,
                                                   OrdNo TEXT,
                                                   OrgOrdNo TEXT,
                                                   ExecNo TEXT,
                                                   Time TEXT,                  
                                                   BuySell TEXT,                                       
                                                   ShortCD TEXT,
                                                   Price TEXT,
                                                   Qty TEXT,
                                                   Type1 TEXT,
                                                   Type2 TEXT,
                                                   ExecPrice TEXT,
                                                   ExecQty TEXT,
                                                   UnExecQty TEXT,
                                                   ChkReq TEXT
                                                   )""")

    def initThread(self):
        logger.info("order_port->%d, exec_report_port->%d" % (self.order_port, self.exec_port))
        self.ordermachineThread = OrderMachineNewThread(order_port=self.order_port, exec_report_port=self.exec_port)
        self.ordermachineThread._XASession = proxy(self.XASession)
        self.ordermachineThread.db_path = self.db_path
        self.ordermachineThread.init_func()
        # self.connect(self.executerThread,QtCore.SIGNAL("OnUpdateDB (QString)"),self.NotifyOrderListViewer)
        self.ordermachineThread.threadUpdateDB.connect(self.NotifyOrderListViewer)
        self.ordermachineThread.finished.connect(self.NotifyThreadEnd)
        if self.accountindex == 1:
            self.ordermachineThread.fo_account_index = 1
            self.ordermachineThread.eq_account_index = 0
        elif self.accountindex == 0:
            self.ordermachineThread.fo_account_index = 0
            self.ordermachineThread.eq_account_index = 1
        pass

    def initExpireDateUtil(self):
        self.expiredate_util = ExpireDateUtil.ExpireDateUtil()
        now_dt = dt.datetime.now()
        today = now_dt.strftime('%Y%m%d')

        self.expiredate_util.read_expire_date(path.dirname(ExpireDateUtil.__file__) + "\\expire_date.txt")
        expire_date_lst = self.expiredate_util.make_expire_date(today)
        logger.info('%s' % ','.join(expire_date_lst))

    def ctimerUpdate(self):
        self.labelTimer.setText(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def slot_StartXingDlg(self, row, column):
        if row == 0 and column == 2:
            # print("Row %d and Column %d was doblueclicked" % (row,column))
            myform = LoginForm(self, proxy(self.XASession))
            myform.show()
            myform.exec_()
            self.start_xing_query()
        pass
            
    def auto_start_xing(self, auto_config):
        server = 'hts.ebestsec.co.kr'
        port = 20001
        servertype = 0
        showcerterror = 1
        user = str(auto_config['id'])
        password = str(auto_config['pwd'].decode('hex'))
        certpw = str(auto_config['cetpwd'].decode('hex'))
        servertype = int(auto_config['servertype'])
        if servertype == 1:
            server = 'demo.ebestsec.co.kr'
        elif servertype == 0:
            server = 'hts.ebestsec.co.kr'
        
        self.XASession.ConnectServer(server, port)
        # print 'connect server'
        ret = self.XASession.Login(user, password, certpw, servertype, showcerterror)
                
        px.XASessionEvents.session = self.XASession
        self.XASession.flag = True
        while self.XASession.flag:
            pythoncom.PumpWaitingMessages()
        self.start_xing_query()
        pass

    def start_xing_query(self):
        self.xingTimer.start(1000)
        self.myDigitViewer.initXing(self.XASession)
        self.myDigitViewer.init_query()
        self.myDigitViewer.init_timer()
        self.myPositionViewer.initXing(self.XASession)
        self.myPositionViewer.initQuery()
        self.myPositionViewer.initTIMER()

    def xingTimerUpdate(self):
        if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
            if self.status_xi.text() == 'connect' or self.status_xi.text() == 'connect: 0000':
                self.status_xi.setText('connect.')
            elif self.status_xi.text() == 'disconnect':
                self.status_xi.setText('connect.')
            elif self.status_xi.text() == 'connect.':
                self.status_xi.setText('connect..')
            elif self.status_xi.text() == 'connect..':
                self.status_xi.setText('connect...')
            elif self.status_xi.text() == 'connect...':
                self.status_xi.setText('connect')
        else:
            self.status_xi.setText('disconnect')

    def autotimer_update(self):
        now_dt = dt.datetime.now()
        close_trigger = False
        close_hour = 6
        close_minute = 5
        re_toggle_hour = 17
        re_toggle_minute = 5
        if now_dt.hour == close_hour and now_dt.minute == close_minute and self.set_auto:
            close_trigger = True
        elif now_dt.hour == re_toggle_hour and now_dt.minute == re_toggle_minute and self.set_auto:
            if self.exchange_code == 'KRX':
                if self.ordermachineThread.isRunning():
                    logger.info("auto toggle false")
                    self.ui.actionExecute.setChecked(False)
                    self.ordermachineThread.terminate()
                    self.ordermachineThread.wait()
                    logger.info('OrderMachineThread stop')
                    close_trigger = True
        elif now_dt.hour == re_toggle_hour and now_dt.minute == re_toggle_minute + 1:
            # FIXME: because thread already is terminated, could not call isRunning func
            if not self.ordermachineThread.isRuning():
                logger.info("auto toggle true")
                self.ui.actionExecute.setChecked(True)
                self.slot_ToggleExecute(True)

        if close_trigger:
            logger.info("auto close trigger")
            self.ui.actionExecute.setChecked(False)
            self.ordermachineThread.terminate()
            self.ordermachineThread.wait()
            self.close()
            
    def slot_ToggleExecute(self, boolToggle):
        if (not self.ordermachineThread.isRunning()) and boolToggle:

            now_dt = dt.datetime.now()
            strdate = now_dt.strftime('%Y%m%d')
            is_expiredate = self.expiredate_util.is_expire_date(strdate)
            if now_dt.hour >= 7 and now_dt.hour < 17:
                self.exchange_code = 'KRX'
            else:
                self.exchange_code = 'EUREX'
            logger.info("exchange_code: %s" % self.exchange_code)
            if is_expiredate and now_dt.hour >= 17:
                now_dt = dt.datetime.now() + dt.timedelta(days=1)
                strdate = now_dt.strftime('%Y%m%d')
                expire_date_lst = self.expiredate_util.make_expire_date(strdate)
                logger.info('%s %s' % (strdate, ','.join(expire_date_lst)))

            if self.XASession.IsConnected() and self.XASession.GetAccountListCount():
                self.servername = (self.XASession.GetServerName()).strip()
                servername_re = "".join(re.split("[^a-zA-Z]*", self.servername))
                logger.info("servername: %s -> %s" % (self.servername, servername_re))
                self.servername = servername_re
                self.accountlist = self.XASession.GetAccountList()
                self.ordermachineThread._accountlist = self.accountlist
                self.ordermachineThread._servername = self.servername
                # print  self.servername, self.accountlist
                logmsg = 'servername: %s   account_no: %s' % (self.servername, self.accountlist[self.accountindex])
                logger.info(logmsg)
                self.initDB()
                self.ordermachineThread.init_thread_pool()
                self.ordermachineThread.start()
                logger.info('OrderMachineThread start')
            else:
                self.ui.actionExecute.setChecked(False)
        elif self.ordermachineThread.isRunning() and (not boolToggle):
            self.ordermachineThread.terminate()
            self.ordermachineThread.wait()
            logger.info('OrderMachineThread stop')
        pass

    def NotifyThreadEnd(self):
        self.ui.actionExecute.setChecked(False)
        logger.info('Thread finished')
        pass
    
    def slot_TriggerOrderList(self):
        if not self.myOrdListDlg.isVisible():
            self.myOrdListDlg.show()
        pass

    def NotifyOrderListViewer(self):
        # update ordlistDB
        logger.info('will update ordlistDB')
        self.myOrdListDlg.on_update_list()
        pass
    
    def triggeredDigitViewer(self):
        if not self.myDigitViewer.isVisible():
            self.myDigitViewer.show()
        pass
    
    def trigeredPositionViewer(self):
        if not self.myPositionViewer.isVisible():
            self.myPositionViewer.show()
        pass
        
        
class XingXASessionUpdate():
    def __init__(self, status_xi=None):
        self.status_xi = status_xi

    def Update(self, subject):
        msg =''
        for item in subject.data:
            msg = msg + ' ' + item                        
        if msg[:5] == ' 0000':
            self.status_xi.setText('connect:' + msg[:5])    
        pass


class observer_cmd:
    def Update(self, subject):
        subject.flag = False
        pass


class observer_t0441:
    def Update(self, subject):
        if len(subject.data) > 0:
            item = subject.data[0]
            if item['tsunik'] != '-':
                subject.pnl = int(int(item['tsunik'] or 0) * 0.001)
            else:
                subject.pnl = 0
        else:
            subject.pnl = 0
        subject.flag = False
        pass

        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myform = MainForm()
    myform.show()
    if myform.set_auto:
        myform.slot_ToggleExecute(True)
        myform.ui.actionExecute.setChecked(True)
    # sys.exit(app.exec_())
    app.exec_()

