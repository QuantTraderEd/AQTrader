# -*- coding: utf-8 -*-

import os
import sys
import ctypes
import time
import logging
import datetime as dt
import psutil
import redis
import pywinauto
import win32api, win32con
import win32gui, win32process


logger = logging.getLogger('TotalRun')
logger.setLevel(logging.DEBUG)
logger.propagate = False


# create file handler which logs even debug messages
fh = logging.FileHandler('TotalRun.log')
# fh = logging.Handlers.RotatingFileHandler('TotalRun.log', maxBytes=104857, backupCount=3)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handler to logger
logger.addHandler(fh)
logger.addHandler(ch)


close_notice_pos_x = 1340
close_notice_pos_y = 150


feeder_toggle_pos_x = 900
feeder_toggle_pos_y = 830
feeder_close_pos_x = 1200
feeder_close_pos_y = 800
oms_toggle_pos_x = 900
oms_toggle_pos_y = 620
oms_close_pos_x = 1200
oms_close_pos_y = 590

optionviewer_front_start_pos_x = 40
optionviewer_front_start_pos_y = 770
optionviewer_front_close_pos_x = 840
optionviewer_front_close_pos_y = 725

optionviewer_back_start_pos_x = 40
optionviewer_back_start_pos_y = 470
optionviewer_back_close_pos_x = 840
optionviewer_back_close_pos_y = 425

dbloader_start_stop_pos_x = 1342
dbloader_start_stop_pos_y = 815
dbloader_close_pos_x = 1660
dbloader_close_pos_y = 680

autootmtrader_start_stop_pos_x = 1442
autootmtrader_start_stop_pos_y = 630
autootmtrader_close_pos_x = 1675
autootmtrader_close_pos_y = 425

holiday_lst = ['20170509', 
               '20170606', 
               '20170815',
               '20171002',
               '20171003',
               '20171004',
               '20171005',
               '20171006',
               '20171009',
               '20171229',
               '20180101',
               ]


def get_window_title_pid(title):
    hwnd = win32gui.FindWindow(None, title)
    threadid, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid

def close_window_title(title):
    hwnd = win32gui.FindWindow(None, title)
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    pass

def close_notice_window():
    title = u'\uacf5\uc9c0\uc0ac\ud56d'
    w_handle = pywinauto.findwindows.find_windows(title=title, class_name='Afx:00400000:0')[0]
    pwa_app = pywinauto.application.Application()
    window = pwa_app.window_(handle=w_handle)
    window.Close()
    pass
    

def getProcessList():
    prcslst = []

    for proc in psutil.process_iter():
        psinfo = proc.as_dict(attrs=['name'])
        if psinfo['name']: prcslst.append(psinfo['name'])
            
    return prcslst

def click(x,y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def cp_start():
    logger.info('start cybos....')
    prcs_lst = getProcessList()
    if ('CpStart.exe' in prcs_lst) or ('DibServer.exe' in prcs_lst):
        logger.info('already run cybos...')
        return
        
    app = pywinauto.application.Application()
    app.start('C:/DAISHIN/starter/ncStarter.exe /prj:cp')
    
    count = 0
    while(1):
        time.sleep(20)
        # window = app.ncStarter
        w_handle_lst = pywinauto.findwindows.find_windows(title=u'CYBOS Starter', class_name='#32770')
        if len(w_handle_lst) == 0 and count <= 3:
            logger.info('there is no handle of cybos')
            count += 1
        elif len(w_handle_lst) > 0:
            w_handle = w_handle_lst[0]
            break
        elif count > 3:
            logger.error('there is no handle of cybos')
            return False
        
    window = app.window_(handle=w_handle)
    window.SetFocus()
    
    time.sleep(5)
    
    logger.info('get cybos window handler')
    
    ctrl = window[u'PLUSButton']
    ctrl.Click()
    
    ctrl = window[u'ONECLIKEdit2']
    ctrl.DrawOutline()
    ctrl.Click()
    ctrl.SetEditText("h6626075")

    ctrl = window[u'Button']
    ctrl.DrawOutline()
    time.sleep(3)
    ctrl.SetFocus()
    ctrl.Click()
    time.sleep(30)
    
    return True
    pass

def cp_kill():
    pid_dict = {}
            
    for proc in psutil.process_iter():
        psinfo = proc.as_dict(attrs=['name'])
        if psinfo['name'] in ['CpStart.exe',"DibServer.exe"]:            
            pid_dict[psinfo['name']] = proc.pid
            logger.info("ps_name: %s pid: %d" %(psinfo['name'], proc.pid))
            
    for key in pid_dict.iterkeys():
        logger.info('TASKKILL PID %s %s'%(pid_dict[key], key))
        os.system('TASKKILL /PID %d'%pid_dict[key])        
        
    pass

def day_session_starter():
    logger.info('start ZeroTrader...')
    nowtime = time.localtime()

    os.chdir(commonfolder + '\\ZeroTrader\\')        
    os.startfile('OptionCode.py')
    logger.info('start optioncode.py')
    
    time.sleep(2)
    # if nowtime.tm_hour == 7:
        # os.chdir('E:/Python/ZeroTrader/comm')        
        # os.startfile('sqlalchemy_FOCode.py')
        # logger.info('start sqlalchemy_FOCode.py')

    time.sleep(3)
    os.chdir(commonfolder + '\ZeroTrader\\ZeroFeeder\\')
    os.startfile('ZeroFeederMainForm.pyw')
    logger.info('start ZeroFeeder')
    
    time.sleep(5)
    os.chdir(commonfolder + '\\ZeroTrader\\ZeroOptionViewer\\')
    os.startfile('zerooptionviewer_main.py')
    logger.info('start ZeroOptionViewer front month')
    
    time.sleep(5)
    os.chdir(commonfolder + '\\ZeroTrader\\ZeroOptionViewer_BackMonth\\')
    os.startfile('zerooptionviewer_main.py')
    logger.info('start ZeroOptionViewer back month')
    
    time.sleep(5)
    os.chdir(commonfolder + '\\ZeroTrader\\ZeroOMS\\')
    os.startfile('zerooms_main.py')
    logger.info('start ZeroOMS')
    
    time.sleep(5)
    os.chdir(commonfolder + '\\ZeroTrader\\ZeroDBLoader\\')
    os.startfile('DBWidget.py')
    logger.info('start ZeroDBLoader')
    
    time.sleep(5)
    os.chdir(commonfolder + '\\ZeroTrader\\AutoTrader\\')
    os.startfile('AutoOTMTrader.py')
    logger.info('start AutoOTMTrader')
    
    logger.info('click optionviewer start')
    click(optionviewer_front_start_pos_x, optionviewer_front_start_pos_y)
    time.sleep(0.5)
    
    click(optionviewer_back_start_pos_x, optionviewer_back_start_pos_y)
    time.sleep(0.5)
    
    time.sleep(5)

    logger.info('click autootmtrader start button')
    click(autootmtrader_start_stop_pos_x, autootmtrader_start_stop_pos_y)    
    logger.info('%d, %d' % (autootmtrader_start_stop_pos_x, autootmtrader_start_stop_pos_y))
    time.sleep(0.5)    
    
    click_utck3_sync_button()
        
    time.sleep(0.5)
    pass


def test_trader_starter():
    time.sleep(5)
    os.chdir(commonfolder + '\\ZeroTrader_Test\\AutoFutArbTrader\\')
    # os.chdir(commonfolder + '\\ZeroTrader_Test\\AutoOTMTrader\\')
    os.startfile('AutoFutArbTrader.py')
    logger.info('start AutoFutArbTrader')
    # os.startfile('AutoOTMTrader.py')
    time.sleep(5)
    
    os.chdir(commonfolder + '\\ZeroTrader_Test\\ZeroOMS_MiniArb\\')
    os.startfile('zerooms_main.py')
    logger.info('start ZeroOMS_MiniArb')
    
    pass


def click_utck3_sync_button():
    logger.info('click utck3 sync button')
    for i in xrange(10):
        click(1640, 940)     # click at clock
        time.sleep(0.5)
        
def clear_ordno_dict():
    try:
        redis_client = redis.Redis()
        ordno_dict = redis_client.hgetall('ordno_dict')
        redis_client.delete('ordno_dict')
        logger.info(str(ordno_dict))
        logger.info('clear ordno_dict')
    except BaseException as e:
        logger.error('Fail to clear ordno_dict: ' + str(e))
        return
    pass


def make_miniarb_research_report():
    time.sleep(3)
    os.chdir(commonfolder + '\\ZeroTrader_Test\\algo strategy\\')
    os.startfile('run_miniarb_research_report.py')
    logger.info('run miniarb_research_report')
    pass
    


restart_option = False
commonfolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    logger.info('init TotalRun')
    
    prcslst = getProcessList()
    
    if not ("redis-server.exe" in prcslst):
        os.chdir('C:/Redis-x64-2.8.2103')
        # os.startfile('redis-server.exe redis.conf')
		redis_exe = "C:/Redis-x64-2.8.2103/redis-server.exe"
		redis_opt = "redis.conf"
		ctypes.windll.shell32.ShellExecuteA(0,'open', redis_exe, redis_opt, None, 1)
        logger.info('start redis-server...')
    else:
        logger.info('redis-server ok')
    
    if not ("UTCk3.exe" in prcslst):
        logger.info('start clock...')        
        # os.chdir('C:\\Program Files (x86)\\KRISS\\UTCk3.1\\')
        app = pywinauto.application.Application()
        app = app.start('C:\\Program Files (x86)\\KRISS\\UTCk3.1\\utck3.exe')
    else:
        logger.info('UTCK3 ok')
        
    if not ("TeamViewer.exe" in prcslst):
        logger.info('start team veiwer...')
        app = pywinauto.application.Application()
        app.start('C:\\Program Files (x86)\\TeamViewer\\TeamViewer.exe')
    else:
        logger.info('TeamViewer ok')
    
    if restart_option:
        logger.info('start restart...')
    
        if not ("DibServer.exe" in prcslst):
            is_logon_to_cp = cp_start()
            if not is_logon_to_cp:
                sys.exit()
            time.sleep(10)        
            logger.info('close notice')
            # click(close_notice_pos_x, close_notice_pos_y)
            close_notice_window()
            
        prcslst = getProcessList()
        if "DibServer.exe" in prcslst:
            day_session_starter()
        
        logger.info('end restart')
    
    else:
        logger.info('wait session trigger..')
    
    day_session_trigger = False
    night_session_trigger = False
    night_session_close_trigger = True
    report_trigger = False
    
    nowtime = time.localtime()
    if nowtime.tm_hour >= 18 or nowtime.tm_hour <= 5:
            day_session_trigger = False
            night_session_trigger = True
            night_session_close_trigger = False
    
    test_open_trigger = True
    test_close_trigger = False
    
    logger.info('day_session_trigger: ' + str(day_session_trigger))
    logger.info('night_session_trigger: ' + str(night_session_trigger))
    logger.info('night_session_close_trigger: ' + str(night_session_close_trigger))
    
    logger.info('Run TotalRun Loop')
    
    while True:
        time.sleep(10)
        nowtime = time.localtime()
        nowdatetime = dt.datetime.now()
        if nowdatetime.weekday() >= 5:
            logger.info('Stop@WeekEnd')
            break
        elif nowdatetime.strftime('%Y%m%d') in holiday_lst:
            logger.info('Stop@Holiday')
            break
        # if nowtime.tm_hour == 22 and nowtime.tm_min >= 0 and nowtime.tm_min <= 59 and test_open_trigger:
        if nowtime.tm_hour in [7,8,9,] and nowtime.tm_min >= 15 and nowtime.tm_min <= 59 and not day_session_trigger:
            nowdatetime = dt.datetime.now()
            if nowdatetime.weekday() >= 5:
                logger.info('Stop@WeekEnd')
                break
            elif nowdatetime.strftime('%Y%m%d') in holiday_lst:
                logger.info('Stop@Holiday')
                break
            
            prcslst = getProcessList()
            if not ("CpStart.exe" in prcslst):
                is_logon_to_cp = cp_start()
                if not is_logon_to_cp:
                    sys.exit()
                time.sleep(10)
                logger.info('close notice')
                # click(close_notice_pos_x, close_notice_pos_y)
                close_notice_window()
                
            prcslst = getProcessList()        
            time.sleep(.5)
            if "CpStart.exe" in prcslst:
                day_session_starter()
            
            logmsg = 'click DBLoader start button (%d, %d)' %(dbloader_start_stop_pos_x, dbloader_start_stop_pos_y)
            logger.info(logmsg)
            click(dbloader_start_stop_pos_x, dbloader_start_stop_pos_y)        
            time.sleep(1.0)
            logger.info('click the feeder')
            click(feeder_toggle_pos_x, feeder_toggle_pos_y)
            time.sleep(2.0)
            logger.info('click the oms run (%d, %d)' %(oms_toggle_pos_x, oms_toggle_pos_y))
            click(oms_toggle_pos_x, oms_toggle_pos_y)
            
            logger.info('End_day_session_trigger')
            day_session_trigger = True
            night_session_trigger = False
            
            test_open_trigger = False
            test_close_trigger = True
            
            test_trader_starter()
    
        elif nowtime.tm_hour == 17 and nowtime.tm_min >= 0 and nowtime.tm_min <= 35 and \
            not night_session_trigger and day_session_trigger:
            nowdatetime = dt.datetime.now()        
            logger.info('click the feeder')
            click(feeder_toggle_pos_x, feeder_toggle_pos_y)
            time.sleep(0.5)
            logger.info('click the oms run')
            click(oms_toggle_pos_x, oms_toggle_pos_x)
            logger.info('click the oms close')
            click(oms_close_pos_x, oms_close_pos_y)
            time.sleep(3)
            
            logger.info('click DBLoader stop button')
            click(dbloader_start_stop_pos_x, dbloader_start_stop_pos_y)
            time.sleep(0.5)
            logger.info('click DBLoader close button')
            click(dbloader_close_pos_x, dbloader_close_pos_y)
            time.sleep(3)
            
            logger.info('click autootmtrader stop button')
            time.sleep(0.5)    
            click(autootmtrader_start_stop_pos_x, autootmtrader_start_stop_pos_y)    
            logger.info('click autootmtrader close button')
            click(autootmtrader_close_pos_x, autootmtrader_close_pos_y)
            time.sleep(0.5)    
            
            click_utck3_sync_button()
            
            clear_ordno_dict()
            
            day_session_trigger = False
            night_session_trigger = False
            
        elif nowtime.tm_hour == 17 and nowtime.tm_min >= 40 and nowtime.tm_min <= 55 and not night_session_trigger:
            nowdatetime = dt.datetime.now()  
            if nowdatetime.weekday() >= 5:
                logger.info('Stop@WeekEnd')
                break
            elif nowdatetime.strftime('%Y%m%d') in holiday_lst:
                logger.info('Stop@Holiday')
                break
            
            logger.info('click utck3 sync button')
            
            click_utck3_sync_button()        
    
            os.chdir(commonfolder + '\\ZeroTrader\\ZeroOMS\\')
            os.startfile('zerooms_main.py')
            logger.info('start ZeroOMS')
            
            time.sleep(5)
            os.chdir(commonfolder + '\\ZeroTrader\\ZeroDBLoader\\')
            os.startfile('DBWidget.py')
            logger.info('start ZeroDBLoader')
            
            time.sleep(3)
            os.chdir(commonfolder + '\\ZeroTrader\\AutoTrader\\')
            os.startfile('AutoOTMTrader.py')
            logger.info( 'start AutoOTMTrader')
            time.sleep(1.0)    
            logger.info('click autootmtrader start button')
            click(autootmtrader_start_stop_pos_x, autootmtrader_start_stop_pos_y) 
            logger.info('%d, %d' % (autootmtrader_start_stop_pos_x, autootmtrader_start_stop_pos_y))
            
            time.sleep(10)
            logger.info('click DBLoader start button')
            click(dbloader_start_stop_pos_x, dbloader_start_stop_pos_y)     # click at switch1        
            time.sleep(10)
    
            logger.info('click the feeder')
            click(feeder_toggle_pos_x, feeder_toggle_pos_y)
            time.sleep(1)
            logger.info('click the oms run')
            click(oms_toggle_pos_x, oms_toggle_pos_y)
            
            day_session_trigger = False
            night_session_trigger = True
            night_session_close_trigger = False
            report_trigger = False
            
        elif nowtime.tm_hour == 18 and nowtime.tm_min == 35 and not report_trigger:
            make_miniarb_research_report()
            report_trigger = True
            
        # elif nowtime.tm_hour == 10 and nowtime.tm_min >= 0 and not test_close_trigger:
        elif nowtime.tm_hour == 6 and nowtime.tm_min >= 30 and not night_session_close_trigger:
            nowdatetime = dt.datetime.now()        
            logger.info('click the feeder run')
            click(feeder_toggle_pos_x, feeder_toggle_pos_y)
            time.sleep(1)
            logger.info('click the feeder close')
            click(feeder_close_pos_x, feeder_close_pos_y)
            time.sleep(1)
            logger.info('click the oms run')
            click(oms_toggle_pos_x, oms_toggle_pos_y)
            logger.info('click the oms close')
            click(oms_close_pos_x, oms_close_pos_y)
            time.sleep(3)
            
            logger.info('click optionviewer close button')
            click(optionviewer_front_close_pos_x, optionviewer_front_close_pos_y)
            time.sleep(1)
            
            time.sleep(1)
            click(optionviewer_back_close_pos_x, optionviewer_back_close_pos_y)
            time.sleep(1)
            
            time.sleep(1)
            click(optionviewer_back_close_pos_x, optionviewer_back_close_pos_y)
            time.sleep(1)
            
            logger.info('click DBLoader stop button')
            click(dbloader_start_stop_pos_x, dbloader_start_stop_pos_y)     # click at switch1
            time.sleep(0.5)
            logger.info('click DBLoader close button')
            click(dbloader_close_pos_x, dbloader_close_pos_y)
            time.sleep(3)
            
            logger.info('click autootmtrader stop button')
            click(autootmtrader_start_stop_pos_x, autootmtrader_start_stop_pos_y)
            time.sleep(0.5)    
            logger.info('click autootmtrader close button')
            click(autootmtrader_close_pos_x, autootmtrader_close_pos_y)
            time.sleep(0.5)    
            
            pid_dict = {}
            
            for proc in psutil.process_iter():
                psinfo = proc.as_dict(attrs=['name'])
                if psinfo['name'] in ["pythonw.exe"]:
                    logger.info('%s'%psinfo['name'])
                    os.system('TASKKILL /PID %d'%proc.pid)
                elif psinfo['name'] in ['CpStart.exe',"DibServer.exe"]:
                    # print proc.pid, psinfo['name']
                    pid_dict[psinfo['name']] = proc.pid
                    
            for key in pid_dict.iterkeys():
                logger.info('%s %s'%(pid_dict[key], key))
                os.system('TASKKILL /PID %d'%pid_dict[key])
    
            clear_ordno_dict()
    
            night_session_close_trigger = True
            day_session_trigger = False
            
            # test_close_trigger = False
            # test_open_trigger = False
            # print 'test done'
            
            
if __name__ == "__main__":
    restart_option = False
    main()